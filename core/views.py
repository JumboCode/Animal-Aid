from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


def home(request):
    return render(request, 'core/home.html')


def pass_reset(request):
    if request.method == 'POST':
	    pass_reset = PasswordResetForm(request.POST)
	    if pass_reset.is_valid():
	    	data = pass_reset.cleaned_data['email']
	    	associated_users = User.objects.filter(Q(email=data))
	    	if associated_users.exists():
	    		for user in associated_users:
	    			subject = 'Password Reset Requested'
	    			email_template_name = 'main/password/password_reset_email.txt'
					info = {
						'email': user.email,
						'domain': '127.0.0.1:8000',
						'site_name': 'Website',
						'uid': urlsafe_base64_encode(force_bytes(user.pk)),
						'user': user,
						'token': default_token_generator.make_token(user),
						'protocol': 'http',
					}
					email = render_to_string(email_template_name, info)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect('/password_reset/done/')
    pass_reset = PasswordResetForm()
    return render(request, 'password/passreset.html')
