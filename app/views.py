from django.shortcuts import render
from app.models import *
# Create your views here.

def index(request):
    return render(request, "index.html", {"key": "11111111111111"})


def plateform(request):

    if not User.objects.exists():
        User(username="bittoy").save()
    user = User.objects.get(username="bittoy")

    #print(user.id)
    if not Plateform.objects.exists():
        Plateform(userId=user, name="cdos1.1", description="description1.1").save()
        Plateform(userId=user, name="cdos1.2", description="description1.2").save()
        Plateform(userId=user, name="cdos1.3", description="description1.3").save()
    plateforms = Plateform.objects.all()

    return render(request, "plateform.html", {"key": "11111111111111", "plateforms": plateforms})


def project(request):
    return render(request, "project.html", {"key": "11111111111111"})


def project_group(request):
    return render(request, "project_group.html", {"key": "11111111111111"})


def case(request):
    return render(request, "case.html", {"key": "11111111111111"})