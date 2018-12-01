from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='users-home'),
    path('about/', views.about, name='users-about'),
    path('exchange/', views.exchange, name='users-exchange'),
    path('announcements/', views.announcements, name='users-announcements'),
    path('contact/', views.contact, name='users-contact'),
]
