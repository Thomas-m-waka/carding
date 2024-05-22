from . import views 
from django.urls import path

urlpatterns = [
    path('',views.register,name='register'),
    path('login',views.login_view,name='login'),
    path('home',views.home,name='home'),
    path('logout/',views.logout_view, name='logout'),
    path('reset_password', views.reset_password, name="reset-password"),
    
    path('enter_username', views.enter_username, name="enter-username"),
    path('get_phone', views.get_phone, name="get-phone"),
    path('send_verification_code', views.send_verification_code, name="send-code"),
    path('enter_verification_code', views.enter_verification_code, name="enter-code"),
   
    
    path('users', views.admin_user_list, name='admin_user_list'),

]