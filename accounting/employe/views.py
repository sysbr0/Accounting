

# views.py
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import calendar
from .models import Attendance, Employee
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404 , redirect
from .models import Attendance
from datetime import datetime
from datetime import date
from .forms import EmployeeForm
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user

from .models import Employee




from datetime import datetime, timedelta


def calendar_view(request):
    # Get today's date
    now = datetime.now()
    
    # Determine the month and year from query parameters if provided, otherwise use current month and year
    month = request.GET.get('month', now.month)
    year = int(request.GET.get('year', now.year))
    
    # Convert month to integer if it's a string
    try:
        month = int(month)
    except ValueError:
        month = now.month

    # Calculate the previous and next months and years
    prev_month = month - 1 if month > 1 else 12
    prev_year = year - 1 if month == 1 else year
    next_month = month + 1 if month < 12 else 1
    next_year = year + 1 if month == 12 else year

    # Get the calendar month as a list of tuples (day, weekday)
    cal = calendar.monthcalendar(year, month)

    # Context data to pass to the template
    context = {
        'now': now,
        'calendar': cal,
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],  # Get month name as string
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
    }
    
    return render(request, 'attendance/calendar.html', context)

def attendance_view(request, year, month, day):
    date_string = f'{year}-{month}-{day}'
    formatted_date = date(year, month, day)



        # Retrieve Attendance object or raise 404 if not found
    attendance = Attendance.objects.filter(date =formatted_date )
 

    context = {
        'attendance': attendance,
        'attendance_date': formatted_date,
        'date_string' :date_string
    }

    return render(request, 'attendance/attendance.html', context)







def attendance_detail_view(request):
    selected_date = request.GET.get('date')
    if selected_date:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        # Example data for employees who attended on the selected date
        employees_attended = ['Employee A', 'Employee B', 'Employee C']
        return render(request, 'attendance/attendance.html', {'employees_attended': employees_attended, 'selected_date': selected_date})
    else:
        return HttpResponse('No date selected.')
    


@login_required
def add_employee(request):
    email = request.user.email if request.user.is_authenticated else None
    print(email)

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            if not employee.created_by:  # Ensure not to override if already set
                employee.created_by = request.user.id  # Assuming you want to store the user ID
            employee.save()
            return redirect('employee_list_view')
    else:
        form = EmployeeForm()

    context = {
        'form': form,
        'email': email
    }
    return render(request, 'employe/add.html', context)




def employee_list_view(request):
    employees = Employee.objects.all()
    return render(request, 'employe/list.html', {'employees': employees})




def edit_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            # Optionally add a success message using Django messages framework
            return redirect('employee_list_view')  # Redirect to employee detail view
    else:
        form = EmployeeForm(instance=employee)
    
    return render(request, 'employe/edit.html', {'form': form, 'employee': employee})





@login_required
def today_attaned(request):
     today = date.today()
     
     

        # Retrieve Attendance object or raise 404 if not found
     attendance = Attendance.objects.filter(date =today )
     for obj in attendance:
       print(obj)


     context = {
        'attendance': attendance,
        'attendance_date': today,

    }



     return render(request, 'attendance/add_attend.html', context)



@login_required
def add_today(request):
    today = date.today()
    
    # Retrieve employees who have not attended today
    employees_not_attended_today = Employee.objects.exclude(
        attendance__date=today,
        attendance__created_by=request.user  # Assuming each attendance is linked to a user
    ).order_by('-state')
    
    context = {
        'employees_not_attended_today': employees_not_attended_today,
        'attendance_date': today,
    }

    return render(request, 'attendance/adding.html', context)



def add_attendance(request, id):
    employee = get_object_or_404(Employee, id=id)
    today = date.today()

    # Check if the attendance record already exists for today
    if Attendance.objects.filter(employee=employee, date=today).exists():
        messages.warning(request, f"Attendance for {employee.name} already exists for today.")
    else:
        # Create a new attendance record
        Attendance.objects.create(
            employee=employee,
            date=today,
            created_by=request.user,
            status='Present'  # or any other status you want to set
        )
        messages.success(request, f"Attendance for {employee.name} has been added.")

    return redirect('add_today')



@login_required
def last_week_attendance(request):
    today = date.today()
    last_week = today - timedelta(days=7)

    # Filter attendance records for the last week and count the number of days each employee attended
    attendance_counts = (
        Attendance.objects.filter(date__gte=last_week)
        .values('employee__id', 'employee__name', 'employee__position')
        .annotate(attendance_days=Count('date'))
        .order_by('-attendance_days')
    )

    context = {
        'attendance_counts': attendance_counts,
        'start_date': last_week,
        'end_date': today,
    }

    return render(request, 'attendance/last_week.html', context)
@login_required
def last_month_attendance(request):
    today = date.today()
    last_month = today - timedelta(days=30)

    # Filter attendance records for the last month and count the number of days each employee attended
    attendance_counts = (
        Attendance.objects.filter(date__gte=last_month)
        .values('employee__id', 'employee__name', 'employee__position')
        .annotate(attendance_days=Count('date'))
        .order_by('-attendance_days')
    )

    context = {
        'attendance_counts': attendance_counts,
        'start_date': last_month,
        'end_date': today,
    }

    return render(request, 'attendance/last_month.html', context)


@login_required
def attendance_views(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if from_date and to_date:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
        attendance_records = Attendance.objects.filter(date__range=[from_date, to_date])
    else:
        attendance_records = Attendance.objects.all()

    attendance_count = attendance_records.values('employee__name').annotate(total_days=Count('date')).order_by('employee__name')

    context = {
        'from_date': from_date,
        'to_date': to_date,
        'attendance': attendance_records,
        'attendance_count': attendance_count
    }
    
    print(attendance_records)  # Debug print
    print(attendance_count)    # Debug print
    
    return render(request, 'attendance/from_to.html', context)