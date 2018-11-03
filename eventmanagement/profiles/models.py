from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    ACCOUNT_PENDING, ACCOUNT_APPROVED = range(2)
    ACCOUNT_STATUS = (
        (ACCOUNT_PENDING, 'pending'),
        (ACCOUNT_APPROVED, 'approved'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, related_name='profile_user')
    nickname = models.CharField(blank=True, max_length=100)
    status = models.SmallIntegerField(choices=ACCOUNT_STATUS, default=0)

    class Meta:
        default_related_name = 'profiles'
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def __str__(self):
        return self.nickname

    def is_approved(self):
        print(self.status)
        if self.status == 1:
            return True
        return False
