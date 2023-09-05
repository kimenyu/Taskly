from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.text import slugify



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    description = models.TextField("Description", max_length=600, default='', blank=True)
    
    # Add related_name to groups and user_permissions fields
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',  # Choose a custom related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',  # Choose a custom related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

from django.conf import settings  # Import the settings module

class Task(models.Model):
    title = models.CharField(max_length=200)  # Title of the task
    description = models.TextField(blank=True, null=True)  # Optional task description
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the task was created
    due_date = models.DateTimeField(blank=True, null=True)  # Optional due date for the task
    completed = models.BooleanField(default=False)  # Whether the task has been completed
    
    # Use settings.AUTH_USER_MODEL as the foreign key target
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # User who owns the task
    slug = models.SlugField(max_length=200, blank=True, null=True)  # Slug field for pretty URLs
    
    class Meta:
        order_with_respect_to = 'user'
        
    def save(self, *args, **kwargs):
        # If the slug field is empty, populate it with the slugified title
        if not self.slug:
            self.slug = slugify(self.title)
        super(Task, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title  # Display the title of the task as its string representation
    
    
    def mark_as_completed(self):
        self.completed = True
        self.save()

    def is_overdue(self):
        if self.due_date and timezone.now() > self.due_date:
            return True
        return False