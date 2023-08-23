from django.shortcuts import render, reverse, redirect, get_object_or_404
from .forms import AddHospitalProfileForm,FacilityForm

from .models import Doctor,Facility
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .forms import DoctorForm
from django.http import Http404
from coreapp.models import Appointment, AppointmentReview
from django.http import HttpResponse
from django.contrib import messages
import math
from django.db.models import Avg, Sum

User = get_user_model()


def hos_dashboard(request):
    if request.user.is_authenticated:
        if request.user.role == 'HOSPITAL':
            try:
                hospital = request.user.hospital
                print(f'----{hospital.hospital_name}')
                doctors = Doctor.objects.filter(hospital=hospital)
                doctor_count = doctors.count()
                review_count = AppointmentReview.objects.filter(
                    appointment__hospital=hospital).count()
                facility = Facility.objects.all().filter(hospital=hospital)
                return render(request, 'hospital/hos_dashboard.html', {
                    'hospital': hospital,
                    'doctors': doctors,
                    'review_count': review_count,
                    'doctor_count': doctor_count,
                    'facilities':facility
                })
            except ObjectDoesNotExist:
                return redirect(reverse('hospital:add_profile'))
        elif request.user.role == 'PATIENT':
            return redirect(reverse('coreapp:home'))
        else:
            return redirect('/admin/')

    else:
        return redirect('user:hossignup')


@login_required
def AddProfile(request):
    if request.user.role == 'HOSPITAL':
        try:
            instance = request.user.hospital
            return redirect('hospital:edit_profile')
        except ObjectDoesNotExist:
            form = AddHospitalProfileForm()
            if request.method == "POST":
                form = AddHospitalProfileForm(request.POST, request.FILES)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.location = request.POST['location']
                    post.user = User.objects.get(id=request.user.id)
                    if 'pic' in request.FILES:
                        post.pic = request.FILES['pic']
                    post.save()
                    return redirect(reverse('hospital:hos_dashboard'))
                else:
                    return render(request, 'hospital/add-profile.html', {
                        'form': form,
                        'error': True,
                    })
            return render(request, 'hospital/add-profile.html', {
                'form': form,
                'error': False
            })
    else:
        return redirect('coreapp:home')


def EditProfile(request):
    if request.user.is_authenticated and request.user.role == 'HOSPITAL':
        try:
            instance = request.user.hospital
            form = AddHospitalProfileForm(instance=instance)
            if request.method == "POST":
                form = AddHospitalProfileForm(
                    request.POST, request.FILES, instance=instance)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.location = request.POST['location']
                    post.save()
                    return redirect(reverse('hospital:hos_dashboard'))
                else:
                    return render(request, 'hospital/add-profile.html', {
                        'form': form,
                        'error': True,
                    })

            return render(request, 'hospital/add-profile.html', {
                'form': form,
                'error': False,
            })
        except ObjectDoesNotExist:
            return redirect('coreapp:home')


def AddDoctor(request):
    if request.user.is_authenticated and request.user.role == 'HOSPITAL':
        try:
            if request.method == "POST":
                form = DoctorForm(request.POST, request.FILES)
                if form.is_valid():
                    doctor = form.save(commit=False)
                    doctor.hospital = request.user.hospital
                    if 'pic' in request.FILES:
                        doctor.pic = request.FILES['pic']
                    doctor.save()
                    return redirect(reverse('hospital:hos_doctors'))
                else:
                    return render(request, 'hospital/add-doctor.html', {
                        'form': form,
                        'error': True,
                        'doctors': Doctor.objects.filter(hospital=request.user.hospital)
                    })

            form = DoctorForm()
            return render(request, 'hospital/add-doctor.html', {
                'form': form,
                'error': False,
                'doctors': Doctor.objects.filter(hospital=request.user.hospital)
            })
        except ObjectDoesNotExist:
            return redirect('hospital:hos_doctors')


def EditDoctor(request, doctor_id):
    if request.user.is_authenticated and request.user.role == 'HOSPITAL':
        doctor = get_object_or_404(Doctor, id=doctor_id)
        # populate with data in form for edit form
        form = DoctorForm(request.POST or None,request.FILES or None, instance=doctor)

        if request.method == "POST":

            if form.is_valid():

                doctor = form.save(commit=False)
                doctor.hospital = request.user.hospital
                if 'pic' in request.FILES:
                    doctor.pic = request.FILES.get('pic')
                doctor.save()

                return redirect(reverse('hospital:hos_doctors'))
            else:
                form = DoctorForm(request.POST or None,request.FILES or None, instance=doctor)
                return render(request, 'hospital/add-doctor.html', {
                    'form': form,
                    'error': True,
                })

        return render(request, 'hospital/add-doctor.html', {
            'form': form,
            'error': False,
        })
    else:
        return redirect('hospital:hos_doctors')


