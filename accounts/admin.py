from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User



class UserAdmin(UserAdmin):
    # Add additional fields to the admin if needed
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'profile_image', 'marital_status', 'gender', 'looking_for', 'birthday', 'state', 'image1', 'image2', 'image3', 'image4', 'image5')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'profile_image', 'marital_status', 'gender', 'looking_for', 'birthday', 'state', 'image1', 'image2', 'image3', 'image4', 'image5')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', )

admin.site.register(User, UserAdmin)

# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser
#
# class CustomUserAdmin(UserAdmin):
#     # Add additional fields to the admin if needed
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': ('bio', 'profile_image')}),
#     )
#
# admin.site.register(CustomUser, CustomUserAdmin)
