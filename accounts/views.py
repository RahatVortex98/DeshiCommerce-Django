from django.http import HttpResponse
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

from django.contrib.auth.hashers import make_password

from django.contrib.auth.tokens import PasswordResetTokenGenerator

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
    # Clear previous messages
    storage = messages.get_messages(request)
    storage.used = True  

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')  # Redirect to home page after login
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



    

@login_required(login_url='login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')

# Use Django's built-in token generator for password reset
password_reset_token = PasswordResetTokenGenerator()

def forgotPassword(request):
    if request.method == "POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact =email)

            # Reset password email
            current_site = get_current_site(request) #This retrieves the domain name (e.g., yourwebsite.com) from the request.
            mail_subject = 'Please Reset Your Password'

            # Render the Activation Email Template

            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,  # Ensure '.domain' is used here
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': password_reset_token.make_token(user),  # Use password reset token
            })

            to_email = email # Recipient email address
            send_email = EmailMessage(mail_subject, message, to=[to_email]) # Create email object
            send_email.send()  # Send the email

            messages.success(request,'A mail has been send your gmail')
            return redirect('login')

        
        else:
            messages.error(request,'Account Not Exist')
            return redirect('forgotPassword')




    return render(request,'accounts/forgotPassword.html')


def resetpassword_validate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()  # Decode the user ID
        user = Account.objects.get(pk=uid)  # Get the user
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and password_reset_token.check_token(user, token):
        request.session['uid'] = uid  # Store uid in session for resetting password
        messages.success(request, "Please reset your password.")
        return redirect('resetPassword')
    else:
        messages.error(request, "This link has expired!")
        return redirect('forgotPassword')



def resetPassword(request):
    if request.method == "POST":
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        uid = request.session.get("uid")

        if not uid:
            messages.error(request, "Session expired. Try again.")
            return redirect("forgotPassword")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("resetPassword")

        try:
            user = Account.objects.get(pk=uid)
            user.set_password(password1)
            user.save()

            del request.session["uid"]

            # ✅ Clear messages before redirecting
            storage = messages.get_messages(request)
            storage.used = True

            messages.success(request, "Your password has been reset successfully. You can now log in.")
            return redirect("login")

        except Account.DoesNotExist:
            messages.error(request, "Something went wrong. Try again.")
            return redirect("forgotPassword")

    return render(request, "accounts/resetPassword.html")

    
    