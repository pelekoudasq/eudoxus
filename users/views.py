from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserRegisterForm, ContactForm
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