from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


# w oparciu o usera zrobic model customera który przechoyuje dane usera i link do URL z zdjęciem profilowym
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True)
    surname = models.CharField(max_length=30, null=True)
    email = models.CharField(max_length=30, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    profile_image_url = models.URLField(max_length=250, null=True, blank=True, default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSHcM04W6diLQBzw4Y4pXDhPgovRf7l1cBF0Q&usqp=CAU")

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = "Customers"
        verbose_name = "Customer"


class Event(models.Model):
    VERY_HIGH = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    VERY_LOW = 5
    PRIORITY_CHOICES = [
        (VERY_HIGH, 'Bardzo Wysoki'),
        (HIGH, 'Wysoki'),
        (MEDIUM, 'Średni'),
        (LOW, 'Niski'),
        (VERY_LOW, 'Bardzo Niski'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    title = models.CharField(max_length=50, null=True)
    completed = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user.username}'s - Priority: {self.priority} - Completed: {self.completed}"


class Task(Event):
    on_date = models.DateTimeField()

    def __str__(self):
        return f"Task - Nazwa: {self.title} - Priority: {self.priority} - Ukończony: {self.completed} - W dniu: {self.on_date.strftime('%Y-%m-%d %H:%M')}"


class Project(Event):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Project - Nazwa: {self.title} - Priority: {self.priority} - Ukończony: {self.completed} - Od dnia: {self.start_date.strftime('%Y-%m-%d %H:%M')} - Do dnia: {self.end_date.strftime('%Y-%m-%d %H:%M')}"