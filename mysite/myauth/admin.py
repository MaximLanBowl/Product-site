from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from myauth import models
from myauth.models import Profile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('avatar_tag', 'user')
    readonly_fields = ['avatar_tag']
    fields = ('avatar_tag', 'user')


class ProfileInline(admin.StackedInline):
    model = models.Profile
    can_delete = False
    fields = ('avatar_tag',)
    readonly_fields = ['avatar_tag']


class EUserAdmin(UserAdmin):

    inlines = [
        ProfileInline
    ]
    list_display = ('avatar_tag',) + UserAdmin.list_display

    def avatar_tag(self, obj):
        return obj.profile.avatar_tag()


admin.site.register(Profile, UserProfileAdmin)

admin.site.unregister(User)
admin.site.register(User, EUserAdmin)