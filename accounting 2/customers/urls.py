from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.customer_login, name='customer_login'),
    path('panel/', views.customer_panel, name='customer_panel'),
    path('logout/', views.customer_logout, name='customer_logout'),
    path('edit/' , views.update_cosomer , name="update_cosomer"),
    path('bill/' , views.fetch_bills_list , name="fetch_bills_list"),
    path('bill/<int:id>' , views.view_bill , name="view_bill"),
 
    path('test/' , views.testt , name="test"),

]
