# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
#class User(models.Model):
#    name = models.CharField(max_length=255)

class Plateform(models.Model):
    # default:
    createdAt = models.DateTimeField("创建的时间")
    name = models.CharField('项目名称', max_length=255, unique=True)
    description = models.TextField('项目描述', blank=True, null=True)
    owner = models.IntegerField(blank=True, null=True)

class Project(models.Model):
    # default:
#    user = models.ForeignKey(User)
    plateform = models.ForeignKey(Plateform)
    createdAt = models.DateTimeField("创建的时间")
    name = models.CharField('项目名称', max_length=255, unique=True)
    description = models.TextField('项目描述', blank=True, null=True)
    owner = models.IntegerField(blank=True, null=True)

class ProjectGroup(models.Model):
    # default:
#    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    createdAt = models.DateTimeField("创建的时间")
    name = models.CharField('项目组名称', max_length=255, unique=True)
    description = models.TextField('项目组描述', blank=True, null=True)

class Case(models.Model):
    # default:
    project = models.ForeignKey(Project)
    progect_group = models.ForeignKey(ProjectGroup)
    createdAt = models.DateTimeField("创建的时间")
    name = models.CharField('用例名称', max_length=255, unique=True)
    description = models.TextField('用例描述', blank=True, null=True)

