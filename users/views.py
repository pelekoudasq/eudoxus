from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.models import Group, Permission
from django.utils.decorators import method_decorator
from django.db.models import Q
from formtools.wizard.views import SessionWizardView
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from .forms import *
from users.models import University, Department, Class, Book, Student, Order, Publisher, Distributor, Secretary
import logging
logr = logging.getLogger(__name__)
# Create your views here.

def home(request):
	query = request.GET.get("q")
	if query:
		queryset_list = Book.objects.all()
		queryset_list = queryset_list.filter(Q(title__icontains=query)|Q(author__icontains=query)|Q(isbn__icontains=query)|Q(pub__title__icontains=query)).distinct()
		return render(request, 'users/search.html', {'results':queryset_list, 'requested':query, 'len':len(queryset_list)})
	return render(request, 'users/home.html', {'title': 'Home'})

def about(request):
	return render(request, 'users/about.html', {'title': 'About'})

def student(request):
	return render(request, 'users/student.html', {'title': 'Student'})

@login_required
def publisher(request):
	return render(request, 'users/publisher.html', {'title': 'Publisher'})

def announcements(request):
	return render(request, 'users/announcements.html', {'title': 'Announcements'})

def contact(request):
	return render(request, 'users/contact.html', {'title': 'Contact'})

@login_required
def exchange(request):
	return render(request, 'users/exchange.html', {'title': 'Exchange'})


class DisplayWizard(AccessMixin, SessionWizardView):
	template_name = "users/display.html"

	def get_form(self, step=None, data=None, files=None):
		form = super(DisplayWizard, self).get_form(step, data, files)
		
		if step is None:
			step = self.steps.current

		if step == 'deptdata':
			prev_data = self.get_cleaned_data_for_step('unidata')['university'].id
			form.fields['department'].queryset = Department.objects.filter(uni=prev_data)
		elif step == 'classes':
			dept = self.get_cleaned_data_for_step('deptdata')['department'].id
			form.fields['lesson'].queryset = Class.objects.filter(dept=dept)
		elif step == 'books':
			classes = self.get_cleaned_data_for_step('classes')['lesson']
			form.fields['book'].queryset = classes.books.all()
			form.fields['book'].widget.attrs['readonly'] = "readonly"

		return form

	def done(self, form_list, **kwargs):
		form_data = process_form_data(form_list)
		print (form_data)
		# messages.success(request, f'{form_data} επιλέχθηκαν')
		return redirect('profile')

class OrderWizard(SessionWizardView):
	template_name = "users/order.html"

	#@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		response = super(OrderWizard, self).dispatch(request, *args, **kwargs)

		# if self.steps.current == 'final':
		# 	if not request.user.is_authenticated:
		# 		return HttpResponseForbidden()

		return response

	def get_form(self, step=None, data=None, files=None):
		form = super(OrderWizard, self).get_form(step, data, files)

		if step is None:
			step = self.steps.current

		if self.request.user.is_authenticated:
			student = Student.objects.filter(user=self.request.user).first()
			if step == 'unidata':
				form.fields['university'].queryset = University.objects.filter(id=student.uni.id)
			elif step == 'deptdata':
				form.fields['department'].queryset = Department.objects.filter(id=student.dept.id)
		else:
			if step == 'deptdata':
				prev_data = self.get_cleaned_data_for_step('unidata')['university'].id
				form.fields['department'].queryset = Department.objects.filter(uni=prev_data)
		
		if step == 'classes':
			dept = self.get_cleaned_data_for_step('deptdata')['department'].id
			sems = self.get_cleaned_data_for_step('semdata')['semester']
			form.fields['lesson'].queryset = Class.objects.filter(dept=dept, semester__in=sems)
		elif step == 'books':
			classes = self.get_cleaned_data_for_step('classes')
			classes = self.get_cleaned_data_for_step('classes')['lesson']
			form.extra = len(classes)
			for i in range(len(classes)):
				form.forms[i].fields['book'].label = classes[i]
				form.forms[i].fields['book'].queryset = classes[i].books.all()
		elif step == 'final':
			books = self.get_cleaned_data_for_step('books')
			form.extra = len(books)
			for i in range(len(books)):
				form.forms[i].fields['way_of_receipt'].label = books[i]['book']
		return form
	
	def done(self, form_list, **kwargs):
		form_data = process_form_data(form_list)
		print(form_data)
		books = self.get_cleaned_data_for_step('books')
		order = Order()
		order.user = self.request.user
		order.save()
		print(books[0]['book'])
		for book in books:
			order.books.add(book['book'])
		# messages.success(request, f'{form_data} επιλέχθηκαν')
		return redirect('profile')

def process_form_data(form_list):
	form_data = [form.cleaned_data for form in form_list]
	return form_data




def search(request):
	query = request.GET.get("q")
	if query:
		queryset_list = Book.objects.all()
		queryset_list = queryset_list.filter(Q(title__icontains=query)|Q(author__icontains=query)|Q(isbn__icontains=query)|Q(pub__title__icontains=query)).distinct().order_by('title')
		return render(request, 'users/search.html', {'results':queryset_list, 'requested':query, 'len':len(queryset_list)})
	return render(request, 'users/search.html', {'title': 'Search'})



