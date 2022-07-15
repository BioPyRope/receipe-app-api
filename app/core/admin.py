from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models as coreM
from django.utils.translation import gettext_lazy as _
# Register your models here.

class UserAdmin(BaseUserAdmin):
    ordering=["id"]
    list_display=["email","user_name"]
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('user_name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']

    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('email', 
                   'password1',
                   "password2",
                   "user_name",
                   'is_active',
                    'is_staff',
                    'is_superuser',),
    }),
    )
    
    
admin.site.register(coreM.User,UserAdmin)
admin.site.register(coreM.Recipes)