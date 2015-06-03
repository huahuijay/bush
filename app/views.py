# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils.timezone import now
from app.models import *

from utils import generate_xml
from staf_wrapper.wrapper_STAF import STAFWrapper
import os
import threading
import time

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect(reverse("case_list"))
        else:
            return render(request, "login.html")
    else:
        return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect(reverse("case_list"))

def suite_list(request):
    error = None
    suites = None
    if request.method == "POST":
        p_name = request.POST['name']
        p_description = request.POST['description']
        if p_name == "" or p_description == "":
            error = "数据不能为空"
        else:
            Suite(name=p_name, description=p_description, createdAt=now()).save()
            script_path = settings.MEDIA_ROOT + settings.SCRIPT_DIR + p_name
            if not os.path.isdir(script_path):
                os.mkdir(script_path)
    if Suite.objects.exists():
        suites = Suite.objects.all()

    return render(request, "suite.html", locals())

def suite_view(request, pk):
    p_suite = Suite.objects.get(id=pk)
    cases = Case.objects.filter(suite=p_suite)
    tasks = Task.objects.filter(suite=p_suite)
    script_path = settings.MEDIA_ROOT + settings.SCRIPT_DIR + p_suite.name
    scripts = os.listdir(script_path)
    return render(request, "suite_view.html", locals())

def case_list(request):
    active = "case"
    error = None
    cases = None
    if request.method == "POST":
        p_name = request.POST['name']
        p_level = request.POST['level']
        p_suite = request.POST['suite']
        p_command = request.POST['command']
        p_param = request.POST['param']
        p_description = request.POST['description']
        if p_name == "" or p_command == "" or p_description == "":
            error = "数据不能为空"
        else:
            Case(name=p_name, suite=Suite.objects.get(id=p_suite),  level=p_level, command=p_command, param=p_param, description=p_description, createdAt=now()).save()

    if Case.objects.exists():
        cases = Case.objects.all()
    suites = Suite.objects.all()
    return render(request, "case.html", locals())

def case_view(request, pk):
    case = Case.objects.get(id=pk)
    return render(request, "case_view.html", locals())

def case_delete(request, pk):
    Case.objects.get(id=pk).delete()
    return redirect(reverse("case_list"))

def case_edit(request, pk):
    #Case.objects.get(id=pk).delete()
    case = Case.objects.get(id=pk)
    if request.method == "POST":
        p_name = request.POST['name']
        p_level = request.POST['level']
        p_command = request.POST['command']
        p_param = request.POST['param']
        p_description = request.POST['description']
        if p_name == "" or p_command == "" or p_description == "":
            error = "数据不能为空"
        else:
            case.name = p_name
            case.level = p_level
            case.command = p_command
            case.param = p_param
            case.description = p_description
            case.modifyAt = now()
            case.save()
            return redirect(reverse("case_view", kwargs={"pk": pk}))

    return render(request, "case_edit.html", locals())

def task_list(request):
    tasks = Task.objects.all()
    suites = Suite.objects.all()
    active = 'task'

    if request.method == "POST":
        p_name = request.POST['name']
        p_suite = request.POST['suite']
        p_description = request.POST['description']
        if p_name == "" or p_description == "":
            error = "数据不能为空"
        else:
            Task(name=p_name, suite=Suite.objects.get(id=p_suite), description=p_description, createdAt=now()).save()
    return render(request, "task.html", locals())

def task_view(request, pk):
    p_task = Task.objects.get(id=pk)
    print p_task.name
    #cases = Case.objects.filter(suite=p_task.suite)
    if request.method == "POST":
        p_id = request.POST['case']
        p_case = Case.objects.get(id=p_id)
        Task_Case(case=p_case, task=p_task).save()
        child_cases = Task_Case.objects.filter(task=p_task)
        generate_xml(p_task.name, child_cases)
    child_cases = Task_Case.objects.filter(task=p_task)

    cases = Case.objects.filter(suite=p_task.suite).exclude(task_case__in=child_cases.values_list("id", flat=True))
    return render(request, "task_view.html", locals())

