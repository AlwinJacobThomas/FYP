from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import AddPatientProfileForm, AppointmentReviewForm, AppointmentBookingForm, MedicalForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from user.models import HospitalProfile, PatientProfile
from hospital.models import Doctor
from .models import Appointment, AppointmentReview, Medical
from django.http import HttpResponse
from django.db.models import Avg, Sum
from docops.lstm import analyze_sentiment
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import Http404
import math

# Create your views here.
User = get_user_model()


def home(request):
    if request.user.is_authenticated:
        if request.user.role == 'HOSPITAL':
            return redirect(reverse('hospital:hos_dashboard'))
        else:
            user = request.user
            medical = get_object_or_404(Medical, user=user.patient)
            context = {
            
                'user': user,
                'medical': medical
            }
            return render(request, 'coreapp/patient/dashboard.html', context)
    else:
        return redirect(reverse('user:signup'))


@login_required
def AddProfile(request):
    if request.user.is_authenticated and request.user.role == 'PATIENT':
            form = AddPatientProfileForm()
            if request.method == "POST":
                form = AddPatientProfileForm(request.POST, request.FILES)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.user = User.objects.get(id=request.user.id)

                    if 'pic' in request.FILES:
                        post.pic = request.FILES['pic']
                    post.save()
                    Medical.objects.create(user =request.user.patient)
                    return redirect(reverse('coreapp:home'))
            return render(request,'coreapp/patient/add-profile.html',{
                'form': form,
                'error': False
            })
    else:
        return redirect('coreapp:home')
    
# def EditProfile(request):
#     if request.user.is_authenticated and request.user.role == 'PATIENT':
#         try:
#             instance = request.user.patient
#             if request.method == "POST":
#                 form = AddPatientProfileForm(request.POST, request.FILES, instance=instance)
#                 if form.is_valid():
#                     profile = form.save(commit=False)
#                     if 'pic' in request.FILES:
#                         profile.pic = request.FILES['pic']
#                     profile.save()
#                     return redirect(reverse('coreapp:home'))
#             else:
#                 form = AddPatientProfileForm(instance=instance)

#             return render(request, 'coreapp/patient/add-profile.html', {
#                 'form': form,
#                 'error': False,
#             })
#         except ObjectDoesNotExist:
#             return redirect('coreapp:home')
#     else:
#         return redirect('coreapp:home')  
    
def EditProfile(request):
    if request.user.is_authenticated and request.user.role == 'PATIENT':
        
        instance = get_object_or_404(PatientProfile, patient_id=request.user.patient.patient_id)
        # populate with data in form for edit form
        form = AddPatientProfileForm(request.POST or None,
                          request.FILES or None, instance=instance)
        if request.method == "POST":
            if form.is_valid():
                post = form.save(commit=False)
                if 'pic' in request.FILES:
                    post.pic = request.FILES.get('pic')
                post.save()
                return redirect(reverse('coreapp:home'))
            else:
                form = AddPatientProfileForm(instance=instance)

        return render(request, 'coreapp/patient/add-profile.html', {
            'form': form,
            'error': False,
        })
    else:
        return redirect('coreapp:home') 
        
@login_required
def booking(request):
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        doctor_name = request.POST.get('doctor_name')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        appointment_status = request.POST.get('appointment_status')

        # Save the appointment to the database
        appointment = Appointment.objects.create(
            patient_name=patient_name,
            doctor_name=doctor_name,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            appointment_status=appointment_status
        )
        appointment.save()

        # Redirect to a success page or another URL
        return redirect('success')
    return render(request, 'coreapp/doc/booking.html')
  

@login_required
def doc_search(request):
    if request.user.is_authenticated and request.user.role == 'PATIENT':
        doctors = Doctor.objects.annotate(average_rating=Avg('d_appointment__appointment_review__doctor_rating')).order_by('-average_rating')
        



        context = {
            "doctors": doctors,
        }
        return render(request, 'coreapp/patient/doc-search.html', context)
    else:
        return HttpResponse("Unauthorized", status=401)

# @login_required
# def DoctorProfile(request,doctor_id):
#     doctor = Doctor.objects.get(id=doctor_id)
#     reviews = AppointmentReview.objects.filter(appointment__doctor=doctor)
#     # rating = reviews.aggregate(avg_rating=Avg('doctor_rating'))['avg_rating']
#     rating_sum = reviews.aggregate(sum_doctor_rating=Sum('doctor_rating'))['sum_doctor_rating']

#     print(rating_sum)

    # context = {
    #         "doctor":doctor,
    #         "reviews": reviews,
    #         "rating": rating_sum                          
    #     }
    # return render(request, 'coreapp/patient/doc-profile.html',context)

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

        print(average_rating)
        if converted_value % 1 == 0:
            half = False
            
        else:
            half = True

    except Doctor.DoesNotExist:
        raise Http404("Doctor does not exist.")

    patients = []
    for review in reviews:
        patient = review.appointment.patient
        patients.append((review, patient))

    context = {
        "doctor": doctor,
        "reviews": reviews,
        "appointments": appointments,
        "patients": patients,
        "average_rating": converted_value,
        'half': half,
        'star':star
    }

    return render(request, 'coreapp/patient/doc-profile.html', context)


@login_required
def hos_search(request):
    if request.user.is_authenticated and request.user.role == 'PATIENT':
        # hospitals = HospitalProfile.objects.all()
        hospitals = HospitalProfile.objects.annotate(average_rating=Avg('h_appointment__appointment_review__hospital_rating')).order_by('-average_rating')
        context = {
            "hospitals": hospitals,
        }
        return render(request, 'coreapp/patient/hos-search.html', context)
    else:
        return HttpResponse("Unauthorized", status=401)

