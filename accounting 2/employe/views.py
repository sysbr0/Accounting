

# views.py
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import calendar
from .models import Attendance, Employee , Salary , EmployeePayment
import csv
from django.db.models import Sum, Count
from django.shortcuts import render, get_object_or_404 , redirect
from .models import Attendance
from datetime import datetime
from datetime import date
from .forms import EmployeeForm ,  TCForm , MarkPaidForm  , SalaryForm , EmployeePaymentForm
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.db import transaction
import json
from .models import Employee

from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.utils import timezone
from calendar import Calendar
from django.urls import reverse
from users.forms import LogingForm
from datetime import datetime, timedelta
import google.generativeai as genai
import os




from django.views.decorators.csrf import csrf_exempt
import json


Gemini_API = os.getenv('Gemini_API')

genai.configure(api_key=Gemini_API)

# Create the model
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="This is a company management system.",
)




def admin_chat(request):
    name = request.user.email if request.user.is_authenticated else None



    # Retrieve employee and attendance records
    employee = Employee.objects.all()
  
    attendance_records = Attendance.objects.all()

    # Create arrays for employee and attendance information
    employee_info = [ {
        "name": record.name,
        "age": record.age,
        "position": record.position,
        "tc": record.tc,
        "title": record.title,
        "state": record.state,
    }
     for record in employee
    ]

    attendance_info = [
        {
            "employee": record.employee,
            "date": record.date,
            "status": record.status,
            "is_paid": record.ispyed,
        }
        for record in attendance_records
    ]

    # Initialize chat session with predefined messages for context
    chat_history = [


        {"role": "user", "parts": [f" مرحبا ساقوم بارسال بعض البيانات عن العاملين لدي ولدي ايضا جدول  يعرض  ايام الجضور لكل شخص وهنالك  خيار يعرض اذا كان اليوم مدوفع او لا  اجب بللغة العربية حصرا "]},


        {"role": "model", "parts": [f"مرحبا ,  بالطبع سؤجيب بالغة لعربية ، كيف يمكنني مساعدتك اليوم  ?"]},
        {"role": "user", "parts": ["اريد ان اعرف كم يوم لي في العمل سواء ايام مدفوقة او ايام غير مدفوعة  لكن احرص على ان البيانات التي سترسلها ستكون عبارة عن تنسيق html ولا تنسى التنسيق فهو مهم جداا  css?"]},
        {"role": "model", "parts": ["هل يمكنك ارسال المعلومات او البيانات "]},
    ]

    for record in attendance_info:
        chat_history.append(
            {"role": "user", "parts": [f"التاريخ: {record['date']}, الحالة : {record['status']}, حالة الدفع : {record['is_paid']}  العامل هو {record['employee']}"]}
        )

    for record in employee_info:
        chat_history.append(
            {"role": "user", "parts": [f"اسم العاملة : {record['name']}, الاسم بلانجليزية : {record['title']}, المعرف  : {record['tc']}"]}
        )

    

    chat_session = model.start_chat(history=chat_history)

    if request.method == 'POST':
        user_input = request.POST.get('message', '')

        # Send the user input to the model and get the response
        response = chat_session.send_message(user_input)
        model_response = response.text

        # Append to history
        chat_session.history.append({"role": "user", "parts": [user_input]})
        chat_session.history.append({"role": "model", "parts": [model_response]})

        return JsonResponse({'response': model_response})

    context = {
        'employee_info': employee_info,
        'attendance_info': attendance_info,
        "name" :name,
    }

    return render(request, 'chat.html', context)






