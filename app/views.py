from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "index.html", {"key": "11111111111111"})
def plateform(request):
    return render(request, "plateform.html", {"key": "11111111111111"})
def project(request):
    return render(request, "project.html", {"key": "11111111111111"})
def project_group(request):
    return render(request, "project_group.html", {"key": "11111111111111"})
def case(request):
    return render(request, "case.html", {"key": "11111111111111"})