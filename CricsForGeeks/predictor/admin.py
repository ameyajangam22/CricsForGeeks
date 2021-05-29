from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *
# Register your models here.


class BlogAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['Player_Name', 'DOB',
                    'Batting_Hand', 'Bowling_Skill', 'Country']


admin.site.register(Player, BlogAdmin)
