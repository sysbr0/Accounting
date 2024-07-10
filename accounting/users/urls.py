from django.urls import path
from  . import views


urlpatterns = [

          path('',views.user_profile, name='user'),
          path('signup/', views.user_signup, name='signup'),
          path('login', views.user_login, name='login'),
          path('logout/', views.user_logout, name='logout'),
          path('loogin/' , views.login)

]