def AddReview(request, doctor_id):
    if request.method == 'POST':
        form = AppointmentReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.doctor_id = doctor_id
            review.user = request.user
            review.save()
            return redirect('hospital:doctor_detail', doctor_id=doctor_id)  # Redirect to doctor detail page
    else:
        form = AppointmentReviewForm()
    
    return render(request, 'doc/add_review.html', {'form': form})


# @login_required
# def DoctorDetailView(request, doctor_id):
#     doctor = Doctor.objects.get(id=doctor_id)
#     return render(request, 'coreapp/patient/doctor_detail.html', {
#         'doctor': doctor,
#         'doctor_id': doctor_id
#     })

    
@login_required
def AppointmentBookingView(request, doctor_id):
    form = AppointmentBookingForm()
    doctor = Doctor.objects.get(id=doctor_id)
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.patient = PatientProfile.objects.get(user=request.user)
            appointment.hospital = doctor.hospital
            appointment.appointment_status = 'pending'
            appointment.save()
            return redirect(reverse('coreapp:appointments'))
        else:
            return HttpResponse("Invalid data", status=401)
    else:
        return render(request, 'coreapp/patient/appointment_booking.html', {
            'form': AppointmentBookingForm(),
            'doctor_id': doctor_id
        })

@login_required
def AppointmentsView(request):     #appointment tab     
                                
    reviewed_appointments = Appointment.objects.filter(patient=request.user.patient, appointment_status='completed',appointment_review__isnull=False).order_by('appointment_date','appointment_time')
    not_reviewed_appointments = Appointment.objects.filter(appointment_status='completed',patient=request.user.patient,appointment_review__isnull=True).order_by('appointment_date','appointment_time')
    
    completed = {
        'reviewed': reviewed_appointments,
        'not_reviewed': not_reviewed_appointments
    }

    context =  {
        'pending': Appointment.objects.filter(appointment_status='pending',patient=request.user.patient).order_by('appointment_date','appointment_time'),
        'cancelled': Appointment.objects.filter(appointment_status='cancelled',patient=request.user.patient).order_by('appointment_date','appointment_time'),
        'completed': completed,
    }
    
    return render(request, 'coreapp/patient/appointment-tab.html',context )


@login_required
def TreatmentReviewView(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)

    reviewed_appointments = Appointment.objects.filter(patient=request.user.patient,appointment_status='completed',appointment_review__isnull=False)
    
    if appointment.appointment_status == 'completed' and appointment not in reviewed_appointments:
        if request.method == 'POST':
            hos_review = request.POST.get('hos_review')
            doc_review = request.POST.get('doc_review')

            hos_rating = analyze_sentiment(hos_review)
            doc_rating = analyze_sentiment(doc_review)
            
            appointmentReview = AppointmentReview(
                hospital_review = hos_review,
                hospital_rating = float(hos_rating),
                doctor_review = doc_review,
                doctor_rating = float(doc_rating),
                appointment = appointment
            )
            
            print(f'------{hos_rating}---{doc_rating}')
            appointmentReview.save()
            return redirect(reverse('coreapp:doc_profile', kwargs={'doctor_id': appointment.doctor.id}))
        return render(request, 'coreapp/patient/treatment_review.html', {
            'appointment_id': appointment_id,
            'doctor_id': appointment.doctor.id
        })
    else:
        return HttpResponse("Error", status=401)

@login_required
def HosProfile(request, hospital_id):
    hospital = HospitalProfile.objects.get(hospital_id=hospital_id)
    
    appointments = Appointment.objects.filter(hospital=hospital)
    reviews = AppointmentReview.objects.filter(appointment__in=appointments)
    average_rating = reviews.aggregate(Avg('hospital_rating'))['hospital_rating__avg']  
        

    if average_rating is not None:
        converted_value = math.ceil(float(average_rating) * 10) / 2.0
    else:
        converted_value = 0.0
    
    

    # Limit the value between 1 and 5
    converted_value = min(5.0, max(1.0, converted_value)) #connverted b/w 1-5
    
    rat=int(converted_value) #removed the decimal part for star count
    star=range(rat) #set the range for no. of star loop

    print(average_rating)
    if converted_value % 1 == 0:
        half = False
        
    else:
        half = True

    reviews = AppointmentReview.objects.filter(appointment__hospital=hospital)
    return render(request, 'coreapp/patient/hos-profile.html', {
        'hospital': hospital,
        'reviews':reviews,
        'rat':rat,
        'avg':average_rating,
        'star':star
    })

@login_required
def AppointmentConfirm(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        if request.method == 'POST' and request.POST.get('_method') != 'DELETE':
            appointment.appointment_status = 'completed'
            appointment.save()
            return HttpResponse("Appointment marked as completed.")
        
        if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
            appointment.appointment_status = 'cancelled'
            appointment.save()
            return redirect(reverse('coreapp:appointments'))

    except ObjectDoesNotExist:
        return HttpResponse("Appointment not found.")
    
    return HttpResponse("Invalid request.")

def AddMedical(request):
    try:
        medical = get_object_or_404(Medical, user=request.user.patient)
        
    except ObjectDoesNotExist:
        medical = None
    form = MedicalForm(instance=medical)    
    if request.method == 'POST':
        form = MedicalForm(request.POST,instance=medical)
        if form.is_valid():
            a = form.save(commit=False)
            a.user = request.user.patient
            a.save()
            return redirect('coreapp:home') 
        else:
            form = MedicalForm()
    return render(request, 'coreapp/patient/add-medical.html', {'form':form,"medical":medical})
   