from django.contrib import admin
from .models import User, Task, Tag, TaskTag, Priority, TaskPriority

# Register your models here.
admin.site.register(User)
admin.site.register(Task)
admin.site.register(Tag)
admin.site.register(TaskTag)
admin.site.register(Priority)
admin.site.register(TaskPriority)
