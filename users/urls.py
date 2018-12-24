from django.urls import path
from . import views
from . import forms

named_order_forms = (
    ('unidata', forms.UniversityForm),
    ('deptsata', forms.DepartmentForm),
)

order_wizard = views.OrderWizard.as_view(named_order_forms)

urlpatterns = [
    path('', views.home, name='users-home'),
    path('about/', views.about, name='users-about'),
    #path('order/', views.order, name='users-order'),
    path('exchange/', views.exchange, name='users-exchange'),
    path('announcements/', views.announcements, name='users-announcements'),
    path('contact/', views.contact, name='users-contact'),
    path('order/', order_wizard, name='users-order')
]
