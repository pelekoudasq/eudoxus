from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.models import Group, Permission
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from formtools.wizard.views import SessionWizardView
from users.models import *
import logging
logr = logging.getLogger(__name__)

def home(request):

	#search handler
	query = request.GET.get("q")
	if query:
		queryset_list = Book.objects.all()
		queryset_list = queryset_list.filter(Q(title__icontains=query)|Q(author__icontains=query)|Q(isbn__icontains=query)|Q(pub__title__icontains=query)).distinct()
		return render(request, 'users/search.html', {'results':queryset_list, 'requested':query, 'len':len(queryset_list)})
	#end of search handler
	else:
		return render(request, 'users/home.html', {'title': 'Αρχική'})

def about(request):

	#search handler
	query = request.GET.get("q")
	if query:
		queryset_list = Book.objects.all()
		queryset_list = queryset_list.filter(Q(title__icontains=query)|Q(author__icontains=query)|Q(isbn__icontains=query)|Q(pub__title__icontains=query)).distinct()
		return render(request, 'users/search.html', {'results':queryset_list, 'requested':query, 'len':len(queryset_list)})
	#end of search handler
	else:
		return render(request, 'users/about.html', {'title': 'Βοήθεια'})

def announcements(request):
	#search handler
	query = request.GET.get("q")
	if query:
		queryset_list = Book.objects.all()
		queryset_list = queryset_list.filter(Q(title__icontains=query)|Q(author__icontains=query)|Q(isbn__icontains=query)|Q(pub__title__icontains=query)).distinct()
		return render(request, 'users/search.html', {'results':queryset_list, 'requested':query, 'len':len(queryset_list)})
	#end of search handler

	return render(request, 'users/announcements.html', {'title': 'Ανακοινώσεις'})


############### * CONTACT * ###############

def contact(request):

	#search handler
	query = request.GET.get("q")
	if query:
		queryset_list = Book.objects.all()
		queryset_list = queryset_list.filter(Q(title__icontains=query)|Q(author__icontains=query)|Q(isbn__icontains=query)|Q(pub__title__icontains=query)).distinct()
		return render(request, 'users/search.html', {'results':queryset_list, 'requested':query, 'len':len(queryset_list)})
	#end of search handler

	#contact form
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


############### * DISTRIBUTION PROCESS * ###############

def distribution(request):

	#search handler
	query = request.GET.get("q")
	if query:
		queryset_list = Book.objects.all()
		queryset_list = queryset_list.filter(Q(title__icontains=query)|Q(author__icontains=query)|Q(isbn__icontains=query)|Q(pub__title__icontains=query)).distinct()
		return render(request, 'users/search.html', {'results':queryset_list, 'requested':query, 'len':len(queryset_list)})
	#end of search handler

	#if user is logged in and is a distributor
	if request.user.is_authenticated and request.user.groups.all()[0].name == 'distributors':
		args = {}
		#get request, 
		distr = Distributor.objects.filter(user=request.user).first()
		books = Book.objects.filter(dist=distr)
		print(distr)
		args['distr'] = distr
		args['books'] = books
		if request.method == 'GET':
			#find the books that the user distributes
			#create a form with this books and their availability
			form = GiveBook()
			form.fields['books'].queryset = books
			args['form'] = form
			return render(request, 'users/distribution.html', args)
		#post request
		else:
			#get form that was posted
			form = GiveBook(request.POST)
			if form.is_valid():
				#get books selected for distribution
				books_selected = form.cleaned_data['books']
				#for every book, update its availability
				for book in books_selected:
					b_sel = Book.objects.get(pk=book.id)
					new_avail = b_sel.avail - 1
					if new_avail >= 0:
						b = Book.objects.filter(pk=book.id).update(avail=new_avail)
						messages.success(request, f'Το σύγγραμμα με τίτλο "{b_sel}" παραδόθηκε επιτυχώς!')
			form = GiveBook()
			form.fields['books'].queryset = books
			args['form'] = form
			return render(request, 'users/distribution.html', args)
	else:
		return redirect('/login/?next=%s' % request.path)

def distributor(request):

	#search handler
	query = request.GET.get("q")
	if query:
		queryset_list = Book.objects.all()
		queryset_list = queryset_list.filter(Q(title__icontains=query)|Q(author__icontains=query)|Q(isbn__icontains=query)|Q(pub__title__icontains=query)).distinct()
		return render(request, 'users/search.html', {'results':queryset_list, 'requested':query, 'len':len(queryset_list)})
	#end of search handler
	return render(request, 'users/distributor.html', {'title': 'Οδηγός Διανομής'})


############### * PUBLISHER * ###############

def publisher(request):

	#search handler
	query = request.GET.get("q")
	if query:
		queryset_list = Book.objects.all()
		queryset_list = queryset_list.filter(Q(title__icontains=query)|Q(author__icontains=query)|Q(isbn__icontains=query)|Q(pub__title__icontains=query)).distinct()
		return render(request, 'users/search.html', {'results':queryset_list, 'requested':query, 'len':len(queryset_list)})
	#end of search handler

	#if user is logged in and is a publisher
	if request.user.is_authenticated and request.user.groups.all()[0].name == 'publishers':
		return render(request, 'users/publisher.html', {'title': 'Εκδότης'})
	else:
		return redirect('/login/?next=%s' % request.path)


############### * STUDENT * ###############

def student(request):

	#search handler
	query = request.GET.get("q")
	if query:
		queryset_list = Book.objects.all()
		queryset_list = queryset_list.filter(Q(title__icontains=query)|Q(author__icontains=query)|Q(isbn__icontains=query)|Q(pub__title__icontains=query)).distinct()
		return render(request, 'users/search.html', {'results':queryset_list, 'requested':query, 'len':len(queryset_list)})
	#end of search handler
	else:
		return render(request, 'users/student.html', {'title': 'Φοιτητής'})

