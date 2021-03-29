from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
urlpatterns = [
    # path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("teamchoice/", views.teamchoice, name="teamchoice"),
    path("teamoption/", views.teamoption, name="teamoption"),
]
