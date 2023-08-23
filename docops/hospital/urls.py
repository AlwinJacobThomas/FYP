from django.urls import path
from . import views

app_name = 'hospital'

urlpatterns =[
    path('',views.hos_dashboard,name='hos_dashboard'),
    path('add_profile',views.AddProfile,name='add_profile'),
    path('edit_profile',views.EditProfile,name='edit_profile'),
    path('doctor_profile/<int:doctor_id>',views.DoctorProfile,name='doctor_profile'),
    
    path('add_doctor',views.AddDoctor,name='add_doctor'),
    path('edit_doctor/<int:doctor_id>',views.EditDoctor,name='edit_doctor'),
    path('delete_doctor/<int:doctor_id>',views.DeleteDoctor,name='delete_doctor'),
    path('add_facility',views.AddFacility,name='add_facility'),
    path('delete_facility/<int:facility_id>',views.DeleteFacility,name='delete_facility'),
    # path('doctor_list',views.DoctorList,name='doctor_list'),

    path('hos_appointments/',views.HosAppointmentsView,name='hos_appointments'),
    path('hos_appointments/<int:appointment_id>/confirm/',views.HosAppointmentConfirmView,name='hos_appointment_confirm'),
    path('hos_doctors/',views.HosDoctorsView,name='hos_doctors'),
]