from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    joining_date = models.DateField()

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='tasks')

    def days_left(self):
        """Return days remaining until due date"""
        return (self.due_date - date.today()).days

    def clean(self):
        """Validation rule: Prevent >5 pending tasks for same employee"""
        if self.status == 'PENDING':
            pending_tasks = Task.objects.filter(employee=self.employee, status='PENDING')
            if self.pk:  # editing existing task
                pending_tasks = pending_tasks.exclude(pk=self.pk)
            if pending_tasks.count() >= 5:
                raise ValidationError(f"{self.employee.name} already has 5 pending tasks.")

    def __str__(self):
        return self.title
