from django.db import models
from user.models import HospitalProfile
import os
import uuid
from django.utils.deconstruct import deconstructible
# Create your models here.


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


path_and_rename = PathAndRename("doctor/")


class Doctor(models.Model):
    name = models.CharField(max_length=255,)
    specialization = models.CharField(max_length=255)
    qualifications = models.TextField()
    experience = models.PositiveIntegerField()
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    pic = models.ImageField('Patient_Profile_Pic',
                            upload_to=path_and_rename, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    hospital = models.ForeignKey(HospitalProfile,on_delete=models.CASCADE,related_name='doctor')

    def __str__(self):
        return self.name


class Facility(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    hospital = models.ForeignKey(HospitalProfile,on_delete=models.CASCADE,related_name='facility')
    
    def __str__(self):
        return self.name        
