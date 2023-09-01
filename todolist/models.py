from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Task(models.Model):
    taskID = models.AutoField(primary_key=True)
    taskTitle = models.CharField(max_length=100, default="")
    taskDescription = models.CharField(max_length=2000, default="")
    taskCompleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.taskTitle

class Contact(models.Model):
    s_no = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=15, default="")
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return self.name