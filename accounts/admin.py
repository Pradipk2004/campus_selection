# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentProfile, RecruiterProfile, StudentDocument
from core.admin import custom_admin_site

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff', 'is_active')}),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'branch')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('user',)

class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'contact_number')
    search_fields = ('user__username', 'company_name')
    readonly_fields = ('user',)

class StudentDocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'uploaded_at')
    search_fields = ('user__username',)
    readonly_fields = ('uploaded_at',)

# Register with your custom admin site only
custom_admin_site.register(CustomUser, CustomUserAdmin)
custom_admin_site.register(StudentProfile, StudentProfileAdmin)
custom_admin_site.register(RecruiterProfile, RecruiterProfileAdmin)
custom_admin_site.register(StudentDocument, StudentDocumentAdmin)
