from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from users.form import SignUpForm
from django.contrib.auth import login, logout
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
import random
import string

from users.models import CustomUser


def generate_code():
    return "".join(random.choices(string.digits + string.ascii_letters, k=6))

def LoginView(request):
    if request.method =='POST':
        date = request.POST
        user = CustomUser.objects.filter(email=date['username'])
        if len(user) == 1:
            user = user[0]
            if user.password == date["password"]:
                login(request, user)
                return redirect('home')
            messages.error(request, "Parol Noto'g'ri")
        else:
            messages.error(request, "Email yoki Parol xato!")
    return render(request, 'login.html')

def SignUpView(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save(commit=False)
            code = generate_code()
            user.is_active = False
            user.confirm_email = code
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account for ' + current_site.domain
            message = f"Your account has been activated code:  {code}"
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect('confirm_code', user.uniq_id)
    return render(request, 'signup.html', {"form": form})


def ConfirmEmailView(request, uniq_id):
    if request.method == 'POST':
        user = CustomUser.objects.get(uniq_id=uniq_id)
        user_confirm = request.POST.get('code', None)
        if user.confirm_email == user_confirm:
            user.is_active = True
            user.save()
            return redirect('home')
        messages.error(request, "Tasdiqlash kodi Xato!")
    return render(request, 'confirm_email.html')


def ProfileView(request, uniq_id):
    user = CustomUser.objects.get(uniq_id=uniq_id)
    context = {
        "profile": user
    }
    return render(request, 'profile.html', context)


def LogoutView(request, uniq_id):
    user = CustomUser.objects.filter(uniq_id=uniq_id)
    if len(user) == 1:
        user = user[0]
        logout(request)
        return redirect('home')
    messages.error(request, "Xatolik User tomilmadi.")
    return redirect('home')