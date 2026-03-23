from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import ProfileForm
from payments.models import *

import logging
logger=logging.getLogger('django')


# Create your views here.
def log_in(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        remember_me=request.POST.get('remember_me')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            if remember_me:
                request.session.set_expiry(120000)
            else:
                request.session.set_expiry(0)
            next=request.POST.get('next')
            return redirect(next if next else 'home')

        else:
            messages.error(request,'Invalid password!!!!!!!!!!!!')
            return redirect('login')
    next=request.GET.get("next",'')
    return render(request,'accounts/login.html',{'next':next})




def register(request):
    if request.method == "POST":
        fname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        # password match check
        if password != password1:
            messages.error(request, 'Password and confirm password are not same')
            return redirect('register')

        # username check
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        # email check
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')
        # password uppercase check
        if not re.search(r"[A-Z]", password):
            messages.error(request, 'Password must contain at least one uppercase letter')
            return redirect('register')

        # password digit check
        if not re.search(r'\d', password):
            messages.error(request, 'Password must contain at least one digit')
            return redirect('register')

        # Django password validation
        try:
            validate_password(password)
        except ValidationError as e:
            for msg in e.messages:
                messages.error(request, msg)
            return redirect('register')

        # create user
        CustomUser.objects.create_user(
            first_name=fname,
            last_name=lastname,
            username=username,
            email=email,
            password=password
        )

        messages.success(request, 'Account created successfully')
        return redirect('register')

    # GET request
    return render(request, 'accounts/register.html')


def log_out(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def change(request):
    form=PasswordChangeForm(user=request.user)
    if request.method=='POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request,'accounts/change.html',{'form':form})



@login_required(login_url='login')
def profile_dashboard(request):
    return render(request,'profile/dashboard.html')


@login_required(login_url='login')
def profile(request):
    profile,created=Profile.objects.get_or_create(user=request.user)
    form=ProfileForm(instance=profile)
    if request.method=='POST':
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile updated successfully')
            return redirect('profile')
    context={
            'form':form
            }
    return render(request,'profile/profile.html',context)


@login_required(login_url='login')
def my_orders(request):
    orders=Order.objects.filter(user=request.user)
    return render(request,'profile/my_order.html',{'orders':orders})