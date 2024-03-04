from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe


def avatar_directory_path(instance: "User", filename: str) -> str:
    return "users/profile_{pk}/avatar/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Profile(models.Model):
    object = None
    DoesNotExist = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(
        verbose_name='Avatar',
        null=True, blank=True,
        upload_to=avatar_directory_path,
    )

    def get_avatar(self):
        if not self.avatar:
            return '/static/images/owl-gray.svg'
        return self.avatar.url

    def avatar_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.get_avatar())

    avatar_tag.short_description = 'Avatar'


