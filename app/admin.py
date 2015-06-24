from django.contrib import admin
from .models import Suite,Case
# Register your models here.

class SuiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'createdAt')

class CaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'createdAt')

admin.site.register(Suite, SuiteAdmin)
admin.site.register(Case, CaseAdmin)
