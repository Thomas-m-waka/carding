from django.shortcuts import render
import json
# Create your views here.
from django.http import JsonResponse
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm
from utils.sms_utils import send_sms

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})




def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                user = request.user
                messages.success(request, f'{user},Login successfull')
                return redirect('home')  # Redirect to home page after successful login
            else:
                messages.error(request,"Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')  


def home(request):
    return render(request,'index.html')


def admin_user_list(request):
    if request.user.is_superuser:  # Check if the user is an admin
        users = User.objects.all()
        return render(request, 'admin_list_users.html', {'users': users})
    else:
        # Redirect to some other page or display a message indicating that the user is not authorized
        return render(request, 'not_authorized.html')
    

def enter_username(request):

    return render(request, 'enter_username.html')


def enter_verification_code(request):
    if request.method == 'POST':
        entered_verification_code = request.POST.get('verification_code')
        
        generated_verification_code = request.session.get('verification_code')
        

        if generated_verification_code is not None and entered_verification_code == generated_verification_code:
            # if entered_verification_code == generated_verification_code:
            # Verification successful, redirect to password reset page
            return redirect('reset-password')
        else:
            # Verification failed, display error message
            messages.error(request, "Invalid verification code. Please try again.")
            return redirect('enter-code')  # Redirect back to verification code entry page
    else:
        # Handle GET request if needed
        return render(request, 'enter_verification.html')

from .models import Profile
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

def get_phone(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            # Get the user associated with the entered username
            user = User.objects.get(username=username)
            
            # Get the profile of the user
            profile = Profile.objects.get(user_id=user.pk)
            
            # Retrieve the phone number from the profile
            phone_number = str(profile.mobile)
            
            # Store the phone number and username in the session
            request.session['phone_number'] = phone_number
            request.session['username'] = username
            
            return render(request, 'get_phone.html', {'username': username, 'phone_number': phone_number})
        
        except ObjectDoesNotExist:
            # If the user does not exist, display an error message
            messages.error(request, "User not found.")
    
    return render(request, 'enter_username.html')

def send_verification_code(request):
    if request.method == 'POST':
        # Retrieve the username from the session
        phone_number = request.session['phone_number']
        print(phone_number)
        verification_code = generate_verification_code()
        phone = phone_number.lstrip('+254')
        print(phone)
        message = f"Your verification code is: {verification_code}"
        response = send_sms(phone, message)  # Pass both phone_number and message
        request.session['verification_code'] = verification_code
        # Process the response
        try:
            response_data = json.loads(response)
           
            response_code = response_data["responses"][0]["response-code"]
            # print(response_code)
            if response_code == 200:
                # If the response code indicates success
                # return JsonResponse({'status': 'success', 'message': 'Verification code sent successfully'})
                 # Redirect the user to the verification page with a success message
                return redirect('enter-code')
            else:
                # If the response code indicates an error
                return JsonResponse({'status': 'error', 'message': 'Failed to send verification code. Please try again later.'})
        except json.JSONDecodeError:
            # If there was an error decoding the JSON response
            return JsonResponse({'status': 'error', 'message': 'Failed to decode response. Please try again later.'})
        except KeyError:
            # If the response JSON structure is unexpected
            return JsonResponse({'status': 'error', 'message': 'Unexpected response structure. Please try again later.'})
    else:
        # Render the form to input phone number
        return render(request, 'generate_code.html')
    
from django.contrib.auth import update_session_auth_hash
import random 
from django.contrib.auth.forms import SetPasswordForm

def generate_verification_code():
    return str(random.randint(10000, 99999))


def reset_password(request):
    if request.method == 'POST':
        username = request.session.get('username')
        if not username:
            # If username is not in session, handle the error
            messages.error(request, "Username not found.")
            return redirect('login')  # Redirect to login page or any other appropriate page
            
        user = User.objects.get(username=username)
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(request, "Password reset successfully.")
            return redirect('home')
        else:
            # If the form is invalid, render the form again with appropriate error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
            return render(request, 'reset_password.html', {'form': form})
    else:
        form = SetPasswordForm(request.user)
    return render(request, 'reset_password.html', {'form': form})