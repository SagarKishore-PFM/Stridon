from django.shortcuts import render, redirect
from nucypher_utils.alice import run
from nucypher_utils.doctor import run_doc
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
@login_required(login_url='/login/')
def home(request):
    stridon_user = None
    if request.user.is_authenticated:
        stridon_user = request.user
    context = {
        'stridon_user': stridon_user,
    }
    return render(request, 'stridon_app/home.html', context=context)


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


@login_required(login_url='/login/')
def subscribe(request):
    paid_user_group = Group.objects.get(name='Paid Users Group')
    stridon_user = None
    if request.user.is_authenticated:
        stridon_user = request.user
    paid_user_group.user_set.add(stridon_user)
    paid_user_group.save()
    stridon_user.save()
    context = {
        'stridon_user': stridon_user,
        'paid_group': paid_user_group,
    }
    return render(request, 'stridon_app/subscribe.html', context=context)


def alice(request):
    run()
    return render(request, 'stridon_app/alice.html')


def doctor(request):
    run_doc()
    return render(request, 'stridon_app/doctor.html')