@login_required
def profile(request):
	args = {}
	if request.user.groups.all()[0].name == 'students':
		print("STUDENT")
		#get student info
		student = Student.objects.filter(user=request.user).first()
		args['student'] = student
		#get student's orders
		orders = Order.objects.filter(user=request.user)
		args['orders'] = orders
	elif request.user.groups.all()[0].name == 'publishers':
		print("PUBLISHER")
		info = Publisher.objects.filter(user=request.user).first()
		args['info'] = info
	elif request.user.groups.all()[0].name == 'distributors':
		print("DISTR")
		info = Distributor.objects.filter(user=request.user).first()
		args['info'] = info
	else:
		print("SECR")
		info = Secretary.objects.filter(user=request.user).first()
		args['info'] = info
	return render(request, 'users/profile.html', args)

@login_required
def additional_register(request):
	if request.method == 'POST':
		if request.user.groups.all()[0].name == 'students':
			form = StudentAdditionalInfo(request.POST)
			student = form.save(commit=False)
			student.user = request.user
			student.save()
		elif request.user.groups.all()[0].name == 'publishers':
			form = PublisherAdditionalInfo(request.POST)
			publisher = form.save(commit=False)
			publisher.user = request.user
			publisher.save()
		elif request.user.groups.all()[0].name == 'distributors':
			form = DistributorAdditionalInfo(request.POST)
			distributor = form.save(commit=False)
			distributor.user = request.user
			distributor.save()
		elif request.user.groups.all()[0].name == 'secretaries':
			form = SecretaryAdditionalInfo(request.POST)
			secretary = form.save(commit=False)
			secretary.user = request.user
			secretary.save()
		return redirect('users-home')
	else:
		if request.user.groups.all()[0].name == 'students':
			form = StudentAdditionalInfo()
		elif request.user.groups.all()[0].name == 'publishers':
			form = PublisherAdditionalInfo()
		elif request.user.groups.all()[0].name == 'distributors':
			form = DistributorAdditionalInfo()
		elif request.user.groups.all()[0].name == 'secretaries':
			form = SecretaryAdditionalInfo()
	return render(request, 'users/additional.html', {'form': form})


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			group_selected = form.cleaned_data.get('user_type')
			group = Group.objects.get(id=group_selected)
			user.groups.add(group)
			username = form.cleaned_data.get('username')
			messages.success(request, f'{username}, ο λογαριασμός σας δημιουργήθηκε με επιτυχία!')
			new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
			login(request, new_user)
			return redirect('additional')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form': form})


def contact(request):
	if request.method == 'GET':
		form = ContactForm()
	else:
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = form.cleaned_data['subject']
			from_email = form.cleaned_data['from_email']
			message = form.cleaned_data['message']
			try:
				send_mail(subject, message, from_email, ['peleioannis@gmail.com'])
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
		messages.success(request, f'Το μήνυμά σας εστάλη με επιτυχία, ευχαριστούμε για την επικοινωνία!')
		return redirect('users-home')
	return render(request, "users/contact.html", {'form': form})

def edit_profile(request):
	user = request.user
	if request.method == 'GET':
		fields = ['username', 'email', 'password1', 'password2']
		form1 = UpdateUser(instance=user)
		if request.user.groups.all()[0].name == 'students':
			student = Student.objects.get(user=user)
			form2 = StudentAdditionalInfo(instance=student)
		elif request.user.groups.all()[0].name == 'publishers':
			publisher = Publisher.objects.get(user=user)
			form2 = PublisherAdditionalInfo(instance=publisher)
		elif request.user.groups.all()[0].name == 'distributors':
			distributor = Distributor.objects.get(user=user)
			form2 = DistributorAdditionalInfo(instance=publisher)
		elif request.user.groups.all()[0].name == 'secretaries':
			secretary = Secretary.objects.get(user=user)
			form2 = SecretaryAdditionalInfo(instance=secretary)
		return render(request, "users/edit.html", {'form1' : form1, 'form2' : form2})
	else:
		form1 = UpdateUser(request.POST, instance=user)
		form1.save()
		form2 = 1
		if request.user.groups.all()[0].name == 'students':
			student = Student.objects.get(user=user)
			form2 = StudentAdditionalInfo(request.POST, instance=student)
		elif request.user.groups.all()[0].name == 'publishers':
			publisher = Publisher.objects.get(user=user)
			form2 = PublisherAdditionalInfo(request.POST, instance=publisher)
		elif request.user.groups.all()[0].name == 'distributors':
			distributor = Distributor.objects.get(user=user)
			form2 = DistributorAdditionalInfo(request.POST, instance=publisher)
		elif request.user.groups.all()[0].name == 'secretaries':
			secretary = Secretary.objects.get(user=user)
			form2 = SecretaryAdditionalInfo(request.POST, instance=secretary)
		form2.save()
		messages.success(request, f'Οι αλλαγές στο προφίλ σας ολοκληρώθηκαν!')
		return redirect('profile')