def chat_view(request, id):
    # Retrieve employee and attendance records
    employee = get_object_or_404(Employee, id=id)

    
    attendance_records = Attendance.objects.filter(employee=employee)

    # Create arrays for employee and attendance information
    employee_info = {
        "name": employee.name,
        "age": employee.age,
        "position": employee.position,
        "tc": employee.tc,
        "title": employee.title,
        "state": employee.state,
    }
    name = employee_info['name']



    attendance_info = [

        {
            
            "date": record.date,
            "status": record.status,
            "is_paid": record.ispyed,
        }
        for record in attendance_records
    ]

    # Initialize chat session with predefined messages for context
    chat_history = [
        {"role": "user", "parts": [f"مرحبا انا اسمي  {employee.name}. رجاءا لا تتحدث الا باللغة العربية انا لا اجيد الإنجليزية "]},
        {"role": "model", "parts": [f"مرحبا  {employee.name},  بالطبع سؤجيب بالغة لعربية ، كيف يمكنني مساعدتك اليوم  ?"]},
        {"role": "user", "parts": ["اريد ان اعرف كم يوم لي في العمل سواء ايام مدفوقة او ايام غير مدفوعة ?"]},
        {"role": "model", "parts": ["هل يمكنك ارسال المعلومات او البيانات "]},
    ]

    for record in attendance_info:
        chat_history.append(
            {"role": "model", "parts": [f"التاريخ: {record['date']}, الحالة : {record['status']}, حالة الدفع : {record['is_paid']}"]}
        )

    chat_session = model.start_chat(history=chat_history)

    if request.method == 'POST':
        user_input = request.POST.get('message', '')

        # Send the user input to the model and get the response
        response = chat_session.send_message(user_input)
        model_response = response.text

        # Append to history
        chat_session.history.append({"role": "user", "parts": [user_input]})
        chat_session.history.append({"role": "model", "parts": [model_response]})

        return JsonResponse({'response': model_response})

    context = {
        'employee_info': employee_info,
        'attendance_info': attendance_info,
        "name" : name
    }

    return render(request, 'chat.html', context)



def download_employee_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')

   
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['Id','Name', 'Position', 'Age', 'TC', 'Created At', 'Created By', 'Title', 'State'])

    # Write the data rows
    employees = Employee.objects.all()
    for employee in employees:
        writer.writerow([
            employee.id,
            employee.name,
            employee.position,
            employee.age,
            employee.tc,
            employee.created_at,
            employee.created_by,
            employee.title,
            employee.state,
        ])

    return response









def download_attendance_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="attendance.csv"'

    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'Employee Name', 'Date', 'Created By', 'Status', 'Is Paid'])

    attendances = Attendance.objects.all()
    for attendance in attendances:
        writer.writerow([
            attendance.employee.id,
            attendance.get_employee_name(),
            attendance.date,
            attendance.created_by,  # Assuming AUTH_USER_MODEL has a 'username' field
            attendance.status,
            attendance.ispyed,
        ])

    return response





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



def attendance_view_admin(request, year, month, day):
    date_string = f'{year}-{month}-{day}'
    formatted_date = date(year, month, day)



        # Retrieve Attendance object or raise 404 if not found
    attendance = Attendance.objects.filter(date =formatted_date )
    count_attendance = attendance.count()
 

    context = {
        'attendance': attendance,
        'attendance_date': formatted_date,
        'date_string' :date_string,
        "count_attendance":count_attendance
    }

    return render(request, 'attendance/attandce_admin.html', context)





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
    email = request.user.email if request.user.is_authenticated else None
    return render(request, 'employe/list.html', {'employees': employees , 'email':email})



def pyment(request):
    employes = Employee.objects.all()


    employees = [employee for employee in employes if employee.is_working and employee.calculate_balance() != 0]
    total_balance = sum(employee.calculate_balance() for employee in employees)


    email = request.user.email if request.user.is_authenticated else None
    return render(request, 'pyment/report.html', {'employees': employees , 'email':email , "total":total_balance})



def employee_payment_view(request, id):
    employee = get_object_or_404(Employee, id=id)
    
    if request.method == 'POST':
        form = EmployeePaymentForm(request.POST)
        if form.is_valid():
            form.instance.employee = employee  # Set the employee instance
            form.save()
            messages.success(request, 'Payment has been successfully created.')
            return redirect('employee_payment_view', id=id)
        else:
            messages.error(request, 'There was an error with the form submission.')
    else:
        form = EmployeePaymentForm()
    
    last_payments = EmployeePayment.objects.filter(employee=employee).order_by('-date')[:10]

    context = {
        'employee': employee,
        'form': form,
        'last_payments': last_payments,
    }

    return render(request, 'pyment/add.html', context)


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

   


    salaries = Salary.objects.filter(employee=employee).order_by('-effective_date')
   



    


    
    return render(request, 'employe/edit.html', {'form': form, 'employee': employee , 'salaries' : salaries})




