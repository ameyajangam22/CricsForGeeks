from django.db import models

# Create your models here.


class Player(models.Model):
    Player_Name = models.CharField(max_length=200, null=True)
    DOB = models.CharField(max_length=200, null=True)
    Batting_Hand = models.CharField(max_length=200, null=True)
    Bowling_Skill = models.CharField(max_length=200, null=True)
    Country = models.CharField(max_length=200, null=True)
