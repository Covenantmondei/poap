from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=255) 
    metadata = models.TextField() 
    location = models.CharField(max_length=255) 
    creator = models.CharField(max_length=255)  # wallet address 
    start_time = models.DateTimeField()

class Attendance(models.Model):
    attendee = models.CharField(max_length=255)  # wallet address
    badge_hash = models.CharField(max_length=255, unique=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendances')
    timestamp = models.DateTimeField(auto_now_add=True)