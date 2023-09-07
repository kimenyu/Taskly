from django.contrib import admin
from .models import CustomUser, Task
from django.utils.text import slugify  # Import the slugify function


class TaskAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)} 
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Task, TaskAdmin)

