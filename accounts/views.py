from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser, OTP
from .forms import RegisterForm, LoginForm, OTPForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # inactive until OTP verified
            user.save()

            # Generate OTP
            code = OTP.generate_code()
            OTP.objects.create(user=user, code=code, purpose='register')

            send_mail(
                subject='Your FYP Portal Registration OTP',
                message=f'Your OTP is: {code}\nIt expires in 5 minutes.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

            # SESSION SAFE SET
            request.session['pending_user_id'] = user.id
            request.session['otp_purpose'] = 'register'

            messages.info(request, 'An OTP has been sent to your email.')
            return redirect('accounts:verify_otp')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)

            if user:
                # Generate OTP
                code = OTP.generate_code()
                OTP.objects.create(user=user, code=code, purpose='login')

                send_mail(
                    subject='Your FYP Portal Login OTP',
                    message=f'Your login OTP is: {code}\nIt expires in 5 minutes.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                )

                # SESSION SAFE SET
                request.session['pending_user_id'] = user.id
                request.session['otp_purpose'] = 'login'

                messages.info(request, 'An OTP has been sent to your email.')
                return redirect('accounts:verify_otp')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def verify_otp_view(request):
    user_id = request.session.get('pending_user_id')
    purpose = request.session.get('otp_purpose')

    # SAFE CHECK (prevents crash)
    if not user_id or not purpose:
        messages.error(request, "Session expired. Please login again.")
        return redirect('accounts:login')

    # SAFE USER FETCH
    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, "User not found. Please login again.")
        return redirect('accounts:login')

    if request.method == 'POST':
        form = OTPForm(request.POST)

        if form.is_valid():
            code = form.cleaned_data['code']

            otp = OTP.objects.filter(
                user=user,
                code=code,
                purpose=purpose,
                is_used=False
            ).last()

            if otp and otp.is_valid():
                otp.is_used = True
                otp.save()

                if purpose == 'register':
                    user.is_active = True
                    user.is_verified = True
                    user.save()

                login(request, user)

                # SAFE SESSION CLEANUP (no KeyError)
                request.session.pop('pending_user_id', None)
                request.session.pop('otp_purpose', None)

                messages.success(request, f'Welcome, {user.username}!')
                return redirect('dashboard:home')
            else:
                messages.error(request, 'Invalid or expired OTP.')
    else:
        form = OTPForm()

    return render(request, 'accounts/verify_otp.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:login')