from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.deconstruct import deconstructible
import uuid
import os
from location_field.models.plain import PlainLocationField

# --------------file renamer--------------------


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join('hospital/', filename)


# -------------------USER-------------------------
# --------usermanager----------
class UserAccountManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_admin', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        if other_fields.get('is_admin') is not True:
            raise ValueError(
                'Superuser must be assigned to is_admin=True.')

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user

# --------user----------


class User(AbstractBaseUser, PermissionsMixin):
    # adding custom field "role" in default User model
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        HOSPITAL = "HOSPITAL", 'Hospital'
        PATIENT = "PATIENT", 'Patient'

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # special permission which define that
    # the new user is hospital or patient

    USERNAME_FIELD = "email"

    # defining the manager for the UserAccount model
    objects = UserAccountManager()

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)

# ------------Patient------------------------------


class PatientManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.PATIENT)
# patient proxy class  for setting baserole


class Patient(User):
    base_role = User.Role.PATIENT

    class Meta:
        proxy = True

    patient = PatientManager()
# Automatic creation of UserProfile during UserCreation
# @receiver(post_save,sender=Patient)
# def create_user_profile(sender,instance,created,**kwargs):
#      if created and instance.role == "PATIENT":
#           PatientProfile.objects.create(user=instance)


# userprofile to created user
path_and_rename = PathAndRename("patient/")


class PatientProfile(models.Model):
    class Gender(models.TextChoices):
        male = "MALE", 'Male'
        female = "FEMALE", 'Female'
        other = "OTHER", 'Other'

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='patient')
    patient_id = models.IntegerField(primary_key=True, editable=False)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(
        max_length=20, choices=Gender.choices, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    dob = models.DateField()

    pic = models.ImageField('Patient_Profile_Pic',
                            upload_to=path_and_rename, blank=True, null=True)

    def __str__(self):
        return self.user.email
# ---------------Hospital----------------------------------------


class HospitalManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.HOSPITAL)
# doctor role class


class Hospital(User):
    base_role = User.Role.HOSPITAL

    class Meta:
        proxy = True

    hospital = HospitalManager()


# Automatic creation of UserProfile during UserCreation
# @receiver(post_save,sender=Hospital)
# def create_user_profile(sender,instance,created,**kwargs):
#      if created and instance.role == "HOSPITAL":
#           HospitalProfile.objects.create(user=instance)

# userprofile to created user
path_and_rename = PathAndRename("hospital/")


class HospitalProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='hospital')
    hospital_id = models.IntegerField(primary_key=True, editable=False)
    hospital_name = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=150, blank=True)
    website = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    location = PlainLocationField(zoom=7, null=True, blank=True)
   
    
    
    pic = models.ImageField('Hospital_Profile_Pic',
                            upload_to=path_and_rename, blank=True, null=True)
    
    def __str__(self):
        return self.user.email
