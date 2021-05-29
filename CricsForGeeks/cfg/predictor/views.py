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
from . import predicter
# Create your views here.


def home(request):
    return render(request, 'predictor/home.html')


def stats(request):
    teamA = []
    teamB = []
    context = {}
    if request.method == "POST":
        alen = int(request.POST["teamAL"])
        blen = int(request.POST["teamBL"])

        for i in range(alen):
            teamA.append(request.POST["teamA"+str(i)])
        for i in range(blen):
            teamB.append(request.POST["teamB"+str(i)])

        final_batsman_a_stats, final_bowler_a_stats, final_batsman_b_stats, final_bowler_b_stats, total_a, total_b = predicter.get_prediction(
            teamA, teamB)

        context = {"bat_a": {i: final_batsman_a_stats[i] for i in sorted(final_batsman_a_stats.keys(), key=final_batsman_a_stats.get, reverse=True)},
                   "bat_b": {i: final_batsman_b_stats[i] for i in sorted(final_batsman_b_stats.keys(), key=final_batsman_b_stats.get, reverse=True)},
                   "bowl_a": {i: [final_bowler_a_stats[i][0], final_bowler_a_stats[i][1]//6] for i in sorted(final_bowler_a_stats.keys(), key=final_bowler_a_stats.get, reverse=True)},
                   "bowl_b": {i: [final_bowler_b_stats[i][0], final_bowler_b_stats[i][1]//6] for i in sorted(final_bowler_b_stats.keys(), key=final_bowler_b_stats.get, reverse=True)},
                   "total_a": total_a,
                   "total_b": total_b
                   }

        # print(context)
        # print('Batsman Team A')
        # for i in final_batsman_a_stats:
        #     print(i, final_batsman_a_stats[i][0],
        #           'in', final_batsman_a_stats[i][1])
        # print('Total =', sum(i[0] for i in final_batsman_a_stats.values()))
        # print('Bowlers Team B')
        # for i in final_bowler_b_stats:
        #     print(i, final_bowler_b_stats[i][0], 'conceded in',
        #           final_bowler_b_stats[i][1]//6, 'overs')
        # print('*'*100)
        # print('Batsman Team B')
        # for i in final_batsman_b_stats:
        #     print(i, final_batsman_b_stats[i][0],
        #           'in', final_batsman_b_stats[i][1])
        # print('Bowlers Team A')
        # for i in final_bowler_a_stats:
        #     print(i, final_bowler_a_stats[i][0], 'conceded in',
        #           final_bowler_a_stats[i][1]//6, 'overs')
        # print('Total =', sum(i[0] for i in final_batsman_b_stats.values()))
    return render(request, "predictor/stats.html", context)


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


def rules(request):
    return render(request, "predictor/rules.html")
