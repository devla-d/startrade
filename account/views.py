from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import  messages
from django.http import JsonResponse
from django.contrib.auth  import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone 
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_text
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .forms import LoginForm,RegistrationForm,UserCreationForm,UserUpdateForm,PasswordChangeForm
#from coin_exchange.utils  import *


from .models import Account



def register_view(request):
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            space_username = str(form.cleaned_data['username'])
            username = space_username.replace(" ","_")
            instance = form.save(commit=False)
            instance.username = username
            instance.is_active = False
            instance.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('auth/account_activation_email.html', {
                'user': instance,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
                'token': default_token_generator.make_token(instance),
            })
            instance.email_user(subject, message)
            
            #return JsonResponse({"success":'Account created','uri':instance.uri,'username':instance.username,'id':instance.id})
            return redirect(f"/verify-email/?uri={instance.uri}&&username={instance.username}")
        '''else:
            return JsonResponse(form.errors)'''

    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html',{"form":form})



def login_view(request):
    destination = get_redirect_if_exists(request)
    print("destination: " + str(destination))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            destination = request.POST['destination']
            user = authenticate(email=email, password=password)
            if user:
                login(request,user)
                if destination != 'None':
                    return redirect(destination)
                else:
                    return redirect("dashboard")
    else:
        form = LoginForm()
    return render(request, 'auth/login.html',{"form":form, "destination":destination})




def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect


def logout_view(request):
    logout(request)
    return redirect('login')




def activate_account_view(request, uidb64, token, *args, **kwargs):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_verified= True
        user.is_email_verifield = True
        user.save()
        login(request, user)
        messages.success(request, ('Your account have been confirmed.'))
        return redirect('dashboard')
    else:
        messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
        return redirect('login')





def verify_email_view(request):
    if request.GET.get('uri'):
        uri = request.GET.get('uri')
        user = Account.objects.get(uri=uri)
        if user:
            return render(request, 'auth/verify-email.html',{'email':user.email})
        else:
            return redirect('register')



@login_required
def account_view(request):
    return render(request, 'auth/account.html')         

@login_required
def settings_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST,instance=user)
        if form.is_valid():
            #print("yes form is valid ", form.save() )
            form.save()
            messages.info(request, ('Account Updated'))
            return redirect("account")
        '''else:
            return JsonResponse(form.errors)'''
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'settings.html',{"form":form})  








@login_required
def security_settings_view(request):
    user = request.user
    if request.POST:
        form = PasswordChangeForm(request.POST,instance=user)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            user.set_password(password1)
            user.save()
            messages.info(request, f'Password Change')
            return redirect('security-settings')
    else:
        form = PasswordChangeForm(initial={'user_id': user.id})
    return render(request,'auth/securty_settings.html',{"form":form})