from django.urls import path
from  . import views


urlpatterns = [

         path('test/',views.test, name='test'),
         path('clint/',views.clint_list, name='clints'),
         path('clint/add/',views.add_clint, name='addclint'),
         path('clint/<int:id>/',views.fatch_clint, name='fatch_clint'),
          path('clint/delete/<int:id>/', views.delete_clint, name='delete_clint'),
          path('clint/update/<int:id>/', views.update_clint, name='update_clint'),
          path('clint/uplode/' ,views.upload_clients , name="upload_clients"),
           path('clints/download-csv/',views.download_clints_csv, name='download_clints_csv'),



]