def tc_input_view(request):
    if request.method == 'POST':
        form = TCForm(request.POST)
        if form.is_valid():
            tc = form.cleaned_data['tc']
            # Check if the TC exists in the Employee model
            employee = get_object_or_404(Employee, tc=tc)
            return redirect('serch_result', id=employee.id)
    else:
        form = TCForm()
    
    return render(request, 'employe/serch.html', {'form': form})





def searching_result(request, id):
   



    today = timezone.now().date()
    checking = False
    
    employee = get_object_or_404(Employee, id=id)
    attendance_records = Attendance.objects.filter(employee=employee).order_by('-date')
    attendance_today = Attendance.objects.filter(employee=employee, date=today).first()
    
    if attendance_today:
        message = "لقد تم تسجيل حضورك اليوم"
        checking = True
    else:
        message = "لم يتم تسجيل حضورك اليوم"
    
    # Get current year and month from request or default to current month
    year = request.GET.get('year', today.year)
    month = request.GET.get('month', today.month)
    
    year = int(year)
    month = int(month)
    
    cal = Calendar()
    month_days = cal.monthdayscalendar(year, month)

    # Gather attendance for the entire month
    month_start = datetime(year, month, 1)
    month_end = month_start + timedelta(days=calendar.monthrange(year, month)[1])
    monthly_attendance = Attendance.objects.filter(employee=employee, date__range=[month_start, month_end])

    attendance_days = set(att.date.day for att in monthly_attendance)




    context = {
     
        'employee': employee,
        'attendance_records': attendance_records,
        'message': message,
        'checking': checking,
        'calendar': month_days,
        'attendance_days': attendance_days,
        'year': year,
        'month': month,
        'now': today,
        'month_name': month_start.strftime('%B'),
        'prev_year': (month_start - timedelta(days=1)).year,
        'prev_month': (month_start - timedelta(days=1)).month,
        'next_year': (month_end + timedelta(days=1)).year,
        'next_month': (month_end + timedelta(days=1)).month,
    }








    
    return render(request, 'employe/see.html', context)





def serch_result(request, id):
    email = request.user.email if request.user.is_authenticated else None
    today = timezone.now().date()
    
    employee = get_object_or_404(Employee, id=id)
    
    
    # Get current year and month from request or default to current month
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month)
    
    # Gather attendance for the entire month
    month_start = datetime(year, month, 1)
    month_end = month_start + timedelta(days=calendar.monthrange(year, month)[1])
    monthly_attendance = Attendance.objects.filter(employee=employee, date__range=[month_start, month_end])
    
    # Create a set of days where attendance was recorded and their status
    attendance_days = set(att.date.day for att in monthly_attendance)
    attendance_status = {att.date.day: att.ispyed for att in monthly_attendance}
    
    # Check if attendance was recorded today
    attendance_today = Attendance.objects.filter(employee=employee, date=today).first()
    if attendance_today:
        message = "لقد تم تسجيل حضورك اليوم"
        cheking = True
    else:
        message = "لم يتم تسجيل حضورك اليوم"
        cheking = False
    
    # Get date range from request if available
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    
    if from_date and to_date:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
        attendance_records = Attendance.objects.filter(date__range=[from_date, to_date], employee=employee)
        pyment_record = Attendance.objects.filter(date__range=[from_date, to_date], employee=employee , ispyed=True )
    else:
        attendance_records = Attendance.objects.filter(employee=employee)
        pyment_record = Attendance.objects.filter(employee=employee , ispyed=True )

    
    attendance_count = attendance_records.values('employee__name').annotate(total_days=Count('date')).order_by('employee__name')
    pyment_cont = pyment_record.values('employee__name').annotate(total_days=Count('date')).order_by('employee__name')

    unpaid_records = monthly_attendance.filter(ispyed=False)
    peyed_record = monthly_attendance.filter(ispyed=True).order_by('-date')[:5]
    count_all = attendance_records.count()
    count_pyed=pyment_record.count()


    check_date = False

    if from_date is not None:
        check_date = True

    


    




    total_paid_days = attendance_records.filter(ispyed=True).count()
    total_unpaid_days = attendance_records.filter(ispyed=False).count()

    difference = count_all - count_pyed 

    diffrence_check = True
    if difference >0:

        messages = "لديك %s يوم غير مدفوع" % difference

        diffrence_check = True
    elif difference == 0:
         messages = "الحساب مغلق "
         diffrence_check = False
    else:
        messages = "يوم  %s لنا عليك  " % difference

    









    context = {
        'employee': employee,
        'from_date': from_date,
        'to_date': to_date,
        'attendance': monthly_attendance,
        'attendance_records': attendance_records,
        'attendance_count': attendance_count,
        "pyment_cont":pyment_cont,
        "difference" : difference,
        'message': message,
        "messages":messages,
        'check': cheking,
        "check_date" :check_date,

        'calendar': month_days,
        'attendance_days': attendance_days,
        'attendance_status': attendance_status,
        'year': year,
        'month': month,
        'now': today,
        'month_name': month_start.strftime('%B'),
        'prev_year': (month_start - timedelta(days=1)).year,
        'prev_month': (month_start - timedelta(days=1)).month,
        'next_year': (month_end + timedelta(days=1)).year,
        'next_month': (month_end + timedelta(days=1)).month,
        'unpaid_records': unpaid_records,
        'peyed_record' : peyed_record, 
        "email": email,
        "diffrence_check":diffrence_check , 






    }
    
    return render(request, 'employe/serch_result.html', context)






