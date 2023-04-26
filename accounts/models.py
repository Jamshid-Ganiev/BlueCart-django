from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password, phone_number=None):
        if not email:
            raise ValueError('User must have an email address.')
        
        if not username:
            raise ValueError('User must have a username.')
        
        user = self.model(
            # it configures the format of an email, if the email is in capital letters, then changed to lowercase letters
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
        )

        user.set_password(password)

        # saves the user to the DataBase
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            # it configures the format of an email, if the email is in capital letters, then changed to lowercase letters
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            password = password,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        # saves the user to the DataBase
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    username      = models.CharField(max_length=50, unique=True)
    first_name    = models.CharField(max_length=50)
    last_name     = models.CharField(max_length=50)
    email         = models.EmailField(max_length=100, unique=True)
    phone_number  = models.CharField(max_length=50, blank=True, null=True)

    date_joined   = models.DateTimeField(auto_now_add=True)
    last_login    = models.DateTimeField(auto_now_add=True)

    # required
    is_admin      = models.BooleanField(default=False)
    is_staff      = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, add_label):
        return True
    

class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line = models.CharField(blank=True, max_length=120)
    profile_picture = models.ImageField(default="/userProfile/default_profile_pic.png", upload_to='userProfile/')

    def __str__(self):
        return self.user.username
    
    def full_address(self):
        return self.address_line
    