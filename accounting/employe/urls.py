from django.urls import path
from  . import views



urlpatterns = [
   path('calendar/', views.calendar_view, name='calendar'),
    path('attendance/', views.attendance_detail_view, name='attendance_detail'),
    
    path('attendance/<int:year>/<int:month>/<int:day>/', views.attendance_view, name='attendance'),


    path('add/' , views.add_employee , name="add_employe"),
    path('list/' , views.employee_list_view , name="employee_list_view"),
    path('edit/<int:id>/' , views.edit_employee , name="edit_employee"),
        path('today/' , views.today_attaned , name="today_attaned"),
       path('attendance/add/<int:id>/', views.add_attendance, name='add_attendance'),


    path('today/add/' , views.add_today , name="add_today"),
    path('last/weak/' , views.last_week_attendance , name="last_week_attendance"),
    path('last/month/' , views.last_month_attendance , name="last_week_attendance"),
    path('from/to/', views.attendance_views, name='attendance_from_to'),
    path('search/', views.tc_input_view, name='tc_input_view'),
    
    path('employee/<int:id>/', views.serch_result, name='serch_result'),
      
    #path('calendar/<int:id>/', views.searching_result, name='serching_result'),
    



    
        

    
    
  #  path('date/', views.date_picker_view, name='date_view'),

]
