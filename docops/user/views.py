from django.shortcuts import render,redirect,reverse
from coreapp.forms import MedicalForm
from . forms import SignupForm,LoginForm,HosLoginForm,HosSignupForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

User = get_user_model()

def HosSignup(request):
    form = HosSignupForm()
    if request.method == "POST":
        form = HosSignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                print('success')
                login(request, user)
                return redirect(reverse('hospital:add_profile'))
        else:
            return render(request, 'user/hospital/hos_signup.html', {
                'form': form,
                'error': True,
            })
    
    return render(request,'user/hospital/hos_signup.html',{
        'form': form,
        'error': False
    })

def HosLogin(request):
    if request.user.is_authenticated:
        return redirect(reverse('hospital:hos_dashboard'))

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)
 
        if user is not None:
            login(request,user)
            return redirect(reverse('hospital:hos_dashboard'))
        else:
            form = HosLoginForm()
            context = {
                'message':'invalid credential',
                'form':form
            }
            return render(request,'user/hospital/hos_login.html',context)
     
    else:
        form = HosLoginForm()
        return render(request, 'user/hospital/hos_login.html', {'form':form})
def HosLogout(request):
    logout(request)
    return redirect('user:hoslogin')  

def Signup(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                print('success')
                login(request, user)
                return redirect(reverse('coreapp:add_profile'))
        else:
            return render(request, 'user/patient/signup.html', {
                'form': form,
                'error': True,
            })
    
    return render(request,'user/patient/signup.html',{
        'form': form,
        'error': False
    })

def Login(request):
    if request.user.is_authenticated:
        print("-----------")
        return redirect(reverse('coreapp:home'))

    elif request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)
 
        if user is not None:
            login(request,user)
           
            return redirect(reverse('coreapp:home'))
        else:
            print("login error")
            form = LoginForm()
            return render(request,'user/patient/login.html',{'form':form})
     
    else:
        form = LoginForm()
        return render(request, 'user/patient/login.html', {'form':form})

def Logout(request):
    logout(request)
    return redirect(reverse('coreapp:home'))

