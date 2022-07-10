from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    
)

# Create your models here.

class UserManager(BaseUserManager):
    
    def create_user(self,email,password=None, **otherField):
        if not email or "@" not in email:
            raise ValueError("Email should not empty. Please recheck your request")
        user = self.model(email=self.normalize_email(email),**otherField )
        user.set_password(password)
        user.save(using=self.db)
        
        return user
    
    def create_superuser(self,email,password, **otherField):
        if not email or "@" not in email:
            raise ValueError("Email should not empty. Please recheck your request")
        
        supuser = self.model(email=self.normalize_email(email),**otherField )
        supuser.set_password(password)
        supuser.is_active=True
        supuser.is_staff=True
        supuser.is_superuser=True
        supuser.save(using=self.db)
        
        return supuser

class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(max_length=255,unique=True)
    user_name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    
    objects=UserManager()
    
    USERNAME_FIELD="email"