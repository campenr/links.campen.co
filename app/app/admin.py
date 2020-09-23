from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User, Link


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Role'), {'fields': ('role',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_filter = ('role', 'is_superuser')
    list_display = ('email', 'role', 'is_superuser')
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Link)
class LinkAdmin(ModelAdmin):

    fieldsets = (
        (None, {'fields': ('url', 'private', 'owner')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('url', 'private', 'owner'),
        }),
    )

    list_display = ('url', 'name', 'token', 'private', 'owner', 'created')

