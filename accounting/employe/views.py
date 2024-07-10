

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
MONTH_MAPPING = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12,
}

def attendance_view(request, year, month, day):
    # Construct date string in 'YYYY-MM-DD' format
    date_string = f'{year}-{month}-{day}'
    formatted_date = date(year, month, day)



        # Retrieve Attendance object or raise 404 if not found
    attendance = Attendance.objects.filter(date =formatted_date )
    for obj in attendance:
       print(obj)


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
    



def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee added successfully!')
            return redirect('employee_list_view')  # Replace with your actual URL name
        else:
            # If form is not valid, display error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = EmployeeForm()

    context = {
        'form': form,
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
            return redirect('employee_detail', employee_id=employee.id)  # Redirect to employee detail view
    else:
        form = EmployeeForm(instance=employee)
    
    return render(request, 'employe/edit.html', {'form': form, 'employee': employee})