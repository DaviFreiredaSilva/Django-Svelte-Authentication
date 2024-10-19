from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserAccountManager(BaseUserManager):
     def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("Um email é necessário.")
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.is_staff=False
        user.set_password(password)
        user.save()

        profile = Profile.objects.create(user=user)
        profile.save()

        return user
     
     def create_superuser(self, email, name, password=None):
        if not email:
            raise ValueError("Um email é necessário.")
        
        user = self.create_user(email, name, password)
        user.is_superuser=True
        user.is_staff=True
        user.save()

        return user

class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['name']

    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name
    
    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True, blank=True)
    phoneNumber = models.CharField(max_length=255, null=True, blank=True)