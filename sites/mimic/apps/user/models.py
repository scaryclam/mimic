from django.contrib.auth.models import AbstractBaseUser, BaseUserManager  # pragma: no cover
from django.db import models  # pragma: no cover


# Managers
class UserManager(BaseUserManager):  # pragma: no cover
    def create_user(self, username, email, password=None, **extra_fields):
        user = self.model(username=username,
                          email=UserManager.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        user = self.create_user(username,
                                email,
                                password=password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):  # pragma: no cover
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=300, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    first_login = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False, null=False)
    is_superuser = models.BooleanField(default=False, null=False)
    is_active = models.BooleanField(default=True, null=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField('auth.Group', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        if self.first_name:
            return "%s %s" % (self.first_name, self.last_name)
        return self.username

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        return self.username

    def __str__(self):
        return str(self.__unicode__())

    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always
        if self.is_superuser:
            return True
        return True

    def has_perms(self, *args, **kwargs):
        # Simplest possible answer: Yes, always
        if self.is_superuser:
            return True
        return True

    def has_module_perms(self, app_label):
        # Simplest possible answer: Yes, always
        if self.is_superuser:
            return True
        return True

