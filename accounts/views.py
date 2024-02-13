from django.shortcuts import render, HttpResponse, get_object_or_404
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth import login, authenticate, logout
from . models import Profile
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib import messages

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse("Logged in")
        else:
            return HttpResponse("User not found")
    else:
        form = LoginForm()
    return render(request, 'login.html', context={
        'form':form
    })

def logout_user(request):
    logout(request)
    return HttpResponse("Logged out")

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            new_user = form.save(commit=False)
            new_user.set_password(cd['password'])
            new_user.save()
            return render(request, 'registration/registration_done.html')
    else:
        form = UserRegistrationForm()
        
    return render(request, 'registration/register.html', {
        'user_form': form
        })

def profile(request):
    profile = get_object_or_404(Profile, user__username=request.user)
    user =  get_object_or_404(User, username=request.user)
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST) 
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile saved successfully')
            profile = get_object_or_404(Profile, user__username=request.user)
    else:
        user_form = UserEditForm(initial=model_to_dict(user))
        profile_form = ProfileEditForm(initial=model_to_dict(profile))
    return render(request, 'profile.html', {
        'profile': profile,
        'user_form': user_form,
        'profile_form': profile_form,
    })