# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from app.models import *
import os
# Create your views here.

def index(request):
    return render(request, "index.html", {"key": "11111111111111"})


def plateform(request):
    if not User.objects.exists():
        User(username="admin").save()
    user = User.objects.get(username="admin")

    # print(user.id)
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

def suite_list(request):
    error = None
    suites = None
    if request.method == "POST":
        p_name = request.POST['name']
        p_description = request.POST['description']
        if p_name == "" or p_description == "":
            error = "数据不能为空"
        else:
            Suite(name=p_name, description=p_description).save()

    if Suite.objects.exists():
        suites = Suite.objects.all()

    return render(request, "suite.html", {"suites": suites, "error": error})

def case_list(request):
    error = None
    cases = None
    if request.method == "POST":
        p_name = request.POST['name']
        p_level = request.POST['level']
        p_suite = request.POST['suite']
        p_command = request.POST['command']
        p_param = request.POST['param']
        p_description = request.POST['description']
        if p_name == "" or p_command == "" or p_param == "" or p_description == "":
            error = "数据不能为空"
        else:
            Case(name=p_name, suite=Suite.objects.get(id=p_suite),  level=p_level, command=p_command, param=p_param, description=p_description).save()
            #根据数据库信息生成新的xml

            #保存xml到本地路径
    if Case.objects.exists():
        cases = Case.objects.all()
    suites = Suite.objects.all()
    return render(request, "case.html", {"cases": cases, "error": error, "suites": suites})

def case_delete(request, pk):
    cases = None
    Case.objects.get(id=pk).delete()
    if Case.objects.exists():
        cases = Case.objects.all()
    return render(request, "case.html", {"cases": cases})

def script_list(request):
    script_path = settings.MEDIA_ROOT + "/script/"
    if request.method == "POST":
        file = request.FILES['name']
        open(script_path + file.name, 'wb').write(file.read())

    scripts = os.listdir(script_path)
    return render(request, "script.html", {"scripts": scripts})

def script_show(request):
    g_name = request.GET['name']
    script_path = settings.MEDIA_ROOT + "/script/"

    name = script_path + g_name

    if os.path.isdir(name):
        scripts = os.listdir(name)
        return render(request, "script.html", {"scripts": scripts})
    else:
        try:
            script = open(name)
            script_text = script.read()
        finally:
            script.close()
        return render(request, "script_show.html", {"script_text": script_text})