def task_edit(request, pk):
    p_task = Task.objects.get(id=pk)
    if request.method == "POST":
        p_name = request.POST['name']
        p_description = request.POST['description']
        if p_name == "" or p_description == "":
            error = "数据不能为空"
        else:
            p_task.name = p_name
            p_task.description = p_description
            p_task.modifyAt = now()
            p_task.save()
            return redirect(reverse("task_view", kwargs={"pk": pk}))

    return render(request, "task_edit.html", locals())

def task_trigger(request, pk):
    p_task = Task.objects.get(id=pk)
    return redirect(reverse("task_view", kwargs={"pk": pk}))

def task_delete(request, pk_task, pk_case):
    p_task = Task.objects.get(id=pk_task)
    p_case = Case.objects.get(id=pk_case)
    Task_Case.objects.filter(task=p_task).get(case=p_case).delete()
    return redirect(reverse("task_view", kwargs={"pk": pk_task}))


def machine_list(request):
    staf_obj = STAFWrapper()
    staf_obj.register()
    if request.method == "POST":
        p_name = request.POST['name']
        p_description = request.POST['description']
        p_address = request.POST['address']
        if p_name == "" or p_description == "":
            error = "数据不能为空"
        else:
            Machine(name=p_name, description=p_description, address=p_address, createdAt=now()).save()
    machines = Machine.objects.all()
    map_macheine_p = dict()
    for machine in machines:
        p = threading.Thread(target=staf_obj.detect_device, args=(machine.address, ))
        p.start()
        map_macheine_p[machine] = p
    time.sleep(0.5)
    for machine, p in map_macheine_p.items():
        if p.is_alive():
            status = 2
        else:
            status = staf_obj.detect_ret_value
        machine.status = status
        machine.save()
    suites = Suite.objects.all()
    staf_obj.unregister()
    return render(request, "machine.html", locals())


def machine_view(request, pk):
    staf_obj = STAFWrapper()
    staf_obj.register()
    p_machine = Machine.objects.get(id=pk)
    p = threading.Thread(target=staf_obj.detect_device, args=(p_machine.address, ))
    p.start()
    time.sleep(0.5)
    if p.is_alive():
        status = 2
    else:
        status = staf_obj.detect_ret_value
    # status = staf_obj.detect_device(p_machine.address)
    p_machine.status = status
    p_machine.save()
    staf_obj.unregister()
    return render(request, "machine_view.html", locals())

def machine_edit(request, pk):
    p_machine = Machine.objects.get(id=pk)
    if request.method == "POST":
        p_name = request.POST['name']
        p_address = request.POST['address']
        p_description = request.POST['description']
        if p_name == "" or p_description == "":
            error = "数据不能为空"
        else:
            p_machine.name = p_name
            p_machine.address = p_address
            p_machine.description = p_description
            p_machine.modifyAt = now()
            p_machine.save()
            return redirect(reverse("machine_view", kwargs={"pk": pk}))

    return render(request, "machine_edit.html", locals())

def machine_delete(request, pk):
    Machine.objects.get(id=pk).delete()
    return redirect(reverse("machine_list"))

def script_add(request):
    if request.method == "POST":
        p_id = request.POST['id']
        p_file = request.FILES['name']
        suite = Suite.objects.get(id=p_id)
        script_path = settings.MEDIA_ROOT + settings.SCRIPT_DIR + suite.name
        open(script_path + '/' + p_file.name, 'wb').write(p_file.read())
        return redirect(reverse("suite_view", kwargs={"pk": suite.id}))

def script_view(request):
    g_suite = request.GET['suite']
    g_name = request.GET['name']
    suite = Suite.objects.get(id=g_suite)
    script_path = settings.MEDIA_ROOT + settings.SCRIPT_DIR + suite.name + '/' +g_name

    try:
        script = open(script_path)
        script_text = script.read()
    finally:
        script.close()
    return render(request, "script_view.html", locals())

def report_list(request):
    tasks = Task.objects.all()
    for task in tasks:
        totle_num = task.report_case_set.count()
        pass_num = task.report_case_set.filter(result=1).count()
        fail_num = task.report_case_set.filter(result=2).count()
        print totle_num, pass_num, fail_num
    return render(request, "task.html", locals())

def report_view(request,version):
    pass
