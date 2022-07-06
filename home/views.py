
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login as auth_login
from .models import *
import uuid
from email import message    
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
import math
from django.core.mail import send_mail
# Create your views here.


def home(request):
    return render(request, 'index.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("Phone")
        desc = request.POST.get("desc")
        print(name,email,phone,desc)
        instance = Contact(name=name, email=email, phone=phone, desc=desc)
        instance.save()
    return render(request, 'index.html')


def login(request):
    return render(request,'login.html')

def signup(request):
    return render(request,'sign.html')

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        passw = request.POST['pass1']
        passw2 = request.POST['pass2']
        father_name = request.POST['father_name']
        classes=request.POST['class_name']
        Uname = request.POST['roll_no']
        print(name,email,passw)
        if passw != passw2:
            return HttpResponse('Both Passward are not same')

        try:
            if User.objects.filter(username=Uname).first():
                messages.success(request, 'Username is taken.')
                return HttpResponse('Both  Username is taken')

            if User.objects.filter(email=email).first():
                messages.success(request, 'Email is taken.')
                return HttpResponse('Both email is taken')

            user_obj = User(username=Uname, email=email)
            user_obj.set_password(passw)
            user_obj.save()

            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(
                user=user_obj, auth_token=auth_token, Name=name, fathers_Name=father_name, Email_id=email,Classes=classes)
            profile_obj.save()
            print("here we are")
            check_mail = send_mail_after_registration(email, auth_token)
            print(check_mail)
            return render(request, 'mess.html')

        except Exception as e:
            print(e)
            # return HttpResponse('sucessfully submited with error')
    else:
        return HttpResponse('404-Error')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('home')
            profile_obj.is_verified = True
            profile_obj.save()
            return render(request,'login.html')
        else:
            return HttpResponse('Error')
    except Exception as e:
        print(e)
        return redirect('/')



def handlelogin(request):

    if request.method == 'POST':
        username = request.POST.get('loginuname')
        password = request.POST.get('loginpass')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return render(request,'index.html')

        profile_obj = Profile.objects.filter(user=user_obj).first()

        if not profile_obj.is_verified:
            messages.success(
                request, 'Profile is not verified check your mail.')
            return render(request,'login.html')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return render(request,'login.html')

        login(request)
        NAME=profile_obj.Name
        Roll_No= profile_obj.user
        Father_name =profile_obj.fathers_Name
        Email_id=profile_obj.Email_id
        CLASSS=profile_obj.Classes
        DUES =profile_obj.Dues
        message=profile_obj.message
       
        # print(NAME,Roll_No,Father_name,Email_id)

        context = {'name': NAME,'Roll':Roll_No ,'Father_name':Father_name, 'Email':Email_id, 'CLASSS':CLASSS,'DUES':DUES,'message':message }


        return render(request,'user.html',context)

    return render(request, 'login.html')

def send_mail_after_registration(email, token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    return send_mail(subject, message, email_from, recipient_list)


def forgetpass(request):
    return render(request,'forget.html')


def reset(request):
    if request.method == 'POST':
        username=request.POST['loginuname']
        
        try:
            if User.objects.filter(username=username).first():
                obj=User.objects.filter(username=username).first()
                email=obj.email
                print(obj)
                print(email) 
                auth_token = str(uuid.uuid4())
                profile_obj= Profile.objects.filter(user=obj).first()
                profile_obj.auth_token=auth_token
                profile_obj.save()

                check=send_mail_after_forget(email, auth_token)
                # print(check)
                return render(request,'mess.html')

            return redirect('forget')    
            
           

        except Exception as e:
            print(e)

    else:
        return redirect('reset')


def send_mail_after_forget(email, token):
    subject = 'Reset Your password'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/changepass/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    return send_mail(subject, message, email_from, recipient_list)



def changepass(request,auth_token):
    context = {}
    
    
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        context = {'user_id' : profile_obj.user.username}
        
        if request.method == 'POST':
            new_password = request.POST.get('pass1')
            confirm_password = request.POST.get('pass2')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'/changepass/{auth_token}/')
                
            
            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/changepass/{auth_token}/')
                         
            
            user_obj = User.objects.get(username = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('login')
        
    except Exception as e:
        print(e)
    return render(request,'changepassword.html',context)


def blog(request):
    no_of_post = 4
    page_no = request.GET.get('page')

    if page_no is None:
        page_no = 1
    else:
        page_no = int(page_no)

    print(page_no)
    blogs = Blog.objects.all()
    blogs.reverse()
    length = len(blogs)

    # blogs = Blog.objects.all()[(page_no-1)*no_of_post: page_no*no_of_post]

    if page_no > 1:
        prev = page_no-1
    else:
        prev = None

    if page_no < math.ceil(length/no_of_post):
        nxt = page_no+1
    else:
        nxt = None

    context = {'blogs': blogs, 'prev': prev, 'nxt': nxt}
    return render(request, 'bloghome.html', context)

def blogpost(request, slug):
    blog = Blog.objects.filter(slug=slug).first()
    context = {'blog': blog}
    return render(request, 'blogpost.html', context)