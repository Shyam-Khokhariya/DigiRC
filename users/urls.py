from django.urls import path
from . import views

urlpatterns = [
    path('register/<usertype>', views.register, name='register'),
    path('login/<usertype>', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('forgot-password/', views.password_reset, name='forgot-password'),
]
