from django.urls import path
from . import views

app_name = 'coreapp'

urlpatterns =[
    path('',views.home,name='home'),

    
    path('doc_search',views.doc_search,name='doc_search'),
    path('hos_search',views.hos_search,name='hos_search'),
   
    #changed the edit profile view
    path('edit_profile',views.EditProfile,name='edit_profile'),
    path('add_profile',views.AddProfile,name='add_profile'),
   

    #doctor
    path('booking',views.booking,name='booking'),
    
    path('doctor/<int:doctor_id>/review/', views.AddReview, name='add_review'),
    

    path('add_medical/',views.AddMedical,name='add_medical'),
    path('appointment/', views.AppointmentsView, name='appointment'),
    path('hos_profile/<int:hospital_id>/',views.HosProfile,name='hos_profile'),
    path('doc_profile/<int:doctor_id>',views.DoctorProfile,name='doc_profile'),
    path('appointments/<int:appointment_id>/confirm/',views.AppointmentConfirm,name='appointment_confirm'),

    # path('doctor/<int:doctor_id>/', views.DoctorDetailView, name='doctor_detail'),
    path('doctor/<int:doctor_id>/appointment_booking/', views.AppointmentBookingView, name='appointment_booking'),
    path('appointments/', views.AppointmentsView, name='appointments'),
    path('appointments/<int:appointment_id>/treatment_review/', views.TreatmentReviewView, name='treatment_review'),
    
    
]