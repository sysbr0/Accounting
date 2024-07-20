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
    created_by = models.IntegerField(null=True , blank=True)
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
    def save(self, *args, **kwargs):
        if not self.pk:  # Only set created_by on creation, not on update
            self.created_by = kwargs.pop('created_by', None)  # Pop the created_by user from kwargs if provided
        super(Employee, self).save(*args, **kwargs)


    def __str__(self):
        return f" {self.name } "
    


  

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_attandec')

    status = models.CharField(max_length=10 , blank=True, null=True)  # e.g., 'Present', 'Absent'
    ispyed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.employee.name} - {self.date}'
    
    def employe(self):
        return f" {self.employee.name } "
    

    def get_employee_name(self):
        return self.employee.name if self.employee else "Unknown Employee"
    

    def created_by_admin(self):
        return self.created_by.full_name


    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the instance is being created
            # Check if there is already an attendance record for this employee on the same date
            existing_attendance = Attendance.objects.filter(employee=self.employee, date=self.date).first()
            if existing_attendance:
                # If an attendance record exists, update it instead of creating a new one
                existing_attendance.status = self.status
                existing_attendance.save()
                return existing_attendance
            
            
        
        # If no existing attendance record, proceed with normal save
        super().save(*args, **kwargs)
        
        # Update the employee state after saving attendance
        self.employee.update_state()
        return self
   