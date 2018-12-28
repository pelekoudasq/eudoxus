from django.urls import path
from . import views
from . import forms
from formtools.wizard.views import SessionWizardView

initial = {
	#'1': {views.OrderWizard.get_cleaned_data_for_step(0)},
}

named_order_forms = (
    ('unidata', forms.UniversityForm),
    ('deptdata', forms.DepartmentForm),
    ('semdata', forms.SemesterPicker),
    ('classes', forms.ClassForm),
    ('books', forms.BookForm),
)

named_display_forms = (
	('unidata', forms.UniversityForm),
    ('deptdata', forms.DepartmentForm),
    ('classes', forms.ClassFormDisplay),
    ('books', forms.BookForm),
)

order_wizard = views.OrderWizard.as_view(named_order_forms, initial_dict=initial)
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
]
