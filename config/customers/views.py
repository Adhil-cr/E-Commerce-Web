from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Customer
from django.contrib import messages
from .forms import CustomerForm,UserRegisterForm

# Create your views here.

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

def login(request):
    return render(request,'customers/login.html')