# Generated by Django 3.1.7 on 2021-03-28 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0002_auto_20210328_1904'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='bat_hand',
            new_name='Batting_Hand',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='bowl_skill',
            new_name='Bowling_Skill',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='country',
            new_name='Country',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='dob',
            new_name='DOB',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='name',
            new_name='Player_Name',
        ),
    ]