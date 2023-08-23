from django.contrib import admin
from .models import User,PatientProfile,HospitalProfile,Hospital,Patient
# Register your models here.

admin.site.register(User)
admin.site.register(HospitalProfile)
admin.site.register(PatientProfile)
admin.site.register(Hospital)
admin.site.register(Patient)
