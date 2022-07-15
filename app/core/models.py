
from django.conf import settings
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
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
    
    def create(self):
        raise ObjectDoesNotExist("the method has been aborted")
    
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
    
    objects=UserManager() #critical custom admin的關鍵
    
    USERNAME_FIELD="email"

class Recipes(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, editable = False,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    time=models.IntegerField()
    price=models.DecimalField(max_digits=5,decimal_places=2)
    description=models.TextField(blank=True)
    link=models.CharField(max_length=255,blank=True)
    
    def __str__(self) -> str:
        return self.title