def DeleteDoctor(request, doctor_id):
    if request.user.is_authenticated and request.user.role == 'HOSPITAL':
        doctor = Doctor.objects.get(id=doctor_id)
        doctor.delete()
        context = {
            "message": "sucessfully deleted"
        }
        return redirect(reverse('hospital:hos_doctors'))


def DoctorProfile(request, doctor_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        appointments = Appointment.objects.filter(doctor=doctor)
        reviews = AppointmentReview.objects.filter(appointment__in=appointments)

         #Calculate the average doctor rating
        average_rating = reviews.aggregate(Avg('doctor_rating'))['doctor_rating__avg']  
        if average_rating is not None:
            converted_value = math.ceil(float(average_rating) * 10) / 2.0
        else:
            converted_value = 0.0
        
        # Limit the value between 1 and 5
        converted_value = min(5.0, max(1.0, converted_value)) #connverted b/w 1-5
        rat=int(converted_value) #removed the decimal part for star count
        star=range(rat) #set the range for no. of star loop
        
      
        if converted_value % 1 == 0:
            half = False
            
        else:
            half = True

    except Doctor.DoesNotExist:
        raise Http404("Doctor does not exist.")
    
    context = {
        "doctor": doctor,
        "reviews":reviews,
        'appointments':appointments,
        "average_rating": converted_value,
        'half': half,
        'star':star
    }

    return render(request, 'hospital/doctor-profile.html', context)


@login_required
def HosAppointmentsView(request):
    appointments = Appointment.objects.filter(hospital=request.user.hospital)

    cancelled_appoinments = appointments.filter(appointment_status='cancelled')
    completed_appoinments = appointments.filter(appointment_status='completed')
    pending_appoinments = appointments.filter(appointment_status='pending')
    return render(request, 'hospital/hos_appointments.html', {
        'cancelled_appointments': cancelled_appoinments,
        'completed_appointments': completed_appoinments,
        'pending_appointments': pending_appoinments
    })


@login_required
def HosAppointmentConfirmView(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)

        if request.method == 'POST' and request.POST.get('_method') != 'DELETE':
            appointment.appointment_status = 'completed'
            appointment.save()
            return redirect(reverse('hospital:hos_appointments'))

        if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
            appointment.appointment_status = 'cancelled'
            appointment.save()
            return redirect(reverse('hospital:hos_appointments'))

    except ObjectDoesNotExist:
        return HttpResponse("Appointment not found.")

    return HttpResponse("Invalid request.")
# def HosDoctorsView(request):
#     doctor = Doctor.objects.all().filter(hospital=request.user.hospital)
#     doctor_ratings = []
    
#     for doctor in doctor:
#         appointments = Appointment.objects.filter(doctor=doctor)
#         reviews = AppointmentReview.objects.filter(appointment__in=appointments)

#         # Calculate the average doctor rating
#         average_rating = reviews.aggregate(Avg('doctor_rating'))['doctor_rating__avg']
#         if average_rating is not None:
#             converted_value = math.ceil(float(average_rating) * 10) / 2.0
#         else:
#             converted_value = 0.0
        
#         # Limit the value between 1 and 5
#         converted_value = min(5.0, max(1.0, converted_value))
#         rat = converted_value

#         # Create a dictionary or a tuple with doctor and rating
#         doctor_rating = {
#             'doctor': doctor,
#             'rating': rat
#         }
#         doctor_ratings.append(doctor_rating)

#     context = {
#         "doctor_ratings": doctor_ratings
#     }

def HosDoctorsView(request):
    doctor = Doctor.objects.filter(hospital=request.user.hospital).annotate(
        average_rating=Avg('d_appointment__appointment_review__doctor_rating')
    )
    
    context = {
        "doctors": doctor
    }    
    return render(request, 'hospital/hos_doctors.html', context)


def AddFacility(request):
    form = FacilityForm(request.POST)
    
    if request.method == 'POST':
        if form.is_valid():
            facility = form.save(commit=False)
            facility.hospital = request.user.hospital
            facility.save()
            return redirect('hospital:hos_dashboard') 
        else:
            form = FacilityForm()
    return render(request, 'hospital/add-facility.html', {'form':form})

def DeleteFacility(request,facility_id):
    facility = Facility.objects.get(id=facility_id)
    facility.delete()
    messages.success(request, "Successfully deleted")
    return redirect(reverse('hospital:hos_dashboard'))