def serch_result_new(request, id):
    email = request.user.email if request.user.is_authenticated else None
    today = timezone.now().date()
    # get the current employe 
    employee = get_object_or_404(Employee, id=id)



 # get the  pyments  
    pyments = EmployeePayment.objects.filter(employee=employee)
    
    # Get current year and month from request or default to current month
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month)
    
    # Gather attendance for the entire month
    month_start = datetime(year, month, 1)
    month_end = month_start + timedelta(days=calendar.monthrange(year, month)[1])
    monthly_attendance = Attendance.objects.filter(employee=employee, date__range=[month_start, month_end])
    
    # Create a set of days where attendance was recorded and their status
    attendance_days = set(att.date.day for att in monthly_attendance)
    attendance_status = {att.date.day: att.ispyed for att in monthly_attendance}
    
    # Check if attendance was recorded today
    attendance_today = Attendance.objects.filter(employee=employee, date=today).first()
    if attendance_today:
        message = "لقد تم تسجيل حضورك اليوم"
        cheking = True
    else:
        message = "لم يتم تسجيل حضورك اليوم"
        cheking = False
    
    # Get date range from request if available
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    
    if from_date and to_date:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
        attendance_records = Attendance.objects.filter(date__range=[from_date, to_date], employee=employee)
        payment_record = EmployeePayment.objects.filter(date__range=[from_date, to_date], employee=employee)

    else:
        attendance_records = Attendance.objects.filter(employee=employee)
        payment_record = EmployeePayment.objects.filter(employee=employee)


    
    attendance_count = attendance_records.values('employee__name').annotate(total_days=Count('date')).order_by('employee__name')
    pyment_cont = payment_record.values('employee__name').annotate(total_days=Count('date')).order_by('employee__name')

    unpaid_records = monthly_attendance.filter(ispyed=False)
    peyed_record = monthly_attendance.filter(ispyed=True).order_by('-date')[:5]
    count_all = attendance_records.count()
    count_pyed=payment_record.count()

    total_payments = payment_record.aggregate(total_amount=Sum('amount'))['total_amount'] or 0



    check_date = False

    if from_date is not None:
        check_date = True

    


    





    difference = count_all - count_pyed 

    diffrence_check = True
    if difference >0:

        messages = "لديك %s يوم غير مدفوع" % difference

        diffrence_check = True
    elif difference == 0:
         messages = "الحساب مغلق "
         diffrence_check = False
    else:
        messages = "يوم  %s لنا عليك  " % difference


    salary_details, total_salary = employee.calculate_salary_details()

   









    context = {
        'employee': employee,
        'from_date': from_date,
        'to_date': to_date,
        'attendance': monthly_attendance,
        'attendance_records': attendance_records,
        'attendance_count': attendance_count,
        "pyment_cont":pyment_cont,
        "difference" : difference,
        'message': message,
        "messages":messages,
        'check': cheking,
        "check_date" :check_date,

        'calendar': month_days,
        'attendance_days': attendance_days,
        'attendance_status': attendance_status,
        'year': year,
        'month': month,
        'now': today,
        'month_name': month_start.strftime('%B'),
        'prev_year': (month_start - timedelta(days=1)).year,
        'prev_month': (month_start - timedelta(days=1)).month,
        'next_year': (month_end + timedelta(days=1)).year,
        'next_month': (month_end + timedelta(days=1)).month,
        'unpaid_records': unpaid_records,
        'peyed_record' : peyed_record, 
        "email": email,
        "diffrence_check":diffrence_check,


        "pyments" : pyments,
        "total_payments" : total_payments,




        'salary_details': salary_details,
        'total_salary': total_salary,




    }
    
    return render(request, 'employe/serch_result_new.html', context)





