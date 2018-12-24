from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import University, Department, Order

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

	def __init__(self, *args, **kwargs):
		super(UserRegisterForm, self).__init__(*args, **kwargs)
		self.fields['username'].help_text = None
		self.fields['email'].label = "Διεύθυνση Email"
		self.fields['password1'].label = "Κωδικός Πρόσβασης"
		self.fields['password1'].help_text = "Ο κωδικός σας θα πρέπει να αποτελείται από τουλάχιστον 8 χαρακτήρες"
		self.fields['password2'].label = "Επαλήθευση Κωδικού Πρόσβασης"
		self.fields['password2'].help_text = "Εισάγετε τον ίδιο κωδικό με πριν, για επαλήθευση"

class ContactForm(forms.Form):
	from_email = forms.EmailField(required=True)
	subject = forms.CharField(required=True)
	message = forms.CharField(widget=forms.Textarea, required=True)

	def __init__(self, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)
		self.fields['subject'].label = "Θέμα:"
		self.fields['from_email'].label = "Email:"
		self.fields['message'].label = "Περιεχόμενο:"

class UniversityChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.title

class UniversityForm(forms.Form):
	university = UniversityChoiceField(queryset = University.objects.all())

	def __init__(self, *args, **kwargs):
		super(UniversityForm, self).__init__(*args, **kwargs)
		self.fields['university'].label = "Επιλέξτε Ίδρυμα:"

class DepartmentForm(forms.Form):
	department = UniversityChoiceField(queryset = Department.objects.all())

	def __init__(self, *args, **kwargs):
		super(DepartmentForm, self).__init__(*args, **kwargs)
		self.fields['department'].label = "Επιλέξτε Τμήμα:"

SEMESTERS = (
	(0, '1ο Εξάμηνο'),
	(1, '2ο Εξάμηνο'),
	(2, '3ο Εξάμηνο'),
	(3, '4ο Εξάμηνο'),
	(4, '5ο Εξάμηνο'),
	(5, '6ο Εξάμηνο'),
	(6, '7ο Εξάμηνο'),
	(7, '8ο Εξάμηνο'),
	(8, '9ο Εξάμηνο'),
	(9, '10ο Εξάμηνο'),
)

class SemesterPicker(forms.Form):
	semester = forms.MultipleChoiceField(choices=SEMESTERS, required=True, widget=forms.CheckboxSelectMultiple)

	def __init__(self, *args, **kwargs):
		super(SemesterPicker, self).__init__(*args, **kwargs)
		self.fields['semester'].label = "Επιλέξτε Εξάμηνα:"

class ClassForm(forms.Form):
	lesson = forms.MultipleChoiceField()


# class OrderForm(forms.ModelForm):
	
# 	class Meta:
# 		model = Order
# 		fields = ['uni', 'dept']

# 	def __init__(self, *args, **kwargs):
# 		super().__init__(*args, **kwargs)
# 		self.fields['uni'].label = "Ίδρυμα:"
# 		self.fields['dept'].label = "Τμήμα:"
# 		self.fields['uni'].queryset = University.objects.all()
# 		self.fields['dept'].queryset = Department.objects.none()