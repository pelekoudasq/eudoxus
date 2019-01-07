from . import forms
from . import views
from django.urls import path
from formtools.wizard.views import SessionWizardView

named_order_forms = (
    ('unidata', forms.UniversityForm),
    ('deptdata', forms.DepartmentForm),
    ('semdata', forms.SemesterPicker),
    ('classes', forms.ClassForm),
    ('books', forms.BookFormset),
    ('final', forms.FinalFormset),
)

named_display_forms = (
	('unidata', forms.UniversityForm),
    ('deptdata', forms.DepartmentForm),
    ('classes', forms.ClassFormDisplay),
    ('books', forms.BookForm),
)

order_wizard = views.OrderWizard.as_view(named_order_forms)
display_wizard = views.DisplayWizard.as_view(named_display_forms)

urlpatterns = [
    path('', views.home, name='users-home'),
    path('about/', views.about, name='users-about'),
    path('publisher/', views.publisher, name='users-publisher'),
    path('student/', views.student, name='users-student'),
    path('exchange/', views.exchange, name='users-exchange'),
    path('announcements/', views.announcements, name='users-announcements'),
    path('contact/', views.contact, name='users-contact'),
    path('search/', views.search, name='users-search'),
    path('order/', order_wizard, name='users-order'),
    path('display/', display_wizard, name='users-display'),
    path('profile/edit/', views.edit_profile, name='users-edit'),
]
