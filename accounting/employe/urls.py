from django.urls import path
from  . import views



urlpatterns = [
   path('calendar/', views.calendar_view, name='calendar'), #clander view 

    # take the date from the clander
    path('attendance/<int:year>/<int:month>/<int:day>/', views.attendance_view, name='attendance'),


    

#add new employee



    path('list/' , views.employee_list_view , name="employee_list_view"),
    path('edit/<int:id>/' , views.edit_employee , name="edit_employee"),
        path('' , views.today_attaned , name="today_attaned"),
       path('attendance/add/<int:id>/', views.add_attendance, name='add_attendance'),


    path('last/weak/' , views.last_week_attendance , name="last_week_attendance"),
    path('last/month/' , views.last_month_attendance , name="last_week_attendance"),
    path('from/to/', views.attendance_views, name='attendance_from_to'),
    path('search/', views.tc_input_view, name='tc_input_view'),
    
    path('employee/<int:id>/', views.serch_result, name='serch_result'),
     path('employe/<int:id>/', views.serch_resul, name='serch_resul'),
   

 path('login/', views.employ_login_view, name='employ_login_view'),
    
  
  path('today/' , views.today_attaned_admin , name="today_attaned_admin"),


# urls.py
path('admin/pyment/', views.pyment, name='pyment'),



    
    
  #  path('date/', views.date_picker_view, name='date_view'),







    path('admin/list/' , views.employee_list_view , name="employee_list_view"),


#

  path('admin/attendance/<int:year>/<int:month>/<int:day>/', views.attendance_view_admin, name='attendance_view_admin'),
    path('admin/paid/not/<int:id>/', views.mark_as_not_pyed, name='mark_as_not_pyed'),
     path('admin/paid/<int:id>/', views.mark_as_paid, name='mark_as_paid'),

    path('admin/pyment/<int:id>/', views.mark_attendance_paid, name='mark_attendance_paid'),
    path('admin/pyment/all/<int:id>/',views.mark_all_attendance_paid, name='mark_all_attendance_paid'),



# path('employ/<int:employee_id>/', views.employee_detail, name='employee_detail'),
 



      path('admin/attendance/delete/<int:id>/', views.delete_attendance, name='delete_attendance'),

 
  path('admin/today/' , views.today_attaned_admin , name="today_attaned_admin"),
      path('admin/today/add/' , views.add_today , name="add_today"),
         path('admin/calendar/', views.calendar_view, name='calendar'), #clander view 
            path('admin/add/' , views.add_employee , name="add_employe"),


       path('chat/<int:id>/', views.chat_view, name='chat_view'),

       path('chat/', views.admin_chat, name='admin_chat'),

       





            




    
         

]



