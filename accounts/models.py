from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.



class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('User Must Have A Email Address')
        if not username:
            raise ValueError('User Must Have A Username')
        user=self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.is_active = True  # Allow the user to log in after registration
        user.save()
        return user 
    
    def create_superuser(self,first_name,last_name,username,email,password):
        user = self.create_user(
            email= self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            password=password,
        
        )
        user.is_active = True
        user.is_admin = True
        user.is_staff =True
        user.is_superadmin = True
        user.set_password(password)   # Encrypts password before saving

        user.save()
        return user


class Account(AbstractBaseUser):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    phone = models.CharField(max_length=20)


    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()


    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
