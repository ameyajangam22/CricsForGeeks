from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from predictor.models import *
# from predictor.forms import *
from django.forms import inlineformset_factory
# from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
# Create your views here.


def home(request):
    return render(request, 'predictor/home.html')


def teamchoice(request):
    if 'term' in request.GET:
        qs = Player.objects.filter(
            Player_Name__icontains=request.GET.get('term'))
        names = list()
        for player in qs:
            names.append(player.Player_Name)
        return JsonResponse(names, safe=False)
    return render(request, 'predictor/teamchoice.html')


def teamoption(request):
    return render(request, 'predictor/teamoption.html')
