from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import formset_factory
from users.models import *


############### * REGISTRATION * ###############

USER_TYPES = (
	(1, 'Φοιτητής/τρια'),
	(2, 'Εκδότης'),
	(3, 'Διανομέας Συγγραμάτων'),
	(4, 'Γραμματεία'),
)

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	user_type = forms.ChoiceField(choices=USER_TYPES, required=True)

	class Meta:
		model = User
		fields = ['username', 'email', 'user_type', 'password1', 'password2']

	def __init__(self, *args, **kwargs):
		super(UserRegisterForm, self).__init__(*args, **kwargs)
		self.fields['username'].help_text = None
		self.fields['email'].label = "Διεύθυνση Email"
		self.fields['password1'].label = "Κωδικός Πρόσβασης"
		self.fields['password1'].help_text = "Ο κωδικός σας θα πρέπει να αποτελείται από τουλάχιστον 8 χαρακτήρες"
		self.fields['password2'].label = "Επαλήθευση Κωδικού Πρόσβασης"
		self.fields['user_type'].label = "Χρησιμοποιώ τον Εύδοξο ως"
		self.fields['password2'].help_text = "Εισάγετε τον ίδιο κωδικό με πριν, για επαλήθευση"

class UpdateUser(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

	def __init__(self, *args, **kwargs):
		super(UpdateUser, self).__init__(*args, **kwargs)
		self.fields['username'].help_text = None
		self.fields['email'].label = "Διεύθυνση Email"
		self.fields['password1'].label = "Κωδικός Πρόσβασης"
		self.fields['password1'].help_text = "Ο κωδικός σας θα πρέπει να αποτελείται από τουλάχιστον 8 χαρακτήρες"
		self.fields['password2'].label = "Επαλήθευση Κωδικού Πρόσβασης"
		self.fields['password2'].help_text = "Εισάγετε τον ίδιο κωδικό με πριν, για επαλήθευση"

################### * ADDITIONAL INFO * ##################################

class StudentAdditionalInfo(forms.ModelForm):

	class Meta:
		model = Student
		fields = ['uni', 'dept']

	def __init__(self, *args, **kwargs):
		super(StudentAdditionalInfo, self).__init__(*args, **kwargs)
		self.fields['uni'].label = "Επιλέξτε το Ίδρυμά σας:"
		self.fields['dept'].label = "Επιλέξτε το Τμήμα σας:"
		# self.fields['dept'].queryset = Department.objects.none()

class PublisherAdditionalInfo(forms.ModelForm):

	class Meta:
		model = Publisher
		fields = ['title']

	def __init__(self, *args, **kwargs):
		super(PublisherAdditionalInfo, self).__init__(*args, **kwargs)
		self.fields['title'].label = "Εισάγετε την Επωνυμία σας:"

class DistributorAdditionalInfo(forms.ModelForm):

	class Meta:
		model = Distributor
		fields = ['title']

	def __init__(self, *args, **kwargs):
		super(DistributorAdditionalInfo, self).__init__(*args, **kwargs)
		self.fields['title'].label = "Εισάγετε την Επωνυμία σας:"

class SecretaryAdditionalInfo(forms.ModelForm):

	class Meta:
		model = Distributor
		fields = ['title']

	def __init__(self, *args, **kwargs):
		super(SecretaryAdditionalInfo, self).__init__(*args, **kwargs)
		self.fields['title'].label = "Εισάγετε τον τίτλο της γραμματείας:"

#################################################################################

class UpdateProfile(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']

	def save(self, commit=True):
		user = super(UserRegisterForm, self).save(commit=False)

		if commit:
			user.save()

		return user

	def __init__(self, *args, **kwargs):
		super(UpdateProfile, self).__init__(*args, **kwargs)
		self.fields['username'].help_text = None
		self.fields['email'].label = "Διεύθυνση Email"

class ContactForm(forms.Form):
	from_email = forms.EmailField(required=True)
	subject = forms.CharField(required=True)
	message = forms.CharField(widget=forms.Textarea, required=True)

	def __init__(self, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)
		self.fields['subject'].label = "Θέμα:"
		self.fields['from_email'].label = "Email:"
		self.fields['message'].label = "Περιεχόμενο:"




################### * ORDER WIZARDS * ######################

class UniversityChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return obj.title

class UniversityForm(forms.Form):
	university = UniversityChoiceField(queryset = University.objects.all().order_by('title'))

	def __init__(self, *args, **kwargs):
		super(UniversityForm, self).__init__(*args, **kwargs)
		self.fields['university'].label = "Επιλέξτε Ίδρυμα:"
		self.fields['university'].empty_label = None

class DepartmentForm(forms.Form):
	department = UniversityChoiceField(queryset = Department.objects.all())

	def __init__(self, *args, **kwargs):
		super(DepartmentForm, self).__init__(*args, **kwargs)
		self.fields['department'].label = "Επιλέξτε Τμήμα:"
		self.fields['department'].empty_label = None

SEMESTERS = (
	(1, '1ο Εξάμηνο'),
	(2, '2ο Εξάμηνο'),
	(3, '3ο Εξάμηνο'),
	(4, '4ο Εξάμηνο'),
	(5, '5ο Εξάμηνο'),
	(6, '6ο Εξάμηνο'),
	(7, '7ο Εξάμηνο'),
	(8, '8ο Εξάμηνο'),
	(9, '9ο Εξάμηνο'),
	(10, '10ο Εξάμηνο'),
)

class SemesterPicker(forms.Form):
	semester = forms.MultipleChoiceField(choices=SEMESTERS, required=True, widget=forms.CheckboxSelectMultiple)

	def __init__(self, *args, **kwargs):
		super(SemesterPicker, self).__init__(*args, **kwargs)
		self.fields['semester'].label = "Επιλέξτε Εξάμηνα:"

class ClassChoiceField(forms.ModelMultipleChoiceField):
	def label_from_instance(self, obj):
		return obj.title

class ClassForm(forms.Form):
	lesson = ClassChoiceField(queryset=Class.objects.all(), required=True, widget=forms.CheckboxSelectMultiple)

	def __init__(self, *args, **kwargs):
		super(ClassForm, self).__init__(*args, **kwargs)
		self.fields['lesson'].label = "Επιλέξτε Μαθήματα:"

#class for display only
class ClassFormDisplay(forms.Form):
	lesson = UniversityChoiceField(queryset=Class.objects.all())

	def __init__(self, *args, **kwargs):
		super(ClassFormDisplay, self).__init__(*args, **kwargs)
		self.fields['lesson'].label = "Επιλέξτε Μάθημα:"

class BookChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return obj.title+", "+obj.author

class BookForm(forms.Form):
	book = BookChoiceField(queryset = Book.objects.all(), required=True, widget=forms.RadioSelect, empty_label=None)

	def __init__(self, *args, **kwargs):
		super(BookForm, self).__init__(*args, **kwargs)
		self.fields['book'].label = "Επιλέξτε Συγγράμματα:"
		self.fields['book'].widget.attrs.update({'class' : 'text-muted'})

BookFormset = formset_factory(BookForm, extra=1)

RECEIPT = (
	(1, 'Παραλαβή από Σημείο Διανομής'),
	(2, 'Παραλαβή από Φοιτητή'),
	(3, 'Αποστολή στο σπίτι'),
)

class OrderFinal(forms.Form):
	way_of_receipt = forms.ChoiceField(choices=RECEIPT, required=True, widget=forms.RadioSelect)

	def __init__(self, *args, **kwargs):
		super(OrderFinal, self).__init__(*args, **kwargs)
		#self.initial['way_of_receipt'] = RECEIPT[1]

FinalFormset = formset_factory(OrderFinal, extra=1)


############## distribution ###############

class BookGiveChoiceField(forms.ModelMultipleChoiceField):
	def label_from_instance(self, obj):
		return obj.title+", Διαθεσιμότητα: "+str(obj.avail)

class GiveBook(forms.Form):
	books = BookGiveChoiceField(queryset=Book.objects.all(), required=True, widget=forms.CheckboxSelectMultiple)

	def __init__(self, *args, **kwargs):
		super(GiveBook, self).__init__(*args, **kwargs)
		self.fields['books'].label = "Επιλέξτε τα Συγγράμματα για παράδοση:"