def employee_report(request, id):
    employee = Employee.objects.get(id=id)

    # Get all payments for the employee
    payments = EmployeePayment.objects.filter(employee=employee)
    total_payments = payments.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    # Get attendance and calculate the total salary
    attendances = Attendance.objects.filter(employee=employee)
    salary_details, total_salary = employee.calculate_salary_details()

    context = {
        'employee': employee,
        'payments': payments,
        'total_payments': total_payments,
        'attendances': attendances,
        'salary_details': salary_details,
        'total_salary': total_salary,
    }

    return render(request, 'employe/report.html', context)





@login_required
def mark_as_paid(request, id):
    attendance = get_object_or_404(Attendance, id=id)
    attendance.ispyed = True
    attendance.save()
    return redirect(reverse('serch_result', kwargs={'id': attendance.employee.id}))
@login_required

def delete_payment(request, id):
    if request.method == 'POST':
        payment = get_object_or_404(EmployeePayment, id=id)
        payment.remove()
     
     
        messages.success(request, 'Payment deleted successfully.')
    return redirect('employee_payment_view', id=payment.employee.id)


def mark_as_not_pyed(request, id):








    attendance = get_object_or_404(Attendance, id=id)
    attendance.ispyed = False
    attendance.save()
    return redirect(reverse('serch_result', kwargs={'id': attendance.employee.id}))




@login_required
def pyments(request):
    email = request.user.email if request.user.is_authenticated else None

    

        
        # Fetch the oldest x attendance records for the employee
    



    attendance_counts = (Attendance.objects.filter(ispyed=False).values('employee__id', 'employee__name', 'employee__position' ,"employee__age" ).annotate(attendance_days=Count('date')).order_by('-attendance_days')
    )
    context = {
        'attendance': attendance_counts,
        'email': email,

    }
        

        
    
    # If not a POST request, render a template or handle the GET request as needed
    return render(request, 'employe/pyment_list.html', context)



@login_required
def mark_attendance_paid(request, id):
    email = request.user.email if request.user.is_authenticated else None

  
    employee = get_object_or_404(Employee, pk=id)
    attendance = Attendance.objects.filter(employee=employee)

    unpaid_records = attendance.filter(ispyed=False)
    peyed_record = attendance.filter(ispyed=True).order_by('-date')[:10]
    if request.method == 'POST':
        form = MarkPaidForm(request.POST)
        if form.is_valid():
            number_of_records = form.cleaned_data['number_of_records']
            oldest_attendance_records = Attendance.objects.filter(employee=employee, ispyed=False).order_by('date')[:number_of_records]
            
            # Update the records in a separate step
            with transaction.atomic():
                for record in oldest_attendance_records:
                    record.ispyed = True
                    record.save()

            return redirect('serch_result', id=employee.id)  # Redirect to the employee detail page
    else:
        form = MarkPaidForm()

    context = {
        'form': form, 
        'employee': employee,
        "unpaid_records":unpaid_records,
        "peyed_record":peyed_record,
        "email":email,

        
        }

    
    return render(request, 'employe/pyment.html',  context)

def mark_all_attendance_paid(request, id):
    employee = get_object_or_404(Employee, pk=id)
    Attendance.objects.filter(employee=employee, ispyed=False).update(ispyed=True)
    return redirect('serch_result', id=employee.id)  # Redirect to the employee detail page




