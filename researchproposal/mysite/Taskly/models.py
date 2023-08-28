from django.db import models
from django.contrib.auth.models import AbstractUser

# User Model: Represents users of the app, extends the built-in AbstractUser model
class User(AbstractUser):

    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='taskly_users_groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='taskly_users_permissions'
    )
    
    email = models.EmailField(unique=True)
    description = models.TextField("Description", max_length=600, default='', blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)
    social_media_links = models.URLField(blank=True)

    def __str__(self):
        return self.username

# Task Model: Represents tasks in the todo app
class Task(models.Model):
    title = models.CharField(max_length=200)  # Title of the task
    description = models.TextField(blank=True, null=True)  # Optional task description
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the task was created
    due_date = models.DateField()  # Due date for the task
    completed = models.BooleanField(default=False)  # Indicates if the task is completed
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who owns the task

    def __str__(self):
        return self.title  # Display the title of the task as its string representation

# Tag Model (Optional): Represents categories or tags that can be associated with tasks
class Tag(models.Model):
    name = models.CharField(max_length=50)  # Name of the tag

    def __str__(self):
        return self.name  # Display the name of the tag as its string representation

# TaskTag Model (Optional): Associates tags with tasks using a many-to-many relationship
class TaskTag(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)  # Task associated with the tag
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)  # Tag associated with the task

    def __str__(self):
        return f"{self.task} - {self.tag}"  # Display the task and tag relationship

# Priority Model (Optional): Represents priority levels that can be associated with tasks
class Priority(models.Model):
    name = models.CharField(max_length=20)  # Name of the priority level

    def __str__(self):
        return self.name  # Display the name of the priority level as its string representation

# TaskPriority Model (Optional): Associates priorities with tasks using a many-to-many relationship
class TaskPriority(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)  # Task associated with the priority
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)  # Priority associated with the task

    def __str__(self):
        return f"{self.task} - {self.priority}"  # Display the task and priority relationship
