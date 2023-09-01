from django.contrib import admin

from .models import Task, Contact

# Register your models here.
admin.site.register(Task)
admin.site.register(Contact)