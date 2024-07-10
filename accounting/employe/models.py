from django.db import models
from django.conf import settings
from datetime import date, timedelta
# Create your models here.


class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100 ,blank=True, null=True )
    age = models.IntegerField(blank=True, null=True)
    tc = models.CharField(max_length=11, blank=True, null=True, unique=True)  # Use CharField for TC    title = models.CharField(max_length=100 , blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_eploye')
    title = models.CharField(max_length=100, blank=True, null=True)  # Add this line
    state = models.BooleanField(default=True)  # True for active, False for inactive
    def update_state(self):
        thirty_days_ago = date.today() - timedelta(days=30)
        recent_attendances = Attendance.objects.filter(employee=self, date__gte=thirty_days_ago)
        if recent_attendances.exists():
            self.state = True  # Employee has attended within the last 30 days
        else:
            self.state = False  # Employee has not attended within the last 30 days

        self.save()


    


    # Add other fields as necessary

    def __str__(self):
        return f" {self.name } اللقب {self.title}"

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_attandec')

    status = models.CharField(max_length=10)  # e.g., 'Present', 'Absent'

    def __str__(self):
        return f'{self.employee.name} - {self.date}'
    
    def employe(self):
        return f" {self.employee.name } "
    

    def get_employee_name(self):
        return self.employee.name if self.employee else "Unknown Employee"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.employee.update_state()


        