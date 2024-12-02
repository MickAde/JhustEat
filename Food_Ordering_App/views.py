from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import (
    View, ListView, UpdateView, CreateView, DeleteView, DetailView
)
from django.contrib.auth.models import Group
from .forms import (
    RegisterForm, FormWithCaptcha, UserProfileForm, AddMenuForm, UserProfileUpdateForm, AddCategoryForm
)
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator



#----------- Check if the user belongs to the 'CUSTOMER' group
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

#----------- Check if the user belongs to the 'DRIVER' group
def is_driver(user):
    return user.groups.filter(name='DRIVER').exists()

#--------- Redirect users after login based on their group (Customer or Driver)
def afterlogin_view(request):
    user_groups = request.user.groups.values_list('name', flat=True)  # Cache user groups

    if 'CUSTOMER' in user_groups:
        return redirect('home')
    if 'DRIVER' in user_groups:
        return redirect('driver_home')
    else:
        return redirect('user_logout')




#####   Email Verification    #######
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.contrib.auth import get_user_model

# Function to activate user account using a token
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        # Decode the UID and get the user
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    
    # Activate user if found
    if user is not None:
        user.is_active = True
        user.save()
        messages.success(request, f'Thank You For Your Email Confirmation. You Can Proceed To Login Now')
        return redirect('user_login')
    else:
        messages.error(request, f'Email Confirmation Failed. You Can Proceed To Login Now')

    return redirect('home')

# Function to send activation email to the user
def activateEmail(request, user, to_email):
    mail_subject =  'Activate your JhustEat Account'
    message = render_to_string(
        'activate_account.html',
        {'user': user.username,
         'domain': get_current_site(request).domain,
         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
         'token': account_activation_token.make_token(user),
         'protocol': 'https' if request.is_secure else 'http',}
    )
    email = EmailMessage(mail_subject, message, to=[to_email,])
    
    # Send email and notify user
    if email.send():
        messages.success(request, f'Dear {user}, please go to your email {to_email} inbox and click on the received activation link to confirm and complete registration. Note: Check Spam Folder.')
    else:
        messages.success(request, f'Problem Sending Email To <b>{to_email}</b>')



################################################
###############   AUTHENTICATION    ############
###############        AND          ############
###############    AUTHORIZATION    ############
################################################    

# View for user registration
class RegisterView(View):
    def get(self, request, *args, **kwargs):
        user_form = RegisterForm()  # Initialize registration form
        user_profile = UserProfileForm()  # Initialize user profile form
        context = {'user_form': user_form, 'user_profile': user_profile}
        return render(request, 'page-register.html', context)

    def post(self, request, *args, **kwargs):
        user_form = RegisterForm(request.POST)  # Bind data to form
        user_profile = UserProfileForm(request.POST, request.FILES)  # Bind data to profile form

        # Validate both forms
        if user_form.is_valid() and user_profile.is_valid():
            user = user_form.save(commit=False)  # Create user instance but don't save yet
            user.is_active = False  # Deactivate user until email confirmation
            user.save()  # Save user

            # Assign user to appropriate group based on user type
            user_type = user_profile.cleaned_data.get('user_type')
            if user_type == 'Driver':
                user_group = Group.objects.get_or_create(name='DRIVER')
                user_group[0].user_set.add(user)
            else:
                user_group = Group.objects.get_or_create(name='CUSTOMER')
                user_group[0].user_set.add(user)
            
            # Create user profile
            profile = UserProfile.objects.create(
                profile_image=user_profile.cleaned_data.get('profile_image'),
                user=user,
                phone_number=user_profile.cleaned_data.get('phone_number'),
                user_type=user_profile.cleaned_data.get('user_type'),
            )
            profile.save()  # Save profile

            # Send activation email
            activateEmail(request, user, user_form.cleaned_data.get('email'))

            
            messages.success(request, "Your Account Has Been Successfully Created.")
            return redirect('home')  # Redirect to home after successful registration
            
        context = {'user_form': user_form, 'user_profile': user_profile}
        return render(request, 'page-register.html', context)  # Render registration page with errors if any

# View for user sign-in
class SignInView(View):
    def get(self, request, *args, **kwargs):
        captcha = FormWithCaptcha  # Initialize captcha form
        return render(request, 'page-login.html', context={'captcha': captcha})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            # Authenticate user
            user = authenticate(
                request,
                username=request.POST.get('username'),
                password=request.POST.get('password'),
            )
            if user:
                login(request, user)  # Log the user in
                messages.success(request, f"Hi {request.POST.get('username')}, Welcome To JhustEat.")
                return redirect('afterlogin_view')  # Redirect to after login view
            else:
                messages.error(request, f"Invalid Login Details.")
                return redirect('user_login')  # Redirect back to login on failure
        
        return render(request, 'page-login.html')  # Render login page

@login_required(login_url='user_login')
def SignOutView(request):
    logout(request)  # Log the user out
    messages.success(request, 'Bye, See ya next time.')
    return redirect('user_login')  # Redirect to login page





###########################################################
###############     CUSTOMER VIEW      ####################
###########################################################

@login_required(login_url='user_login')
@user_passes_test(is_customer, redirect_field_name="afterlogin_view")
def Home(request):
    return render(request, 'index.html')  # Render customer home page

@login_required(login_url='user_login')
@user_passes_test(is_customer, login_url='user_login')
def Home2(request):
    return render(request, 'index-2.html')  # Render alternative customer home page

