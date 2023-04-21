from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, password, **kwargs):
        print('=============')
        user = self.model(
            # phone_number=phone_number,
            username=username,
            # profile=profile,
            # last_login=timezone.now(),
        )
        user.set_password(password)
        print('hashing!')
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **kwargs):
        user = self.create_user(username, password, profile=None, **kwargs)
        user.is_superuser = True
        user.save(using=self._db)
        return user
