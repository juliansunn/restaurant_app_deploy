from restaurants.views import change_password, edit_profile
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt
from django.http import JsonResponse
from django.views.generic.edit import View

def index(request):
    return render(request, "index.html")

def validate_email(request):
    email = request.GET['email']
    data = {
        'found': User.objects.filter(email__iexact=email).exists(),
    }
    return JsonResponse(data)

def validate_username(request):
    username = request.GET['username']
    data = {
        'found': User.objects.filter(username__iexact=username).exists(),
    }
    return JsonResponse(data)


def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST, edit_profile=True, change_password=True)
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v, extra_tags=k)
            return redirect("/")
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], username=request.POST['username'], email=request.POST['email'], birthday=request.POST['birthday'], password=pw_hash)
        request.session['user_id'] = new_user.id
        return redirect("/dashboard")
    return redirect("/")
        

def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['login_email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['login_password'].encode(),logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect("/dashboard")
            messages.error(request, "Your password is incorrect", extra_tags="user_pw")
            return redirect("/")
        messages.error(request,'your email is not in our database.', extra_tags="user_em")
        return redirect("/")
    return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")




