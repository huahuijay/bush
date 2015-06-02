# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Plateform(models.Model):
    userId = models.ForeignKey(User)
    createdAt = models.DateTimeField("创建的时间", auto_now_add=True)
    name = models.CharField('平台名称', max_length=255, unique=True)
    description = models.TextField('平台描述', blank=True, null=True)

class Project(models.Model):
    user = models.ForeignKey(User)
    plateform = models.ForeignKey(Plateform)
    createdAt = models.DateTimeField("创建的时间", auto_now_add=True)
    name = models.CharField('项目名称', max_length=255, unique=True)
    description = models.TextField('项目描述', blank=True, null=True)
    owner = models.IntegerField(blank=True, null=True)

class ProjectGroup(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    createdAt = models.DateTimeField("创建的时间",auto_now_add=True)
    name = models.CharField('项目组名称', max_length=255, unique=True)
    description = models.TextField('项目组描述', blank=True, null=True)

class Suite(models.Model):
    #user = models.ForeignKey(User)
    name = models.CharField('套件名称', max_length=255, unique=True)
    description = models.TextField('套件描述', blank=True, null=True)
    createdAt = models.DateTimeField("创建的时间", auto_now_add=True)

class Case(models.Model):
    #user = models.ForeignKey(User)
    #progect_group = models.ForeignKey(ProjectGroup)
    suite = models.ForeignKey(Suite)
    name = models.CharField("用例名称", max_length=255, unique=True)
    description = models.TextField('用例描述', blank=True, null=True)
    level = models.IntegerField('用例等级', choices=((1, "低"), (2, '中'), (3, '高')))
    command = models.TextField('命令', max_length=255, null=True)
    param = models.TextField('参数', max_length=255, null=True)
    createdAt = models.DateTimeField("创建的时间", auto_now_add=True)

class Task(models.Model):
    #user = models.ForeignKey(User)
    suite = models.ForeignKey(Suite)
    name = models.CharField("任务名称", max_length=255, unique=True)
    description = models.TextField('任务描述', blank=True, null=True)
    createdAt = models.DateTimeField("创建的时间", auto_now_add=True)

    def __unicode__(self):
        return self.name

class Task_Case(models.Model):
    case = models.ForeignKey(Case)
    task = models.ForeignKey(Task)
    createdAt = models.DateTimeField("创建的时间", auto_now_add=True)