def serch_resul(request, id):
    today = timezone.now().date()
 
    
    employee = get_object_or_404(Employee, id=id)
    
    # Fetch all attendance records for the employee
    attendance_records = Attendance.objects.filter(employee=employee).order_by('-date')


    
    # Check if attendance was recorded today
   

    # Get current year and month from request or default to current month
    year = request.GET.get('year', today.year)
    month = request.GET.get('month', today.month)
    
    year = int(year)
    month = int(month)
    
    cal = Calendar()
    month_days = cal.monthdayscalendar(year, month)

    # Gather attendance for the entire month
    month_start = datetime(year, month, 1)
    month_end = month_start + timedelta(days=calendar.monthrange(year, month)[1])
    monthly_attendance = Attendance.objects.filter(employee=employee, date__range=[month_start, month_end])

    # Create a set of days where attendance was recorded
    attendance_days = set(att.date.day for att in monthly_attendance)
    
    # Create a dictionary to store whether each day is paid or not
    attendance_status = {}
    for att in monthly_attendance:
        attendance_status[att.date.day] = att.ispyed # Assuming 'paid' is a boolean field in Attendance model

   
    if from_date and to_date:
        from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        attendance_records = Attendance.objects.filter(date__range=[from_date, to_date], employee=employee)
    else:
        attendance_records = Attendance.objects.filter(employee=employee)
    


 



    # Aggregate attendance count per employee
    attendance_count = attendance_records.values('employee__name').annotate(total_days=Count('date')).order_by('employee__name')
    context = {
       
        'from_date': from_date,
        'to_date': to_date,
        'attendance': attendance_records,
        'attendance_count': attendance_count,
        'employee': employee,
        'attendance_records': attendance_records,
 
 
        'calendar': month_days,
        'attendance_days': attendance_days,
        'attendance_status': attendance_status,  # Pass the dictionary to template
        'year': year,
        'month': month,
        'now': today,
        'month_name': month_start.strftime('%B'),
        'prev_year': (month_start - timedelta(days=1)).year,
        'prev_month': (month_start - timedelta(days=1)).month,
        'next_year': (month_end + timedelta(days=1)).year,
        'next_month': (month_end + timedelta(days=1)).month,
    }
    
    return render(request, 'employe/serch_resul.html', context)




def employ_login_view(request):
    if request.method == 'POST':
        form = LogingForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('today_attaned_admin')  # Replace 'home' with the name of your home page URL
    else:
        form = LogingForm()
    
    context = {
        'form': form,
    }
    return render(request, 'login.html', context)






def today_attaned(request):
     today = date.today()
     
     

        # Retrieve Attendance object or raise 404 if not found
     attendance = Attendance.objects.filter(date =today )



     context = {
        'attendance': attendance,
        'attendance_date': today,

    }



     return render(request, 'attendance/add_attend.html', context)

@login_required
def today_attaned_admin(request):
     email = request.user.email if request.user.is_authenticated else None
     today = date.today()
     
     

        # Retrieve Attendance object or raise 404 if not found
     attendance = Attendance.objects.filter(date =today )
     attendance_count = attendance.count()



     context = {
        'attendance': attendance,
        'attendance_date': today,
        'email' : email,
        'attendance_count' : attendance_count,

    }



     return render(request, 'attendance/add_attend_admin.html', context)


@login_required
def delete_attendance(request, id):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    
    attendance = get_object_or_404(Attendance, id=id)
    attendance.delete()
    return redirect('today_attaned_admin')




@login_required
def add_today(request):
     
    email = request.user.email if request.user.is_authenticated else None
    today = date.today()
    
    # Retrieve employees who have not attended today
    employees_not_attended_today = Employee.objects.filter(
        is_working=True
    ).exclude(
        attendance__date=today  # Assuming each attendance is linked to a user
    ).order_by('-state')
    
    context = {
        'employees_not_attended_today': employees_not_attended_today,
        'attendance_date': today,
        'email' : email
    }

    return render(request, 'attendance/adding.html', context)








@login_required
def add_attendance(request, id):
    email = request.user.email if request.user.is_authenticated else None
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
    

    
    return render(request, 'attendance/from_to.html', context)





def export_attendance_csv(request):
    # Create an HTTP response with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance_records.csv"'

    # Create a CSV writer object
    writer = csv.writer(response)
    
    # Write the header row
    writer.writerow(['ID', 'Employee', 'Date', 'Created By', 'Status', 'Is Paid'])

    # Write data rows
    for record in Attendance.objects.all().values_list('id', 'employee', 'date', 'created_by', 'status', 'ispyed'):
        writer.writerow(record)

    return response




# List View
def salary_list(request):
    form = Salary.objects.all()
    return render(request, 'salary/list.html', {'form': form})

# Create View
def salary_create(request):
    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('salary_list'))
    else:
        form = SalaryForm()
    return render(request, 'salary/add.html', {'form': form})

