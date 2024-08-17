from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import IntegrityError

class Company(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    domain = models.CharField(max_length=255, db_index=True)
    year_founded = models.IntegerField(null=True, blank=True, db_index=True)
    industry = models.CharField(max_length=255, db_index=True)
    size_range = models.CharField(max_length=50, db_index=True)
    locality = models.CharField(max_length=255, db_index=True)
    country = models.CharField(max_length=255, db_index=True)
    linkedin_url = models.URLField(max_length=500, blank=True)
    current_employee_estimate = models.IntegerField(db_index=True)
    total_employee_estimate = models.IntegerField(db_index=True)
    
    def __str__(self):
        return self.name


class CompanyFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File uploaded at {self.uploaded_at}"

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        try:
            user = self.model(username=username, **extra_fields)
            if password:
                user.password = make_password(password)  # Hash the password before saving
            user.save(using=self._db)
            return user
        except IntegrityError as e:
            print(f"Error creating user: {e}")  # Debugging line
            return None

    def create_superuser(self, username, password=None, **extra_fields):
        return self.create_user(username, password, **extra_fields)
    
class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)  # Add this line

    objects = CustomUserManager()  # Use the custom manager

    USERNAME_FIELD = 'username'

    def save(self, *args, **kwargs):
        self._state.adding = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username