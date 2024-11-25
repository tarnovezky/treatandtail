from django.contrib.auth.tokens import default_token_generator as generate_token
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect
from django.contrib import messages
from shop.services.email import send_email
from shop.services.token import generate_token
from django.contrib.auth import authenticate


""" 
Django Authentication Documentation
"""

class AuthController:
    """
    Handling all auth action
    """


    @staticmethod
    def signin(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('pass1')
            remember_me = request.POST.get('remember_me')  # Get the "Remember Me" checkbox value

            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)

                    if remember_me:
                        # Keep session active for 2 weeks (default Django session expiry)
                        request.session.set_expiry(1209600)  # 2 weeks in seconds
                    else:
                        # Set session to expire when the browser closes
                        request.session.set_expiry(0)

                    messages.success(request, 'Successfully logged in!')
                    return redirect('home')
                else:
                    messages.error(request, "Your account is not active. Please activate it first.")
                    print("NON ACTIVATED=================")
                    return redirect('auth')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('auth')

        return redirect('auth')







    @staticmethod
    def signup(request):
        if request.method == "POST":
            username = request.POST["username"]
            email = request.POST["email"]
            pass1 = request.POST["password1"]
            pass2 = request.POST["password2"]

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists! Try a different username.")
                return redirect('signup')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already in use. Try a different email.")
                return redirect('signup')

            if len(username) > 25:
                messages.error(request, "Username must be 25 characters or less.")
                return redirect('signup')

            if pass1 != pass2:
                messages.error(request, "Passwords do not match.")
                return redirect('signup')

            if not username.isalnum():
                messages.error(request, "Username should only contain letters and numbers.")
                return redirect('signup')

            try:
                # Create inactive user
                myuser = User.objects.create_user(username, email, pass1)
                myuser.is_active = False
                myuser.save()

                # Email confirmation
                current_site = get_current_site(request)
                email_subject = "Email Confirmation on ShopSite"
                message = render_to_string("shop/emails/email_confirmation.html", {
                    'name': myuser.username,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                    'token': generate_token.make_token(myuser),
                })
                send_email(email, 465, email_subject, message, html=True)

                messages.success(request,
                                 "Your account has been successfully created. Please check your email to activate your account.")
                return redirect('auth')

            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
                return redirect('signup')

        return render(request, "shop/pages/auth.html")



    @staticmethod
    def activate(request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            myuser = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            myuser = None

        if myuser is not None and generate_token.check_token(myuser, token):
            myuser.is_active = True
            myuser.save()
            login(request, myuser)
            messages.success(request, "Account activated successfully!")
            return redirect('home')
        else:
            messages.error(request, "Activation link is invalid or expired.")
            return render(request, 'shop/pages/activation_failed.html')