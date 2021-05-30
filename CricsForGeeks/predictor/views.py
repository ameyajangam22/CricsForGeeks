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


def teamvteam(request):
    return render(request, 'predictor/teamVteam.html')


def stats(request):
    teamA = []
    teamB = []
    context = {}
    if request.method == "POST":
        if request.POST["teamAL"] == 1 and request.POST["teamBL"] == 1:

            alen = int(request.POST["teamAL"])
            blen = int(request.POST["teamBL"])

            for i in range(alen):
                teamA = (request.POST["teamA"+str(i)])
            for i in range(blen):
                teamB = (request.POST["teamB"+str(i)])

            final_batsman_a_stats, final_bowler_a_stats, final_batsman_b_stats, final_bowler_b_stats, total_a, total_b = predicter.get_prediction(
                teamA, teamB)

            context = {"bat_a": {i: final_batsman_a_stats[i] for i in sorted(final_batsman_a_stats.keys(), key=final_batsman_a_stats.get, reverse=True)},
                       "bat_b": {i: final_batsman_b_stats[i] for i in sorted(final_batsman_b_stats.keys(), key=final_batsman_b_stats.get, reverse=True)},
                       "bowl_a": {i: [final_bowler_a_stats[i][0], final_bowler_a_stats[i][1]//6] for i in sorted(final_bowler_a_stats.keys(), key=final_bowler_a_stats.get, reverse=True)},
                       "bowl_b": {i: [final_bowler_b_stats[i][0], final_bowler_b_stats[i][1]//6] for i in sorted(final_bowler_b_stats.keys(), key=final_bowler_b_stats.get, reverse=True)},
                       "total_a": total_a,
                       "total_b": total_b,
                       "teamA_name": "Team A",
                       "teamB_name": "Team B"
                       }
        else:
            alen = int(request.POST["teamAL"])
            blen = int(request.POST["teamBL"])

            for i in range(alen):
                teamA_name = (request.POST["teamA"])
            for i in range(blen):
                teamB_name = (request.POST["teamB"])
            MI = ['RG Sharma', 'Q de Kock', 'HH Pandya',
                  'J Yadav', 'TA Boult', 'KH Pandya', 'JJ Bumrah', 'Ishan Kishan', 'KA Pollard', 'RD Chahar', 'SA Yadav']
            # 5 not in playing 11
            RCB = ['V Kohli', 'GJ Maxwell', 'AB de Villiers',
                   'Washington Sundar', 'HV Patel', 'YS Chahal', 'Mohammed Siraj', 'DT Christian', 'KW Richardson', 'Sachin Baby', 'S Kuggeleijn']
            RR = ['JC Buttler', 'SV Samson', 'S Dube',
                  'DA Miller', 'R Parag', 'R Tewatia', 'CH Morris', 'S Gopal', 'Mustafizur Rahman', 'JD Unadkat', 'Kuldeep Yadav']
            CSK = ['F du Plessis', 'SK Raina', 'M Ali',
                   'AT Rayudu', 'RA Jadeja', 'MS Dhoni', 'S Curran', 'L Ngidi', 'DL Chahar', 'SN Thakur', 'DJ Bravo']

            PBKS = ['KL Rahul', 'MA Agarwal', 'CH Gayle',
                    'N Pooran', 'DJ Hooda', 'MC Henriques', 'Mohammed Shami', 'A Singh', 'R Bishnoi', 'CJ Jordan', 'M Ashwin']

            KKR = ['N Rana', 'S Gill', 'RA Tripathi',
                   'EJG Morgan', 'KD Karthik', 'SP Narine', 'AD Russell', 'PJ Cummins', 'V Chakravarthy', 'S Mavi', 'Shakib Al Hasan']
            DC = ['P Shaw', 'S Dhawan', 'RR Pant', 'SPD Smith',
                  'S Hetmyer', 'MP Stoinis', 'K Rabada', 'I Sharma', 'AR Patel', 'A Mishra', 'Avesh Khan']
            SRH = ['DA Warner', 'J Bairstow', 'KS Williamson',
                   'MK Pandey', 'KM Jadhav', 'V Shankar', 'Rashid Khan', 'J Suchith', 'Sandeep Sharma', 'K Ahmed', 'S Kaul  ']

            teams = {"Chennai Super Kings": CSK,
                     "Delhi Capitals": DC,
                     "Kolkata Night Riders": KKR,
                     "Mumbai Indians": MI,
                     "Punjab Kings": PBKS,
                     "Rajasthan Royals": RR,
                     "Royal Challenges Bangalore": RCB,
                     "Sunrisers Hyderabad": SRH}
            final_batsman_a_stats, final_bowler_a_stats, final_batsman_b_stats, final_bowler_b_stats, total_a, total_b = predicter.get_prediction(
                teams[teamA_name], teams[teamB_name])
            team_short = {"Chennai Super Kings": "CSK",
                          "Delhi Capitals": "DC",
                          "Kolkata Night Riders": "KKR",
                          "Mumbai Indians": "MI",
                          "Punjab Kings": "PBKS",
                          "Rajasthan Royals": "RR",
                          "Royal Challenges Bangalore": "RCB",
                          "Sunrisers Hyderabad": "SRH"}
            context = {"bat_a": {i: final_batsman_a_stats[i] for i in sorted(final_batsman_a_stats.keys(), key=final_batsman_a_stats.get, reverse=True)},
                       "bat_b": {i: final_batsman_b_stats[i] for i in sorted(final_batsman_b_stats.keys(), key=final_batsman_b_stats.get, reverse=True)},
                       "bowl_a": {i: [final_bowler_a_stats[i][0], final_bowler_a_stats[i][1]//6] for i in sorted(final_bowler_a_stats.keys(), key=final_bowler_a_stats.get, reverse=True)},
                       "bowl_b": {i: [final_bowler_b_stats[i][0], final_bowler_b_stats[i][1]//6] for i in sorted(final_bowler_b_stats.keys(), key=final_bowler_b_stats.get, reverse=True)},
                       "total_a": total_a,
                       "total_b": total_b,
                       "teamA_name": team_short[teamA_name],
                       "teamB_name": team_short[teamB_name]
                       }

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