@login_required(login_url='user_login')
@user_passes_test(is_customer, login_url='user_login')
def food_order(request):
    return render(request, 'food-order.html')  # Render food order page


@login_required(login_url='user_login')
@user_passes_test(is_customer, login_url='user_login')
def menu(request):
    form = AddCategoryForm()  # Initialize add category form
    addmenuform = AddMenuForm()  # Initialize add menu form
    if request.method == 'POST':
        addmenuform = AddMenuForm(request.POST, request.FILES)  # Bind data to add menu form
        if addmenuform.is_valid():
            addmenuform.save()  # Save new menu item
            messages.success(request, 'Menu Added Successfully.')
            return redirect('menu')  # Redirect to menu page
        else:
            messages.error(request, 'Menu Not Added.')
            return redirect('menu')  # Redirect back to menu page if there's an error
            
    # Pagination logic
    menu_list = Menu.objects.all()  # Fetch all menus
    paginator = Paginator(menu_list, 9)  # Show 9 menus per page
    page_number = request.GET.get('page')  # Get the page number from the URL
    page_obj = paginator.get_page(page_number)  # Get the items for the current page
    
    context = {
        'addmenuform': addmenuform,
        'form': form,
        'categories': Category.objects.all(),  # Get all categories
        'page_obj': page_obj,  # Pass the paginated menus
    }
    
    return render(request, 'menu.html', context)  # Render menu page with context

@login_required(login_url='user_login')
def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST, request.FILES)  # Bind data to add category form
        if form.is_valid():
            form.save()  # Save new category
            messages.success(request, "Menu Category Added Successfully.")
            return redirect('menu')  # Redirect to menu page
    
    return render(request, 'menu.html')  # Render menu page if not POST

@login_required(login_url='user_login')
def order_history(request):
    return render(request, 'order-history.html')  # Render order history page

@login_required(login_url='user_login')
def bill(request):
    return render(request, 'bill.html')  # Render bill page

###########################################################
##############     GENERAL VIEW           #################
###########################################################

@login_required(login_url='user_login')
def settings(request):
    user = request.user  # Get the current user
    profile = user.userprofile  # Get the user's profile
    u_profile = UserProfileUpdateForm(instance=profile, user=user)  # Initialize update form with existing profile data

    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, user=user)  # Bind data to update form
        if form.is_valid():
            # Update User model fields
            user.username = form.cleaned_data.get('username')
            user.email = form.cleaned_data.get('email')

            # Update password if provided
            password1 = form.cleaned_data.get('password1')
            if password1:
                user.set_password(password1)  # Set the new password

            user.save()  # Save user changes

            # Update UserProfile model fields
            profile.profile_image = form.cleaned_data.get('profile_image')
            profile.phone_number = form.cleaned_data.get('phone_number')  # Ensure this field exists in the form
            profile.address = form.cleaned_data.get('address')  # Ensure this field exists in the form
            profile.save()  # Save profile changes

            messages.success(request, 'Profile updated successfully!')
            return redirect('settings')  # Redirect to settings page after successful update
        else:
            return redirect('settings')  # Redirect back to settings if there's an error

    context = {
        'profileupdateform': u_profile,  # Pass the update form to the template
    }
    return render(request, 'setting.html', context)  # Render settings page

@login_required(login_url='user_login')
def page404(request):
    return render(request, 'page-error-404.html')  # Render 404 error page

# View to update user profile
def UserProfileUpdateView(request):
    user = request.user  # Get the current user
    profile = user.userprofile  # Get the user's profile

    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, user=user)  # Bind data to update form
        if form.is_valid():
            # Update User model fields
            user.username = form.cleaned_data.get('username')
            user.email = form.cleaned_data.get('email')

            # Update password if provided
            password1 = form.cleaned_data.get('password1')
            if password1:
                user.set_password(password1)  # Set the new password

            user.save()  # Save user changes

            # Update UserProfile model fields
            profile.profile_image = form.cleaned_data.get('profile_image')
            profile.phone_number = form.cleaned_data.get('phone_number')  # Ensure this field exists in the form
            profile.address = form.cleaned_data.get('address')  # Ensure this field exists in the form
            profile.save()  # Save profile changes

            messages.success(request, 'Profile updated successfully!')
            return redirect('settings')  # Redirect to settings page after successful update
        else:
            return redirect('settings')  # Redirect back to settings if there's an error

###########################################################
##############     DRIVER'S VIEW          #################
###########################################################

@login_required(login_url='user_login')
@user_passes_test(is_driver, login_url='user_login')
def driver_home(request):
    return render(request, 'deliver-main.html')  # Render driver's home page

@login_required(login_url='user_login')
@user_passes_test(is_driver, login_url='user_login')
def driver_order(request):
    return render(request, 'deliver-order.html')  # Render driver's order page

#############################################################
##############     ERROR_PAGE VIEW          #################
#############################################################

# Custom error views for handling different HTTP errors
def custom_400_view(request, exception):
    return render(request, 'page-error-400.html', status=400)

def custom_403_view(request, exception):
    return render(request, 'page-error-403.html', status=403)

def custom_404_view(request, exception):
    return render(request, 'page-error-404.html', status=404)

def custom_500_view(request):
    return render(request, 'page-error-500.html', status=500)

def custom_503_view(request):
    return render(request, 'page-error-503.html', status=503)
