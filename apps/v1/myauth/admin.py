# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from rest_framework_api_key.admin import ApiKeyAdmin
from rest_framework_api_key.models import APIKey

from .models import Account, Admin, Token

class UserAdmin(DjangoUserAdmin):
    model = Account
    list_display = ('email', 'name', 'is_active',)
    list_filter = ('email', 'name', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_active')}
        ),
    )
    filter_horizontal = []
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(Account, UserAdmin)
admin.site.register(Admin)

# Override API Key admin
class MyApiKeyAdmin(ApiKeyAdmin):
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


admin.site.unregister(APIKey)
admin.site.register(APIKey, MyApiKeyAdmin)


class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created_at')
    fields = ('user',)
    ordering = ('-created_at',)


admin.site.register(Token, TokenAdmin)