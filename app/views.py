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

import utils

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect(reverse("task_list"))
        else:
            return render(request, "login.html", locals())

    else:
        return render(request, "login.html", locals())

def logout_view(request):
    logout(request)
    return redirect(request.META.get("HTTP_REFERER", reverse("task_list")))

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
    if Suite.objects.exists():
        suites = Suite.objects.all()

    return render(request, "suite.html", locals())

def suite_create(request):
    if request.method == "POST":
        p_name = request.POST['name']
        p_description = request.POST['description']
        if p_name == "" or p_description == "":
            error = "数据不能为空"
        else:
            Suite(name=p_name, description=p_description, createdAt=now()).save()
        return redirect(reverse("suite_list"))
    return render(request, "suite_create.html", locals())

def case_list(request):
    p_suite = None
    cases = None
    suites = None

    if Suite.objects.exists():
        p_suite = Suite.objects.all().order_by('id')[0]
        suites = Suite.objects.all()
        cases = Case.objects.filter(suite=p_suite)
    return render(request, "case.html", locals())


def case_list_index(request, pk):
    p_suite = None
    suites = None
    cases = None
    if Suite.objects.exists():
        suites = Suite.objects.all()
        p_suite = Suite.objects.get(id=pk)
        cases = Case.objects.filter(suite=p_suite).order_by('id')
    return render(request, "case.html", locals())

def case_create(request, pk):
    p_suite = Suite.objects.get(id=pk)
    suites = Suite.objects.all()
    if request.method == "POST":
        p_name = request.POST['name']
        p_level = request.POST['level']
        p_suite = Suite.objects.get(id=pk)
        p_command = request.POST['command']
        p_script = request.POST['script']
        p_param = request.POST['param']
        p_description = request.POST['description']
        if p_name == "" or p_command == "" or p_description == "":
            error = "数据不能为空"
        else:
            Case(name=p_name, suite=p_suite,  level=p_level, command=p_command,
                 script=p_script, param=p_param, description=p_description, createdAt=now()).save()
            return redirect(reverse("case_list_index", kwargs={"pk": pk}))
    return render(request, "case_create.html", locals())

def case_view(request, pk):
    case = None
    suites = None
    if Suite.objects.exists():
        case = Case.objects.get(id=pk)
        suites = Suite.objects.all()
    return render(request, "case_view.html", locals())

def case_delete(request, pk):
    Case.objects.get(id=pk).delete()
    return redirect(reverse("case_list"))

def case_edit(request, pk):
    suites = None
    case = None
    case = Case.objects.get(id=pk)

    if request.method == "POST":
        p_name = request.POST['name']
        p_level = request.POST['level']
        p_command = request.POST['command']
        p_script = request.POST['script']
        p_param = request.POST['param']
        p_description = request.POST['description']
        if p_name == "" or p_command == "" or p_description == "":
            error = "数据不能为空"
        else:
            case.name = p_name
            case.level = p_level
            case.command = p_command
            case.script = p_script
            case.param = p_param
            case.description = p_description
            case.modifyAt = now()
            case.save()
            return redirect(reverse("case_view", kwargs={"pk": pk}))
    else:
        if Suite.objects.exists():
            suites = Suite.objects.all()
        return render(request, "case_edit.html", locals())

def task_list(request):
    p_suite = None
    suites = None
    tasks = None
    if Suite.objects.exists():
        p_suite = Suite.objects.all().order_by('id')[0]
        suites = Suite.objects.all()
        tasks = Task.objects.filter(suite=p_suite)
    return render(request, "task.html", locals())

def task_list_index(request, pk):
    p_suite = None
    suites = None
    tasks = None
    if Suite.objects.exists():
        p_suite = Suite.objects.get(id=pk)
        suites = Suite.objects.all()
        tasks = Task.objects.filter(suite=p_suite).order_by('id')
    return render(request, "task.html", locals())

def task_create(request, pk):
    p_suite = Suite.objects.get(id=pk)
    suites = Suite.objects.all()
    cases = Case.objects.filter(suite=p_suite).order_by('id')
    if request.method == "POST":
        p_name = request.POST['name']
        p_description = request.POST['description']
        if p_name == "" or p_description == "":
            error = "数据不能为空"
        else:
            Task(name=p_name, suite=p_suite, description=p_description, createdAt=now()).save()
            return redirect(reverse("task_list_index", kwargs={"pk": pk}))
    return render(request, "task_create.html", locals())

