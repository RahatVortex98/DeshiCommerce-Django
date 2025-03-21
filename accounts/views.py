from django.shortcuts import redirect, render

from .models import Account
from .forms import RegistrationForm
from django.contrib import messages,auth

from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages

#verfication Email 

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from .utils import account_activation_token  # Import custom token generator

def generate_unique_username(email):
    base_username = email.split('@')[0]  # Extract from email
    username = base_username
    counter = 1

    while Account.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"  # Append a number to make it unique
        counter += 1

    return username

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = generate_unique_username(email)  # Ensure uniqueness
            
            user = form.save(commit=False)  # Don't save yet
            user.username = username  # Assign unique username
            user.is_active = False
            user.save()  # Now save to DB


          
            # USER ACTIVATION
            current_site = get_current_site(request) #This retrieves the domain name (e.g., yourwebsite.com) from the request.
            mail_subject = 'Please Activate Your Account'

            # Render the Activation Email Template

            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site.domain,  # Ensure '.domain' is used here
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user), # Use custom token
            })

            to_email = email # Recipient email address
            send_email = EmailMessage(mail_subject, message, to=[to_email]) # Create email object
            send_email.send()  # Send the email

            
            messages.success(request, "Registration successful! You can now log in.Please Check Your email for varification")
            return redirect('login')  

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = RegistrationForm()
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)






def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid login credentials. Please try again.")
            return redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    storage = get_messages(request)
    for _ in storage:  # This clears existing messages before adding a new one
        pass  

    auth.logout(request)
    messages.success(request, 'Logged Out')
    return redirect('login')



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()  # Decode the UID
        user = Account._default_manager.get(pk=uid)  # Get user
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None  # Handle invalid cases

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account has been activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link or expired token.')
        return redirect('register')



    


def dashboard(request):
    return render(request,'accounts/dashboard.html')