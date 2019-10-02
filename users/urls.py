from django.urls import path
from . import views

urlpatterns = [
    path('register/manufacturer', views.manu_register, name='register-manufacturer'),
    path('register/dealer', views.dealer_register, name='register-dealer'),
    path('register/buyer', views.buyer_register, name='register-buyer'),
    path('login/<usertype>', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('forgot-password/', views.password_reset, name='forgot-password'),
]
