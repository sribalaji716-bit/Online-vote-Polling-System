from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import CustomUserForm
from voting.forms import VoterForm
from voting.models import Voter
# Create your views here.


def account_login(request):
    if request.user.is_authenticated:
        if str(request.user.user_type) == '1':
            return redirect(reverse("adminDashboard"))
        return redirect(reverse("voterDashboard"))

    next_url = request.POST.get('next') or request.GET.get('next') or ''
    context = {'next': next_url}

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if str(user.user_type) == '1':
                return redirect(reverse("adminDashboard"))

            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                return redirect(next_url)
            return redirect(reverse("voterDashboard"))

        messages.error(request, "Invalid email or password")
        context['email'] = email

    return render(request, "voting/login.html", context)


def account_register(request):
    userForm = CustomUserForm(request.POST or None)
    voterForm = VoterForm(request.POST or None)
    context = {
        'form1': userForm,
        'form2': voterForm
    }
    if request.method == 'POST':
        if userForm.is_valid() and voterForm.is_valid():
            user = userForm.save(commit=False)
            user.user_type = "2"
            user.save()
            voter = voterForm.save(commit=False)
            voter.admin = user
            voter.save()
            # Auto-login after successful registration
            login(request, user)
            messages.success(request, "Account created and logged in successfully!")
            return redirect(reverse('voterDashboard'))
        else:
            messages.error(request, "Provided data failed validation")
    return render(request, "voting/reg.html", context)


def account_logout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        messages.success(request, "Thank you for visiting us!")
    else:
        messages.error(
            request, "You need to be logged in to perform this action")

    return redirect(reverse("account_login"))
