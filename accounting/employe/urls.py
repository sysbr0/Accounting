from django.urls import path
from  . import views



urlpatterns = [
   path('calendar/', views.calendar_view, name='calendar'),
    path('attendance/', views.attendance_detail_view, name='attendance_detail'),
    
    path('attendance/<int:year>/<int:month>/<int:day>/', views.attendance_view, name='attendance'),


    path('add/' , views.add_employee , name="add_employe"),
    path('list/' , views.employee_list_view , name="employee_list_view"),
    path('edit/<int:id>/' , views.edit_employee , name="edit_employee"),
    
  #  path('date/', views.date_picker_view, name='date_view'),

]