from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Customer
from django.contrib import messages
from .forms import CustomerForm,UserRegisterForm,LoginForm
from django.contrib.auth import login,authenticate
from django.contrib.auth import logout


# Create your views here.
def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request,user)
                messages.success(request,"Login Successful!")
                return redirect('home')
            else:
                messages.error(request,"Invalide email or password")
                return redirect('login')
    else:
        form = LoginForm()

    
    return render(request,'customers/login.html',{'form':form})



def signup(request):
    if request.method == "POST":
        uform = UserRegisterForm(request.POST)
        cform = CustomerForm(request.POST)

        if uform.is_valid() and cform.is_valid():
            email = uform.cleaned_data['email']
            password = uform.cleaned_data['password']
            confirm_password = uform.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.error(request,'Password do not match')
                return redirect('signup')
            
            if User.objects.filter(username=email).exists():
                messages.error(request,'Email already exists')
                return redirect('signup')
            
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )

            customer = cform.save(commit=False)
            customer.user = user
            customer.save()

            messages.success(request,"Account created successfully!")
            return redirect('login')
        
    else:
        uform = UserRegisterForm()
        cform = CustomerForm()


    return render(request,'customers/signup.html',{
        'uform':uform,
        'cform':cform
    })

def logout_page(request):
    logout(request)
    return redirect('login') 
