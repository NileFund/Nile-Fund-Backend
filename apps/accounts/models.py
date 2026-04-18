from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models
from apps.common.models import TimeStampedModel
from apps.common.validators import validate_egyptian_phone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required.')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', False) 
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True) 
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    email      = models.EmailField(unique=True)
    phone      = models.CharField(
        max_length=11,
        unique=True,
        validators=[validate_egyptian_phone],
    )
    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
    )

    birthdate        = models.DateField(blank=True, null=True)
    facebook_profile = models.URLField(blank=True, null=True)
    country          = models.CharField(max_length=60, blank=True, null=True)

    is_active  = models.BooleanField(
        default=False, 
        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
    )   
    is_staff   = models.BooleanField(default=False)

    failed_delete_attempts = models.IntegerField(default=0)
    
    email_verification_sent_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    objects = UserManager()

    class Meta:
        db_table = 'accounts_user'
        indexes  = [models.Index(fields=['email'])]
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'