from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from .forms import LowercaseAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .utils import send_welcome_email
from django.views.decorators.cache import never_cache

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        print("Submitted data:", request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")
            form.save()
            user = form.save()
            send_welcome_email(user)  # <--- Send email here
            return redirect('accounts:login')
        else:
            print("Form errors:", form.errors)
    else:
        form = SignUpForm()

    return render(request, 'accounts/register.html', {'form': form})



# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username').lower()
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('accounts:dashboard')  # Redirect to homepage after login
#             else:
#                 error = "Invalid credentials"
#                 return render(request, 'accounts/login.html', {'error': error})
#     else:
#         form = AuthenticationForm()
#     return render(request, 'accounts/login.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LowercaseAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')  # Already lowercase
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accounts:dashboard')
            else:
                error = "Invalid credentials"
                return render(request, 'accounts/login.html', {'error': error, 'form': form})
    else:
        form = LowercaseAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


@never_cache
@login_required
def dashboard(request):
    return render(request, "accounts/member-single.html")

@never_cache
@login_required
def contact(request):
    return render(request, "accounts/contact.html")


from django.http import JsonResponse
from .models import State

def get_lgas(request, state_id):
    try:
        state = State.objects.get(id=state_id)
        lgas = state.lgas.all().values('id', 'name')
        return JsonResponse({'lgas': list(lgas)})
    except State.DoesNotExist:
        return JsonResponse({'error': 'State not found'}, status=404)


# from django.shortcuts import render
# from .models import College  # assuming College is the model name
#
# def get_colleges(request):
#     colleges = College.objects.all()  # Fetch all colleges from the database
#     return render(request, 'accounts/register.html', {'colleges': colleges})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm

@never_cache
@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("accounts:dashboard")  # Redirect to profile page after update
    else:
        form = EditProfileForm(instance=user)

    return render(request, "accounts/edit_profile.html", {"form": form})


from django.db.models import Q
from django.contrib.auth import get_user_model
from members.models import Like

def user_search(request):
    query = request.GET.get('username', '').lower()
    results = []

    if query:
        results = User.objects.filter(username__icontains=query).exclude(id=request.user.id)

    # Get list of users already liked
    liked_user_ids = Like.objects.filter(user_from=request.user).values_list('user_to__id', flat=True)

    return render(request, 'accounts/search_results.html', {
        'results': results,
        'query': query,
        'liked_user_ids': liked_user_ids
    })



from .models import User
from .utils import get_online_users
from members.models import Like
from django.core.paginator import Paginator

@login_required
def online_users_view(request):
    online_users = get_online_users().exclude(id=request.user.id)

    # Get IDs of users the current user has already liked
    liked_user_ids = Like.objects.filter(user_from=request.user).values_list('user_to__id', flat=True)

    # Paginate the online users list
    paginator = Paginator(online_users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/online_users.html', {
        'online_users': page_obj,
        'page_obj': page_obj,
        'liked_user_ids': liked_user_ids
    })







from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model, login
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

User = get_user_model()


# ✅ Custom Password Reset View
def custom_password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(
                    reverse('accounts:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                )

                # ✅ Send Reset Email

                subject = "Password Reset Request"
                from_email = settings.DEFAULT_FROM_EMAIL
                to = [email]

                # Render your HTML template
                html_content = render_to_string('accounts/password_reset_email.html', {'reset_link': reset_link})

                # Create the email message and attach HTML
                email_message = EmailMultiAlternatives(subject, '', from_email, to)
                email_message.attach_alternative(html_content, "text/html")
                email_message.send()


            return redirect('accounts:password_reset_done')  # Redirect to success page

    else:
        form = PasswordResetForm()

    return render(request, 'accounts/password_reset.html', {'form': form})


# ✅ Password Reset Done View
def custom_password_reset_done(request):
    return render(request, 'accounts/password_reset_done.html')


# ✅ Password Reset Confirm View
def custom_password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError):
        return HttpResponse("Invalid reset link", status=400)

    if not default_token_generator.check_token(user, token):
        return HttpResponse("Invalid reset link", status=400)

    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:password_reset_complete')  # Redirect after successful reset
    else:
        form = SetPasswordForm(user)

    return render(request, 'accounts/password_reset_confirm.html', {'form': form})


# ✅ Password Reset Complete View
def custom_password_reset_complete(request):
    return render(request, 'accounts/password_reset_complete.html')

def single(request):
    return render(request, "accounts/single.html")
