from django.urls import path
from.views import *
from django.contrib.auth import views as auth_views
urlpatterns =[
    path('register/',register,name="register"),
    path('',log_in,name="login"),
    path('logout/',log_out,name="logout"),
    path('change/',change,name='change'),
    


    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),

    path('profile',profile,name='profile'),
    path('dashboard',profile_dashboard,name='dashboard'),
    path('my_orders',my_orders,name='my_orders')

    

]