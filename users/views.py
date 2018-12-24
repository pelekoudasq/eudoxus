from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from formtools.wizard.views import SessionWizardView
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserRegisterForm, ContactForm, UniversityForm
from users.models import University, Department, Class, Book
import logging
logr = logging.getLogger(__name__)
# Create your views here.

def home(request):
	context = {
		#'posts': Post.objects.all()
	}
	return render(request, 'users/home.html', context)


def about(request):
	return render(request, 'users/about.html', {'title': 'About'})

def announcements(request):
	return render(request, 'users/announcements.html', {'title': 'Announcements'})

def contact(request):
	return render(request, 'users/contact.html', {'title': 'Contact'})

def exchange(request):
	return render(request, 'users/exchange.html', {'title': 'Exchange'})

# def order(request):
# 	#universities = University.objects.all()
# 	form = UniversityForm()
# 	if request.method == 'POST':
# 		form = UniversityForm(request.POST)
# 		if form.is_valid():
# 			selected_uni = form.cleaned_data.get('university')
# 			messages.success(request, f'{selected_uni} επιλέχθηκε')
# 			return redirect('users-home')
# 	return render(request, 'users/order.html', {'form':form}, {'title': 'Order'})

class OrderWizard(SessionWizardView):
	template_name = "users/order.html"

	# def get_context_data(self, form, **kwargs):
	# 	context = super(OrderWizard, self).get_context_data(form=form, **kwargs)
	# 	if self.steps.current == '1':
	# 		prev_data = self.get_cleaned_data_for_step('0')
	# 		logr.debug(prev_data)
	# 		context.update({'department': Department.objects.filter(uni=prev_data.pk)})
	# 	return context

	def get_form(self, step=None, data=None, files=None):
		form = super(OrderWizard, self).get_form(step, data, files)
		if step is None:
			step = self.steps.current

		if step == 'deptdata':
			prev_data = self.get_cleaned_data_for_step('unidata')
			prev_data = prev_data['university']
			prev_data = prev_data.id
			print ("here", step, prev_data)
			form.fields['department'].queryset = Department.objects.filter(uni=prev_data)
		return form
	
	# def get_form_kwargs(self, step):
	# 	kwargs = super(OrderWizard, self).get_form_kwargs()
	# 	print("---> get_form_kwards", self.steps.current, self.get_cleaned_data_for_step('0'))
	# 	if self.steps.current == '1':
	# 		print("---> entered deptdata")
	# 		obj = self.get_cleaned_data_for_step('0')
	# 		kwargs['filter'] = obj.id
	# 	return kwargs
	def done(self, form_list, **kwargs):
		form_data = process_form_data(form_list)
		# messages.success(request, f'{form_data} επιλέχθηκαν')
		return redirect('profile')

def process_form_data(form_list):
	form_data = [form.cleaned_data for form in form_list]
	return form_data





@login_required
def profile(request):
	return render(request, 'users/profile.html')

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'{username}, ο λογαριασμός σας δημιουργήθηκε με επιτυχία! Συνδεθείτε για να συνεχίσετε')
			return redirect('login')
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