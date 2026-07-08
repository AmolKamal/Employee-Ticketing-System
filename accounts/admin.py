from django.contrib import admin
from .models import EmployeeInfo, ContactInfo
# Register your models here.
admin.site.register(EmployeeInfo)
admin.site.register(ContactInfo)