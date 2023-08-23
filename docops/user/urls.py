from django.urls import path
from . import views

app_name = 'user'

urlpatterns =[
    path('hoslogin/',views.HosLogin,name='hoslogin'),
    path('hoslogout/',views.HosLogout,name='hoslogout'),
    path('hossignup/',views.HosSignup,name='hossignup'),

    path('signup/',views.Signup,name='signup'),
    path('login/',views.Login,name='login'),
    path('logout/',views.Logout,name='logout'),
]