from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import University, Department, Order

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

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
		super().__init__(*args, **kwargs)
		self.fields['university'].label = "Ίδρυμα:"

class DepartmentForm(forms.Form):
	department = UniversityChoiceField(queryset = Department.objects.all())

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['department'].label = "Ίδρυμα:"
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