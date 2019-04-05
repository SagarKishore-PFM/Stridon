from django.shortcuts import render, redirect
from nucypher_utils.alice import run
from nucypher_utils.doctor import run_doc
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def home(request):
    return render(request, 'stridon_app/home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'stridon_app/signup.html', {'form': form})


def alice(request):
    run()
    return render(request, 'stridon_app/alice.html')


def doctor(request):
    run_doc()
    return render(request, 'stridon_app/doctor.html')