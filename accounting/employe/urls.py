from django.urls import path
from  . import views



urlpatterns = [
   path('calendar/', views.calendar_view, name='calendar'), #clander view 

    # take the date from the clander
    path('attendance/<int:year>/<int:month>/<int:day>/', views.attendance_view, name='attendance'),

#add new employee
    path('add/' , views.add_employee , name="add_employe"),



    path('list/' , views.employee_list_view , name="employee_list_view"),
    path('edit/<int:id>/' , views.edit_employee , name="edit_employee"),
        path('' , views.today_attaned , name="today_attaned"),
       path('attendance/add/<int:id>/', views.add_attendance, name='add_attendance'),


    path('today/add/' , views.add_today , name="add_today"),
    path('last/weak/' , views.last_week_attendance , name="last_week_attendance"),
    path('last/month/' , views.last_month_attendance , name="last_week_attendance"),
    path('from/to/', views.attendance_views, name='attendance_from_to'),
    path('search/', views.tc_input_view, name='tc_input_view'),
    
    path('employee/<int:id>/', views.serch_result, name='serch_result'),
     path('employe/<int:id>/', views.serch_resul, name='serch_resul'),
   

 path('login/', views.employ_login_view, name='employ_login_view'),
    
  
  path('today/' , views.today_attaned_admin , name="today_attaned_admin"),
  path('delete-attendance/<int:id>/', views.delete_attendance, name='delete_attendance'),
 path('attend/payed/<int:id>/', views.mark_as_paid, name='mark_as_paid'),
    
     path('attend/pyed/not/<int:id>/', views.mark_as_not_pyed, name='mark_as_not_pyed'),
         



# urls.py
path('pyment/<int:x>/<int:id>/', views.pyment, name='pyment'),



    
    
  #  path('date/', views.date_picker_view, name='date_view'),




    path('pyment/<int:id>/', views.mark_attendance_paid, name='mark_attendance_paid'),
    path('pyment/all/<int:id>/',views.mark_all_attendance_paid, name='mark_all_attendance_paid'),
]



