from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User, State, LGA, College, GradYear


class LowercaseAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        return self.cleaned_data['username'].lower()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    state = forms.ModelChoiceField(
        queryset=State.objects.all(),
        required=True,
        empty_label="Select a state",
        widget=forms.Select(attrs={'id': 'stateSelect'})
    )
    lga = forms.ModelChoiceField(
        queryset=LGA.objects.none(),  # Initially empty
        required=False,
        empty_label="Select an LGA",
        widget=forms.Select(attrs={'id': 'lgaSelect'})
    )
    college = forms.ModelChoiceField(
        queryset=College.objects.all(),
        required=True,
        empty_label="Select a college",
        widget=forms.Select(attrs={'id': 'collegeSelect'})
    )
    grad_year = forms.ModelChoiceField(
        queryset=GradYear.objects.all(),
        required=True,
        empty_label="Select a Grad Year",
        widget=forms.Select(attrs={'id': 'gradYearSelect'})
    )



    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2', 'profile_image',
            'first_name', 'middle_name', 'last_name', 'marital_status', 'gender',
            'looking_for', 'birthday', 'state', 'lga', 'college', 'grad_year', 'bio'
        ]


    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.lower()  # Force lowercase


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Debug: Log the state of the form's data and queryset initialization
        print("Form initialized with data:", self.data)
        print("State queryset (initial):", self.fields['state'].queryset)
        print("LGA queryset (initial):", self.fields['lga'].queryset)

        # Prepopulate LGAs if a state is selected
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                state = State.objects.get(id=state_id)
                self.fields['lga'].queryset = LGA.objects.filter(state=state)
                print(f"LGA queryset for State ID {state_id}:", self.fields['lga'].queryset)
            except (ValueError, State.DoesNotExist):
                print(f"Invalid State ID: {self.data.get('state')}")
                self.fields['lga'].queryset = LGA.objects.none()
        elif self.instance and self.instance.state:
            self.fields['lga'].queryset = self.instance.state.lgas.all()

        # Debug: Ensure college queryset is loaded correctly
        self.fields['college'].queryset = College.objects.all()
        print("College queryset:", self.fields['college'].queryset)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.middle_name = self.cleaned_data['middle_name']
        user.last_name = self.cleaned_data['last_name']
        user.profile_image = self.cleaned_data['profile_image']
        user.state = self.cleaned_data['state']  # State object
        user.lga = self.cleaned_data['lga']  # LGA object
        user.college = self.cleaned_data['college']  # College object
        user.grad_year = self.cleaned_data['grad_year']
        print("Saving profile image:", self.cleaned_data['profile_image'])  # Debugging profile image

        # Debug: Log the user data being saved
        print("Saving user with data:")
        print("  State:", user.state)
        print("  LGA:", user.lga)
        print("  College:", user.college)
        print("Saving profile image:", self.cleaned_data['profile_image'])
        print("User saved:", user)


        if commit:
            user.save()
        return user




class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'middle_name', 'last_name', 'bio', 'marital_status', 'gender',
            'looking_for', 'birthday', 'state', 'lga', 'college', 'grad_year',
            'profile_image', 'image1', 'image2', 'image3', 'image4', 'image5'
        ]
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

        # Debug: Log form initialization
        print("Edit Profile Form Initialized with:", self.instance)

    def save(self, commit=True):
        """Preserve existing values if fields are left blank"""
        user = super().save(commit=False)

        # Loop through each field and keep original value if unchanged
        for field in self.fields:
            if not self.cleaned_data.get(field):  # If empty, restore old value
                setattr(user, field, getattr(self.instance, field))

        if commit:
            user.save()
        return user












# from django.contrib.auth.forms import UserCreationForm
# from django import forms
# from .models import User, State, LGA
#
# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#
#     # Dynamically populate State and LGA fields
#     state = forms.ModelChoiceField(
#         queryset=State.objects.all(),
#         required=True,
#         empty_label="Select a state",
#         widget=forms.Select(attrs={'id': 'state'})  # Add ID for JS
#     )
#     lga = forms.ModelChoiceField(
#         queryset=LGA.objects.none(),  # Initially empty
#         required=False,
#         empty_label="Select an LGA",
#         widget=forms.Select(attrs={'id': 'lga'})  # Add ID for JS
#     )
#
#     class Meta:
#         model = User
#         fields = [
#             'username', 'email', 'password1', 'password2', 'profile_image',
#             'first_name', 'last_name', 'marital_status', 'gender', 'looking_for',
#             'birthday', 'state', 'lga', 'bio'
#         ]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         # If a state is pre-selected, populate the corresponding LGAs
#         if 'state' in self.data:
#             try:
#                 state_id = int(self.data.get('state'))
#                 self.fields['lga'].queryset = LGA.objects.filter(state_id=state_id)
#             except (ValueError, TypeError):
#                 self.fields['lga'].queryset = LGA.objects.none()
#         elif self.instance and self.instance.state:
#             self.fields['lga'].queryset = self.instance.state.lgas.all()
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data['email']
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.profile_image = self.cleaned_data['profile_image']
#         user.state = self.cleaned_data['state']
#         user.lga = self.cleaned_data['lga']
#         if commit:
#             user.save()
#         return user



# from django.contrib.auth.forms import UserCreationForm
# from django import forms
# from .models import User
#
# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2', 'profile_image', 'first_name', 'last_name', 'marital_status', 'gender', 'looking_for', 'birthday', 'state']
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data['email']
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.profile_image = self.cleaned_data['profile_image']
#         # user.marital_status = self.cleaned_data['marital_status']
#         # user.gender = self.cleaned_data['gender']
#         # user.gender_search = self.cleaned_data['looking_for']
#         if commit:
#             user.save()
#         return user