def exchange(request):

	#search handler
	query = request.GET.get("q")
	if query:
		queryset_list = Book.objects.all()
		queryset_list = queryset_list.filter(Q(title__icontains=query)|Q(author__icontains=query)|Q(isbn__icontains=query)|Q(pub__title__icontains=query)).distinct()
		return render(request, 'users/search.html', {'results':queryset_list, 'requested':query, 'len':len(queryset_list)})
	#end of search handler

	#if user is logged in and is a student
	if request.user.is_authenticated and request.user.groups.all()[0].name == 'students':
		return render(request, 'users/exchange.html', {'title': 'Ανταλλαγή'})
	else:
		return redirect('/login/?next=%s' % request.path)


############### * DISPLAY ALL BOOKS * ###############

class DisplayWizard(AccessMixin, SessionWizardView):
	template_name = "users/display.html"

	def get_form(self, step=None, data=None, files=None):
		form = super(DisplayWizard, self).get_form(step, data, files)
		
		if step is None:
			step = self.steps.current

		if step == 'deptdata':
			prev_data = self.get_cleaned_data_for_step('unidata')['university'].id
			form.fields['department'].queryset = Department.objects.filter(uni=prev_data).order_by('title')
		elif step == 'classes':
			dept = self.get_cleaned_data_for_step('deptdata')['department'].id
			form.fields['lesson'].queryset = Class.objects.filter(dept=dept).order_by('title')
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


############### * ORDER BOOKS * ###############

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

		if self.request.user.is_authenticated and self.request.user.groups.all()[0].name == 'students':
			student = Student.objects.filter(user=self.request.user).first()
			if step == 'unidata':
				form.fields['university'].queryset = University.objects.filter(id=student.uni.id).order_by('title')
			elif step == 'deptdata':
				form.fields['department'].queryset = Department.objects.filter(id=student.dept.id).order_by('title')
		else:
			if step == 'deptdata':
				prev_data = self.get_cleaned_data_for_step('unidata')['university'].id
				form.fields['department'].queryset = Department.objects.filter(uni=prev_data).order_by('title')
		
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
				#form.forms[i].initial = {'book':1}
		elif step == 'final':
			books = self.get_cleaned_data_for_step('books')
			form.extra = len(books)
			for i in range(len(books)):
				form.forms[i].initial = {'way_of_receipt':1}
				form.forms[i].fields['way_of_receipt'].label = books[i]['book']
		return form
	
	def done(self, form_list, **kwargs):
		if self.request.user.is_authenticated and self.request.user.groups.all()[0].name == 'students':
			form_data = process_form_data(form_list)
			print(form_data)
			books = self.get_cleaned_data_for_step('books')
			order = Order()
			order.user = self.request.user
			order.save()
			print(books[0]['book'])
			for book in books:
				order.books.add(book['book'])
			messages.success(self.request, f'Η δήλωσή σας καταχωρήθηκε επιτυχώς!')
			return redirect('profile')
		else:
			return redirect('/login/?next=%s' % self.request.path)

def process_form_data(form_list):
	form_data = [form.cleaned_data for form in form_list]
	return form_data


############### * SEARCH * ###############

def search(request):

	#search handler
	query = request.GET.get("q")
	if query:
		queryset_list = Book.objects.all()
		queryset_list = queryset_list.filter(Q(title__icontains=query)|Q(author__icontains=query)|Q(isbn__icontains=query)|Q(pub__title__icontains=query)).distinct().order_by('title')
		return render(request, 'users/search.html', {'results':queryset_list, 'requested':query, 'len':len(queryset_list)})
	#end of search handler

	return render(request, 'users/search.html', {'title': 'Search'})


############### * PROFILE * ###############

@login_required
def profile(request):

	#search handler
	query = request.GET.get("q")
	if query:
		queryset_list = Book.objects.all()
		queryset_list = queryset_list.filter(Q(title__icontains=query)|Q(author__icontains=query)|Q(isbn__icontains=query)|Q(pub__title__icontains=query)).distinct()
		return render(request, 'users/search.html', {'results':queryset_list, 'requested':query, 'len':len(queryset_list)})
	#end of search handler

	args = {}

	#if user is a student
	if request.user.groups.all()[0].name == 'students':
		#get student info
		student = Student.objects.filter(user=request.user).first()
		args['student'] = student
		#get student's orders
		orders = Order.objects.filter(user=request.user)
		args['orders'] = orders
		for order in orders:
			for book in order.books.all():
				print(book.dist)
			print("----------")
	#else, for the other three categories we just have a title
	elif request.user.groups.all()[0].name == 'publishers':
		info = Publisher.objects.filter(user=request.user).first()
		args['info'] = info
	elif request.user.groups.all()[0].name == 'distributors':
		info = Distributor.objects.filter(user=request.user).first()
		args['info'] = info
	else:
		info = Secretary.objects.filter(user=request.user).first()
		args['info'] = info
	return render(request, 'users/profile.html', args)

@login_required
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

############### * REGISTRATION * ###############

def register(request):
	#if new user
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			#get user type
			group_selected = form.cleaned_data.get('user_type')
			#find group of that user type
			group = Group.objects.get(id=group_selected)
			#add user to that group
			user.groups.add(group)
			username = form.cleaned_data.get('username')
			messages.success(request, f'{username}, ο λογαριασμός σας δημιουργήθηκε με επιτυχία!')
			#log new user in so can procede to additional info, 'additional_register' requires login
			new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
			login(request, new_user)
			return redirect('additional')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form': form})

### under construction
def load_departments(request):
	uni = request.GET('uni')
	depts = Department.objects.filter(uni=uni).order_by('title')
	return render(request, )

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