def task_view(request, pk):
    suites = None
    p_task = Task.objects.get(id=pk)
    p_cases = Task_Case.objects.filter(task=p_task)

    if Suite.objects.exists():
        suites = Suite.objects.all()
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
    suites = None
    p_task = None
    p_cases = None
    if Suite.objects.exists():
        suites = Suite.objects.all()
        p_task = Task.objects.get(id=pk)
        p_task_cases = Task_Case.objects.filter(task=p_task)
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
    staf_obj = STAFWrapper()
    staf_obj.register()
    utils.tmp_handle_global = staf_obj.execute(p_task.name)
    staf_obj.unregister()
    # cases = Task_Case.objects.filter(p_task)
    # if cases:
    #     for p_case in cases:
    #         Report(case=p_case, )
    return redirect(reverse("task_view", kwargs={"pk": pk}))

def task_delete(request, pk):
    p_task = Task.objects.get(id=pk)
    Task_Case.objects.filter(task=p_task).delete()
    Task.objects.get(id=pk).delete()
    return redirect(reverse("task_list"))


def task_case_create(request):
    pass

def task_case_delete(request):
    #Task_Case.objects.filter(task=p_task).get(case=p_case).delete()
    pass

def machine_list(request):
    staf_obj = STAFWrapper()
    staf_obj.register()
    suites = Suite.objects.all()
    p_suite = Suite.objects.all().order_by('id')[0]
    machines = Machine.objects.filter(suite=p_suite).order_by('id')
    if request.method == "POST":
        p_name = request.POST['name']
        p_description = request.POST['description']
        p_address = request.POST['address']
        if p_name == "" or p_description == "":
            error = "数据不能为空"
        else:
            Machine(name=p_name, description=p_description, address=p_address, createdAt=now()).save()
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
    staf_obj.unregister()
    return render(request, "machine.html", locals())

def machine_list_index(request, pk):
    p_suite = None
    suites = None
    machines = None
    if Suite.objects.exists():
        p_suite = Suite.objects.get(id=pk)
        suites = Suite.objects.all()
        machines = Machine.objects.filter(suite=p_suite).order_by('id')
    return render(request, "machine.html", locals())

def machine_view(request, pk):
    suites = None
    p_suite = None
    machine = None
    if Suite.objects.exists():
        suites = Suite.objects.all()
        machine = Machine.objects.get(id=pk)
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

def machine_create(request, pk):
    suites = Suite.objects.all()
    p_suite = Suite.objects.get(id=pk)
    if request.method == "POST":
        p_name = request.POST['name']
        p_description = request.POST['description']
        p_address = request.POST['address']
        if p_name == "" or p_description == "":
            error = "数据不能为空"
        else:
            Machine(name=p_name, suite=p_suite, description=p_description, address=p_address, createdAt=now()).save()
            return redirect(reverse("machine_list_index", kwargs={"pk": pk}))
    return render(request, "machine_create.html", locals())

def machine_edit(request, pk):
    suites = None
    p_suite = None

    if Suite.objects.exists():
        suites = Suite.objects.all()
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
    else:
        return render(request, "machine_edit.html", locals())

def machine_delete(request, pk):
    Machine.objects.get(id=pk).delete()
    return redirect(reverse("machine_list"))

def script_list(request):
    script_path = settings.MEDIA_ROOT + settings.SCRIPT_DIR
    if request.method == "POST":
        p_file = request.FILES['name']
        open(script_path + p_file.name, 'wb').write(p_file.read())
    scripts = os.listdir(script_path)
    return render(request, "script.html", locals())

def script_view(request):
    g_name = request.GET['name']
    script_path = settings.MEDIA_ROOT + settings.SCRIPT_DIR + g_name

    try:
        script = open(script_path)
        script_text = script.read()
    finally:
        script.close()
    return render(request, "script_view.html", locals())

def script_add(request):
    if request.method == "POST":
        p_file = request.FILES['name']
        script_path = settings.MEDIA_ROOT + settings.SCRIPT_DIR
        open(script_path + p_file.name, 'wb').write(p_file.read())
        return redirect(reverse("script_view"))

def report_list(request):
    suites = None
    if Suite.objects.exists():
        suites = Suite.objects.all()
    reports = Report.objects.all()
    return render(request, "report.html", locals())

def report_view(request, pk):
    pass

def lay(request):
    return render(request, "layout.html", locals())