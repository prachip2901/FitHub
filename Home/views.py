# views.py (cleaned & fixed)

from datetime import date, timedelta
from http import client
from Home.models import Earnings
import uuid
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from .models import Earning, TrainerBooking, Workout,DietPlan,Badge, Session
from requests import Session, request, session
from .models import YogaReminder, YogaStreak 
from django.conf import settings

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from .models import  CustomUser, Contact, UserProgress

from .models import (
    Contact, Earning, Exercise, MembershipPlan, UserSubscription,
    DemoTransaction, Post, Comment, MembershipTransaction,
    Trainer, TrainerAccount, TrainerReview, TrainerNotification,
    TrainerSession, SessionBooking, UserProgress, CustomUser, Client
)
from .forms import TrainerProfileForm, TrainerSessionForm, UserProgressForm
User = get_user_model()


# ------------------ Home & Static Pages ------------------
@login_required(login_url='login')
def index(request):
    context = {
        "prachi1": "Hi, my name is ...",
        "prachi2": "Hi, my age is ...",
    }
    return render(request, "index.html", context)





from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import  Progress, MoodHistory, YogaVideo

@login_required
def yoga(request):
    try:
        client = request.user.client
    except:
        client = None  # or redirect / create

    progress = None
    if client:
        progress, created = Progress.objects.get_or_create(client=client)

    videos = YogaVideo.objects.all()
    moods = MoodHistory.objects.filter(client=client) if client else []

    return render(request, 'yoga.html', {
        'progress': progress,
        'videos': videos,
        'moods': moods,
    })

def save_streak(request):
    streak,_=YogaStreak.objects.get_or_create(user=request.user)
    streak.streak+=1
    streak.save()
    return JsonResponse({"ok":True})

def save_email_reminder(request):
    YogaReminder.objects.update_or_create(
      user=request.user,
      defaults={"reminder_time":request.POST["time"]}
    )
    return JsonResponse({"saved":True})

@login_required
def save_mood(request):
    if request.method == 'POST':
        MoodHistory.objects.create(
            user=request.user,
            mood=request.POST['mood']
        )
        return JsonResponse({'status': 'saved'})

@login_required
def save_progress(request):
    if request.method == 'POST':
        progress, _ = Progress.objects.get_or_create(user=request.user)
        progress.percent = request.POST['value']
        progress.save()
        return JsonResponse({'saved': True})


from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import timedelta



# -------------------------------
# AI-LIKE PREDICTION FUNCTION
# -------------------------------

def predict_goal(weights, target_weight):
    """
    Predicts how many weeks are needed to reach target weight
    using average weekly weight loss.
    """
    if len(weights) < 2:
        return "Not enough data to predict progress."

    start_weight = weights[0]
    current_weight = weights[-1]

    total_loss = start_weight - current_weight
    weeks_passed = len(weights) - 1

    if total_loss <= 0:
        return "No weight loss trend detected. Improve consistency."

    avg_weekly_loss = total_loss / weeks_passed

    remaining = current_weight - target_weight
    if remaining <= 0:
        return "🎉 Target already achieved!"

    weeks_needed = remaining / avg_weekly_loss
    return f"Target achievable in approximately {int(abs(weeks_needed))} weeks."


# -------------------------------
# STREAK CALCULATION
# -------------------------------
def calculate_streak(records):
    """
    Calculates weekly streak based on 7-day gap rule.
    """
    if len(records) < 2:
        return 1

    streak = 1
    for i in range(len(records) - 1, 0, -1):
        gap = records[i].date - records[i - 1].date
        if gap <= timedelta(days=7):
            streak += 1
        else:
            break
    return streak


# -------------------------------
# MAIN DASHBOARD VIEW
# -------------------------------
from django.shortcuts import render, redirect


from django.shortcuts import render, redirect
from .models import WeightProgress
from .forms import CalculatorForm
from django.contrib.auth.decorators import login_required

@login_required
def weightloss(request):
    user = request.user
    form = CalculatorForm()
    weight_data = WeightProgress.objects.filter(user=user).order_by('week')
    chart_labels = [f"Week {w.week}" for w in weight_data]
    chart_data = [w.weight for w in weight_data]

    return render(request, 'weightloss.html', {
        'form': form,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    })

@login_required
def add_weight(request):
    if request.method == "POST":
        weight = float(request.POST.get('weight'))
        last_week = WeightProgress.objects.filter(user=request.user).count()
        week = last_week + 1
        WeightProgress.objects.create(user=request.user, week=week, weight=weight)
    return redirect('weightloss')


@login_required(login_url='login')
def dietplans(request):
    return render(request, 'dietplans.html')

import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def strenghtraining(request):

    exercises = [
        {
            'title': 'Push-Ups',
            'desc': 'Strengthen your upper body and core.',
            'img': 'https://plus.unsplash.com/premium_photo-1667511317035-b25f767c4f37',
            'video': 'https://www.youtube.com/embed/_l3ySVKYVJ8'
        },
        {
            'title': 'Squats',
            'desc': 'Train your legs and improve balance.',
            'img': 'https://images.unsplash.com/photo-1536922246289-88c42f957773',
            'video': 'https://www.youtube.com/embed/aclHkVaku9U'
        },
        {
            'title': 'Deadlifts',
            'desc': 'Improve posture and overall strength.',
            'img': 'https://images.unsplash.com/photo-1706029831405-619b27e3260c',
            'video': 'https://www.youtube.com/embed/ytGaGIn3SjE'
        }
    ]

    ai_plans = {
        "Full Body": [
            {"name": "Push-Ups", "duration": 30, "tip": "Keep core tight"},
            {"name": "Squats", "duration": 40, "tip": "Knees aligned"},
            {"name": "Deadlifts", "duration": 35, "tip": "Back straight"}
        ],
        "Chest": [
            {"name": "Push-Ups", "duration": 40, "tip": "Slow reps"},
            {"name": "Push-Ups", "duration": 30, "tip": "Squeeze chest"}
        ],
        "Legs": [
            {"name": "Squats", "duration": 45, "tip": "Push through heels"},
            {"name": "Squats", "duration": 35, "tip": "Maintain posture"}
        ],
        "Core": [
            {"name": "Plank", "duration": 30, "tip": "Engage abs"},
            {"name": "Mountain Climbers", "duration": 40, "tip": "Keep rhythm"}
        ],
        "Arms": [
            {"name": "Diamond Push-Ups", "duration": 25, "tip": "Triceps focus"}
        ]
    }

    return render(request, 'strenghtraining.html', {
        'exercises': exercises,
        'aiPlans': json.dumps(ai_plans)
    })


@login_required(login_url='login')
def cardio(request):
    return render(request, 'cardio.html')


@login_required(login_url='login')
def hiit(request):
    return render(request, 'hiit.html')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Home.models import Session, TrainerProfile, Workout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Home.models import TrainerProfile, Session, Workout
from django.contrib import messages

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Session, TrainerProfile, ClientProfile, Workout

@login_required
def trainers_hub(request):
    # 1️⃣ Make sure only clients can access this page
    if request.user.role != 'user':
        messages.error(request, "🚫 Access Denied. You are not registered as a client. Only clients can access this page.")
        return redirect('home')  # change 'home' to wherever non-clients should go

    # 2️⃣ Get the ClientProfile for the logged-in user
    try:
        client_profile = request.user.clientprofile
    except ClientProfile.DoesNotExist:
        messages.error(request, "🚫 You do not have a client profile. Please contact admin.")
        return redirect('home')

    # 3️⃣ Get all sessions for this client
    client_sessions = Session.objects.filter(client=client_profile)

    # 4️⃣ Get all unique trainers who have sessions with this client
    trainer_ids = client_sessions.values_list('trainer', flat=True).distinct()
    trainers = TrainerProfile.objects.filter(id__in=trainer_ids)

    # 5️⃣ Get all workouts assigned via sessions
    workouts = Workout.objects.filter(session__client=client_profile).distinct()

    # 6️⃣ Efficiently select related fields for template
    sessions = client_sessions.select_related('trainer', 'workout')

    context = {
        'trainers': trainers,
        'workouts': workouts,
        'sessions': sessions,
        'total_trainers': trainers.count(),
        'total_workouts': workouts.count(),
        'total_sessions': client_sessions.count(),
    }

    return render(request, 'trainers.html', context)


from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Session, TrainerProfile, Workout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def client_dashboard(request):
    # Make sure the user is a client
    if request.user.role != 'user':
        messages.error(request, "🚫 Access Denied. Only clients can view this page.")
        return redirect('home')

    # Get ClientProfile instance for the logged-in user
    client_profile = getattr(request.user, 'clientprofile', None)

    # Fetch only future sessions (today or later)
    upcoming_sessions = Session.objects.filter(
        client=client_profile,
        date__gte=timezone.now().date()
    ).order_by('date', 'time')

    # Get workouts via upcoming sessions
    upcoming_workouts = Workout.objects.filter(
        session__in=upcoming_sessions
    ).distinct()

    # Get all unique trainers assigned via these sessions
    trainer_ids = upcoming_sessions.values_list('trainer', flat=True).distinct()
    trainers = TrainerProfile.objects.filter(id__in=trainer_ids)

    context = {
        'sessions': upcoming_sessions.select_related('trainer', 'workout'),
        'trainers': trainers,
        'workouts': upcoming_workouts,
        'total_sessions': upcoming_sessions.count(),
        'total_trainers': trainers.count(),
        'total_workouts': upcoming_workouts.count(),
    }

    return render(request, 'client_dashboard.html', context)

@login_required
def book_session(request):
    """
    Book a trainer (TrainerBooking). Notify trainer and optionally send email.
    """
    if request.method == 'POST':
        trainer_id = request.POST.get('trainer_id')
        session_date = request.POST.get('session_date')
        session_time = request.POST.get('session_time')
        trainer = get_object_or_404(Trainer, id=trainer_id)

        booking = TrainerBooking.objects.create(
            trainer=trainer,
            user=request.user,
            session_date=session_date,
            session_time=session_time
        )

        TrainerNotification.objects.create(
            trainer=trainer,
            title="New Session Booking",
            message=f"{request.user.username} booked a session on {session_date} at {session_time}."
        )

        # Use trainer.user.email (Trainer model stores user relationship)
        trainer_email = getattr(trainer.user, "email", None)
        if trainer_email:
            try:
                send_mail(
                    subject=f"New Booking from {request.user.username}",
                    message=f"{request.user.username} booked a session with you on {session_date} at {session_time}.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[trainer_email],
                    fail_silently=True,
                )
            except Exception as e:
                print("Email sending failed:", e)

        return JsonResponse({'status': 'success', 'message': 'Session booked!'})
    return JsonResponse({'status': 'error'}, status=400)


from django.shortcuts import render, redirect
from .forms import TrainerReviewForm
from django.contrib.auth.decorators import login_required

@login_required
def add_review(request):
    if request.method == 'POST':
        form = TrainerReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # make sure the logged-in user is saved
            review.save()
            return redirect('reviews_list')  # or wherever you want
    else:
        form = TrainerReviewForm()
    return render(request, 'add_review.html', {'form': form})


# ------------------ Membership ------------------
@login_required(login_url='login')
def membership_page(request):
    plans = MembershipPlan.objects.all()
    return render(request, "membership.html", {"plans": plans})


@login_required
def create_transaction(request, plan_id):
    plan = get_object_or_404(MembershipPlan, id=plan_id)
    order_id = f"ORD-{uuid.uuid4().hex[:8]}"
    transaction = MembershipTransaction.objects.create(
        user=request.user,
        plan=plan,
        order_id=order_id,
        amount=plan.price,
        status='pending'
    )
    callback_url = request.build_absolute_uri(reverse('payment_callback'))

    context = {
        "plan": plan,
        "transaction": transaction,
        "callback_url": callback_url,
        "phonepe_qr": static('img/phonepe_qr.jpeg'),
        "paytm_qr": static('img/paytm_qr.jpeg'),
        "gpay_qr": static('img/gpay_qr.jpeg'),
        'phonepe_url': 'https://phonepe.com/pay-link',
        'paytm_url': 'https://paytm.com/pay-link',
        'gpay_url': 'https://gpay.com/pay-link',
    }
    return render(request, "phonepe_demo.html", context)


@login_required
def payment_callback(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        status = request.POST.get("status")
        transaction = get_object_or_404(MembershipTransaction, order_id=order_id)
        transaction.status = status
        transaction.save()
        message = (
            f"✅ Payment successful! You have subscribed to the {transaction.plan.name} plan."
            if status == "success"
            else "❌ Payment failed or cancelled. Please try again."
        )
        return render(request, "payment_result.html", {"message": message})
    return redirect("membership_page")


# ------------------ Progress / Exercise API ------------------
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from .models import Exercise

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import date, timedelta
from .models import Exercise

@login_required
def progress_page(request):
    return render(request, 'progress.html')

@login_required
def exercise_api(request):
    period = request.GET.get('period', 'today')
    today = date.today()

    if period == 'today':
        start_date = today
    elif period == 'weekly':
        start_date = today - timedelta(days=today.weekday())  # Monday
    elif period == 'monthly':
        start_date = today.replace(day=1)  # first day of month
    else:
        start_date = today

    # Filter only the logged-in user's exercises in this period
    exercises = Exercise.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lte=today
    ).order_by('date')

    # Prepare JSON data
    data = [
        {
            'date': e.date.strftime('%Y-%m-%d'),
            'name': e.name,
            'duration': e.duration,
            'calories': e.calories,
        } for e in exercises
    ]

    return JsonResponse(data, safe=False)



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Post, Comment
from .forms import CommentForm
from .forms import CommentForm, PostForm

@login_required(login_url='login')
def community(request):
    # Get all posts, latest first
    posts = Post.objects.all().order_by('-created_at')

    # Handle comment submission
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            Comment.objects.create(
                post=post,
                user=request.user,
                text=comment_form.cleaned_data['text']
            )
            return redirect('community')  # reload the page
    else:
        comment_form = CommentForm()

    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'community.html', context)


# ------------------ Dashboard ------------------
@login_required(login_url='login')
def dashboard_view(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST.get("username", user.username)
        user.email = request.POST.get("email", user.email)
        user.save()
        messages.success(request, "Profile updated successfully!")
    return render(request, "dashboard.html")


# ------------------ Contact ------------------
@login_required(login_url='login')
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Contact.objects.create(name=name, email=email, message=message)

        try:
            send_mail(
                f"New Contact Message from {name}",
                f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                settings.EMAIL_HOST_USER,
                ['prachipatel4706@gmail.com'],
                fail_silently=False
            )
            messages.success(request, "✅ Your message has been sent successfully and saved!")
        except Exception as e:
            messages.error(request, f"❌ Failed to send message. Error: {str(e)}")

        return redirect('contact')
    return render(request, "contact.html")

# ------------------ Authentication (signup, login, logout) ------------------
# views.py
import json, time
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib import messages

User = get_user_model()

# ---------------- SIGNUP + VERIFY OTP ----------------
def signup_view(request):
    # Handle AJAX POST (JSON)
    
    if request.method == "POST" and request.content_type.startswith('application/json'):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password1 = data.get('password1')
            password2 = data.get('password2')
            otp_entered = data.get('otp')
            role = data.get('role', 'user')

            # Password match
            if password1 != password2:
                return JsonResponse({'status':'error','error':'Passwords do not match'})

            # OTP session check
            otp_session = request.session.get('signup_otp')
            email_session = request.session.get('signup_email')
            otp_time = request.session.get('signup_otp_time')

            if not otp_session or not email_session or not otp_time:
                return JsonResponse({'status':'error','error':'Please request OTP first'})

            # OTP expiry (2 min)
            if time.time() - otp_time > 120:
                request.session.pop('signup_otp', None)
                request.session.pop('signup_email', None)
                request.session.pop('signup_otp_time', None)
                return JsonResponse({'status':'error','error':'OTP expired. Please request again'})

            # OTP & email check
            if otp_entered != otp_session or email != email_session:
                return JsonResponse({'status':'error','error':'Invalid OTP'})

            # Check if user exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({'status':'error','error':'Username already exists'})
            if User.objects.filter(email=email).exists():
                return JsonResponse({'status':'error','error':'Email already registered'})

            # Create user
            is_trainer = True if role=='trainer' else False
            is_client = not is_trainer
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
            )
            user.role = role
            user.is_trainer = is_trainer
            user.is_client = is_client
            user.save()

            # Clear session
            request.session.pop('signup_otp', None)
            request.session.pop('signup_email', None)
            request.session.pop('signup_otp_time', None)

            return JsonResponse({'status':'ok'})
        except Exception as e:
            return JsonResponse({'status':'error','error':str(e)})
    else:
        # Normal GET request
        return render(request,'signup.html')

# ---------------- SEND OTP ----------------
def send_otp_view(request):
    if request.method == "POST" and request.content_type.startswith('application/json'):
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                return JsonResponse({'status':'error','error':'Email required'})

            # Generate 6-digit OTP
            import random
            otp = str(random.randint(100000, 999999))

            # Store OTP in session
            request.session['signup_otp'] = otp
            request.session['signup_email'] = email
            request.session['signup_otp_time'] = time.time()

            # TODO: send OTP via email (use EmailMessage or SMTP)
            print(f"DEBUG: OTP for {email} is {otp}")

            return JsonResponse({'status':'ok'})
        except Exception as e:
            return JsonResponse({'status':'error','error':str(e)})
    return JsonResponse({'status':'error','error':'Invalid request'})

# ---------------- LOGIN ----------------
def login_view(request):
    if request.method == "POST" and request.content_type.startswith('application/json'):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            role = data.get('role', 'user')

            if not email or not password:
                return JsonResponse({'status':'error','error':'Fill all fields'})

            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({'status':'error','error':'Invalid email or password'})

            # Check role matches
            if user_obj.role != role:
                return JsonResponse({'status':'error','error':f'No {role} account found with this email'})

            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'status':'ok','role':role})
            else:
                return JsonResponse({'status':'error','error':'Invalid email or password'})
        except Exception as e:
            return JsonResponse({'status':'error','error':str(e)})

    return render(request, 'login.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import random, json

User = get_user_model()

# ============================
# SEND OTP (AJAX)
# ============================
# -----------------------------
# AJAX: Send OTP (NO password check here)
# -----------------------------
def send_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                return JsonResponse({'status': 'error', 'error': 'Email is required'})

            # Generate OTP
            otp = str(random.randint(100000, 999999))

            # Save in session
            request.session['signup_otp'] = otp
            request.session['signup_email'] = email
            request.session.modified = True

            # Send email
            send_mail(
                subject='FitLife OTP Verification',
                message=f'Your OTP is {otp}. Valid for 5 minutes.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False
            )

            return JsonResponse({'status': 'ok'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)})

    return JsonResponse({'status': 'error', 'error': 'Invalid request'})

# ============================
# SIGNUP + OTP VERIFY
# ============================
import random, json, time
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

# --------------------------
# SEND OTP
# --------------------------
@csrf_exempt
def send_otp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get('email')

        if not email:
            return JsonResponse({'status': 'error', 'error': 'Email required'})

        otp = str(random.randint(100000, 999999))

        # Save OTP + email + timestamp in session
        request.session['signup_otp'] = otp
        request.session['signup_email'] = email
        request.session['signup_otp_time'] = time.time()  # store as UNIX timestamp

        try:
            send_mail(
                'FitLife OTP Verification',
                f'Your OTP is {otp}. It will expire in 2 minutes.',
                'your_email@gmail.com',  # replace with your sender email
                [email],
                fail_silently=False,
            )
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)})
    return JsonResponse({'status': 'error', 'error': 'Invalid request method'})

# --------------------------
# SIGNUP + OTP VERIFY
# --------------------------


import json, random, time
from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

# ---------------- SEND OTP ----------------
def send_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get('email')
            if not email:
                return JsonResponse({'status':'error','error':'Email required'})
            
            otp = str(random.randint(100000,999999))

            # Save OTP in session with timestamp
            request.session['signup_otp'] = otp
            request.session['signup_email'] = email
            request.session['signup_otp_time'] = time.time()

            # Send email
            send_mail(
                'FitLife OTP Verification',
                f'Your OTP is {otp}',
                'your_email@gmail.com',  # change to your sender email
                [email],
                fail_silently=False,
            )
            return JsonResponse({'status':'ok'})
        except Exception as e:
            return JsonResponse({'status':'error','error': str(e)})
    return JsonResponse({'status':'error','error':'Invalid request'})


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Email verified successfully. You can now login.")
    else:
        messages.error(request, "Invalid or expired verification link")

    return redirect("login")


# Home/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string

User = get_user_model()  # this will automatically use your CustomUser

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if not email:
            messages.error(request, "Please enter your email.")
            return redirect("forgot-password")

        try:
            user = User.objects.get(email=email)

            # Generate a temporary random password or token
            temp_password = get_random_string(length=8)
            user.set_password(temp_password)
            user.save()

            # Send email with temporary password
            send_mail(
                subject="Password Reset Request",
                message=f"Hello {user.username},\n\nYour temporary password is: {temp_password}\nPlease log in and change your password immediately.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, "A temporary password has been sent to your email.")
            return redirect("login")

        except User.DoesNotExist:
            messages.error(request, "No user found with this email.")
            return redirect("forgot-password")

    return render(request, "forgot_password.html")

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if not user or not default_token_generator.check_token(user, token):
        messages.error(request, "Invalid or expired reset link")
        return redirect("login")

    if request.method == "POST":
        p1 = request.POST["password1"]
        p2 = request.POST["password2"]

        if p1 == p2:
            user.set_password(p1)
            user.save()
            messages.success(request, "Password reset successful")
            return redirect("login")

        messages.error(request, "Passwords do not match")

    return render(request, "reset_password.html")


# -------------------- TRAINER DASHBOARD --------------------

# -------------------- LOGOUT --------------------
def logout_view(request):
    logout(request)
    messages.success(request, "You've been logged out successfully! 👋")
    return redirect('login')

# ------------------ Trainer Dashboard (fixed) ------------------



# ------------------ Manage TrainerSession (classes) ------------------
@login_required(login_url='login')
def manage_session(request, session_id=None):
    trainer = get_object_or_404(Trainer, user=request.user)
    sessions = Session.objects.filter(trainer=trainer).order_by('-date')  # ✅ FIX

    if request.method == 'POST':
        form = TrainerSessionForm(request.POST, instance=session)
        if form.is_valid():
            new_session = form.save(commit=False)
            new_session.trainer = trainer
            new_session.save()
            messages.success(request, "Session saved successfully.")
            return redirect('trainer_dashboard')
    else:
        form = TrainerSessionForm(instance=session)

    return render(request, 'trainer/manage_session.html', {'form': form, 'session': session})


# ------------------ Session Users (for TrainerSession) ------------------
@login_required(login_url='login')
def session_users(request, session_id):
    trainer = get_object_or_404(Trainer, user=request.user)
    session = get_object_or_404(TrainerSession, id=session_id, trainer=trainer)
    bookings = SessionBooking.objects.filter(session=session).select_related('user').order_by('-booked_on')
    return render(request, 'trainer/session_users.html', {'session': session, 'bookings': bookings})



# ------------------ Add user progress (trainer action) ------------------
@login_required(login_url='login')
def add_user_progress(request, user_id):
    trainer = get_object_or_404(Trainer, user=request.user)
    user_obj = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = UserProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            # UserProgress model has user ForeignKey — set it
            progress.user = user_obj
            # if your UserProgress model has a trainer FK, uncomment the next line:
            # progress.trainer = trainer
            progress.save()
            messages.success(request, "User progress saved.")
            return redirect('trainer_dashboard')
    else:
        form = UserProgressForm()

    return render(request, 'trainer/add_user_progress.html', {'form': form, 'user': user_obj})


# ------------------ User Dashboard ------------------
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def user_dashboard(request):
    return render(request, 'user_dashboard.html')

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Trainer, Workout, Session
import json
from django.shortcuts import render
from Home.models import TrainerProfile, Workout, Session
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from Home.models import Session, Workout, TrainerProfile, ClientProfile
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json


@login_required
def trainers_list(request):
    trainers = TrainerProfile.objects.all()
    return render(request, "trainers.html", {"trainers": trainers})

@login_required
def trainer_detail(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)
    workouts = Workout.objects.filter(trainer=trainer)
    context = {
        'trainer': trainer,
        'workouts': workouts
    }
    return render(request, 'trainer_detail.html', context)



# ------------------ Simple trainer client list (demo) ------------------
# Home/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Home.models import Trainer

@login_required
def trainer_clients(request):
    try:
        trainer = Trainer.objects.get(user=request.user)
        print("Trainer found:", trainer)
    except Trainer.DoesNotExist:
        print("Trainer not found for user:", request.user)
        messages.error(request, "You are not registered as a trainer yet.")
        return redirect('trainer_dashboard')

    clients = trainer.clients.all() if hasattr(trainer, 'clients') else []
    print("Clients found:", clients)

    return render(request, 'trainer_clients.html', {'clients': clients})



@login_required
def trainer_earnings(request):
    trainer = get_object_or_404(Trainer, user=request.user)
    earnings = Earnings.objects.filter(trainer=trainer).order_by('-date')
    total_earnings = earnings.aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'trainer_earnings.html', {'earnings': earnings, 'total_earnings': total_earnings})

@login_required
def trainer_reviews(request):
    trainer = get_object_or_404(Trainer, user=request.user)
    reviews = TrainerReview.objects.filter(trainer=trainer).order_by('-created_at')
    return render(request, 'trainer_reviews.html', {'reviews': reviews, 'trainer': trainer})


@login_required
def trainer_notifications(request):
    trainer = get_object_or_404(Trainer, user=request.user)
    notifications = TrainerNotification.objects.filter(trainer=trainer).order_by('-created_at')
    return render(request, 'trainer_notifications.html', {'notifications': notifications})


@login_required
def trainer_sessions(request):
    # Get the Trainer instance for the logged-in user
    trainer = get_object_or_404(Trainer, user=request.user)
    # Now filter sessions by the Trainer instance (group/class sessions)
    sessions = TrainerSession.objects.filter(trainer=trainer)
    return render(request, 'trainer_sessions.html', {'sessions': sessions})


@login_required
def trainer_view_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, 'trainer_view_client.html', {'client': client})


# ================= DASHBOARDS =================

def user_dashboard(request): return render(request,'user_dashboard.html')

# ================= FORGOT PASSWORD =================
def forgot_password_view(request): return render(request,'forgot_password.html')

# ---------------- Analytics ----------------
@login_required
def trainer_analytics(request):
    trainer = request.user.trainer

    data = (
        Booking.objects
        .filter(trainer=trainer, status="completed")
        .extra(select={'month': "strftime('%%m', date)"})
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )

    return render(request, "trainer/analytics.html", {"data": data})




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Client
from django.template.defaultfilters import default

@csrf_exempt
def add_client(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        plan = request.POST.get('plan')
        progress = request.POST.get('progress')
        ai_insight = request.POST.get('ai_insight', '')  # optional

        if not name or not email or not plan or progress is None:
            return JsonResponse({'success': False, 'error': 'Missing fields'})

        try:
            progress = int(progress)
            if progress < 0 or progress > 100:
                return JsonResponse({'success': False, 'error': 'Progress out of range'})
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid progress'})

        # Save new client
        client = Client.objects.create(
            name=name,
            email=email,
            plan=plan,
            progress=progress,
            ai_insight=ai_insight
        )

        # Calculate new total and average progress
        all_clients = Client.objects.all()
        total_clients = all_clients.count()
        avg_progress = int(sum(c.progress for c in all_clients) / total_clients) if total_clients else 0

        # Prepare JSON response
        response_data = {
            'success': True,
            'client': {
                'id': client.id,
                'name': client.name,
                'email': client.email,
                'plan': client.plan,
                'progress': client.progress,
                'ai_insight': client.ai_insight,
                'photo_url': client.photo.url if client.photo else '/static/images/default_client.png',
                'view_url': f"/trainer/client/{client.id}/",  # replace with your URL or use reverse()
            },
            'total_clients': total_clients,
            'avg_progress': avg_progress
        }

        return JsonResponse(response_data)
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def get_ai_insight(progress):
    """Generate AI insight badge text based on progress"""
    if progress < 50:
        return "Needs Attention"
    elif progress < 80:
        return "On Track"
    return "Excellent"

# Home/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Comment
import json

@login_required
def community_page(request):
    return render(request, 'community.html')  # community.html, progress.html nathi

@login_required
def get_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    data = [
        {
            'id': post.id,
            'user': post.user.username,
            'text': post.text,
            'image': post.image.url if post.image else '',
            'likes': post.likes,
            'created_at': post.created_at.strftime("%Y-%m-%d %H:%M"),
            'comments': [{'user': c.user.username, 'text': c.text} for c in post.comments.all()]
        }
        for post in posts
    ]
    return JsonResponse({'posts': data})

@csrf_exempt
@login_required
def create_post(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        image = request.FILES.get('image')
        post = Post.objects.create(user=request.user, text=text, image=image)
        return JsonResponse({'status': 'success', 'post_id': post.id})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes += 1
    post.save()
    return JsonResponse({'status': 'success', 'likes': post.likes})

@csrf_exempt
@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text')
        if text:
            post = get_object_or_404(Post, id=post_id)
            Comment.objects.create(post=post, user=request.user, text=text)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

from django.views.decorators.http import require_http_methods

# Delete post
@csrf_exempt
@login_required
def delete_post(request, post_id):
    if request.method == 'DELETE':
        post = get_object_or_404(Post, id=post_id)
        if post.user != request.user:
            return JsonResponse({'status': 'error', 'message': 'Not allowed'}, status=403)
        post.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

# API endpoint to fetch trainers dynamically
def get_trainers(request):
    # Get filters from GET parameters
    goal = request.GET.get('goal', 'all')
    spec_filter = request.GET.get('spec', 'all')

    # Fetch all trainers
    trainers = Trainer.objects.all()

    # Apply filters if provided
    if goal != 'all':
        trainers = trainers.filter(spec=goal)
    if spec_filter != 'all':
        trainers = trainers.filter(spec=spec_filter)

    # Convert queryset to list of dictionaries
    trainers_data = list(trainers.values('id', 'name', 'spec', 'exp', 'rating', 'photo', 'lat', 'lng'))

    # Return JSON response
    return JsonResponse({'trainers': trainers_data})

@login_required
def submit_review(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)
    if request.method == "POST":
        rating = int(request.POST.get('rating', 0))
        comment = request.POST.get('comment', '')
        if rating > 0 and comment:
            TrainerReview.objects.create(
                trainer=trainer,
                user=request.user,
                rating=rating,
                comment=comment
            )
    return redirect('trainer_review', trainer_id=trainer.id)


from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Booking

def approve_session(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, trainer=request.user.trainer)
    booking.status = "approved"
    booking.save()
    messages.success(request, "Session approved successfully")
    return redirect("trainer_dashboard")

def reject_session(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, trainer=request.user.trainer)
    booking.status = "rejected"
    booking.save()
    messages.warning(request, "Session rejected")
    return redirect("trainer_dashboard")

def complete_session(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, trainer=request.user.trainer)
    booking.status = "completed"
    booking.save()
    messages.success(request, "Session marked as completed. Earnings added!")
    return redirect("trainer_dashboard")

from django.shortcuts import render
from .models import Category

def yoga_classes(request):
    categories = Category.objects.prefetch_related('classes').all()
    return render(request, 'yoga.html', {'categories': categories})

from django.templatetags.static import static


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Booking

# ---------------- Approve / Reject Booking ----------------
@login_required
def booking_action(request, id, action):
    booking = get_object_or_404(Booking, id=id, trainer=request.user.trainer)

    if action == "approve":
        booking.status = "approved"
    elif action == "reject":
        booking.status = "rejected"

    booking.save()
    return redirect("trainer_dashboard")
# Tamara view ma


from django.shortcuts import render, redirect
from .models import TrainerProfile, ClientProfile, Session
from .forms import SessionForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .models import TrainerProfile, ClientProfile, Session
from .forms import SessionForm
from django.contrib.auth.decorators import login_required

@login_required
def add_session(request):
    trainer = getattr(request.user, 'trainerprofile', None)  # logged-in trainer
    clients = ClientProfile.objects.all()  # or filter by trainer if needed

    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.trainer = trainer  # assign trainer
            session.save()
            return redirect('trainer_dashboard')
        else:
            print(form.errors)  # debug if form invalid
    else:
        form = SessionForm()

    context = {
        'form': form,
        'clients': clients,  # pass correctly
    }
    return render(request, 'add_session.html', context)

# Home/views.py
from django.shortcuts import render
@login_required

def upload_report(request):
    # Your upload logic here
    return render(request, 'trainer/upload_report.html')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Only if you want to test without CSRF errors; otherwise keep CSRF protection
def save_workout(request):
    if request.method == "POST":
        workout = request.POST.get("workout")
        duration = request.POST.get("duration")
        calories = request.POST.get("calories")
        # You can save this data to your DB if needed
        print(workout, duration, calories)  # For testing
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"}, status=400)



# Home/views.py
from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from Home.models import TrainerProfile, Workout

from Home.models import Workout, TrainerProfile, Plan

# Home/views.py
# views.py
from Home.models import Workout, TrainerProfile, Plan
from django.shortcuts import render, redirect, get_object_or_404
from .forms import WorkoutForm




def add_diet(request):
    if request.method == 'POST':
        # handle form submission
        pass
    return render(request, 'add_diet.html')


@login_required
def trainer_dashboard(request):
    # Get the TrainerProfile instance for the logged-in user
    trainer = getattr(request.user, 'trainerprofile', None)
    if not trainer:
        return redirect('create_trainer_profile')

    # Workouts created by this trainer
    workouts = Workout.objects.filter(trainer=trainer)

    # Sessions created by this trainer
    sessions = Session.objects.filter(trainer=trainer)
    total_sessions = sessions.count()

    # Total earnings
    total_earnings = Earning.objects.filter(trainer=trainer).aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'trainer': trainer,
        'workouts': workouts,
        'sessions': sessions,
        'total_sessions': total_sessions,
        'total_earnings': total_earnings,
    }

    return render(request, 'trainer_dashboard.html', context)

def assign_workout(request):
    return render(request, 'assign_workout.html')

def delete_workout(request):
    return render(request,"delete_workout")

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TrainerProfileForm
from .models import TrainerProfile

@login_required
def trainer_profile_update(request):
    if not hasattr(request.user, 'trainerprofile'):
        messages.error(request, "Access denied!")
        return redirect('home')

    trainer = getattr(request.user, 'trainerprofile', None)

    if request.method == 'POST':
        form = TrainerProfileForm(request.POST, request.FILES, instance=trainer)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully ✅")
            return redirect('trainer_dashboard')
    else:
        form = TrainerProfileForm(instance=trainer)

    return render(request, 'trainer_profile_update.html', {'form': form})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TrainerProfile
from .forms import TrainerProfileForm

@login_required
def create_trainer_profile(request):

    # ✅ If already exists → go dashboard (STOP LOOP)
    if TrainerProfile.objects.filter(user=request.user).exists():
        return redirect('trainer_dashboard')

    if request.method == 'POST':
        form = TrainerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            trainer = form.save(commit=False)
            trainer.user = request.user
            trainer.save()
            messages.success(request, "Profile Created Successfully!")
            return redirect('trainer_dashboard')
    else:
        form = TrainerProfileForm()

    return render(request, 'create_trainer_profile.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from Home.models import TrainerProfile
from Home.forms import TrainerProfileForm
@login_required
def manage_trainer_profile(request):
    user = request.user
    profile = TrainerProfile.objects.filter(user=user).first()

    if request.method == "POST":
        if profile:
            form = TrainerProfileForm(request.POST, request.FILES, instance=profile)
        else:
            form = TrainerProfileForm(request.POST, request.FILES)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('trainer_dashboard')   # Only redirect after save
    else:
        form = TrainerProfileForm(instance=profile)

    return render(request, 'manage_trainer_profile.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import WorkoutForm
from .models import Workout, TrainerProfile

@login_required
def create_workout(request):
    # Ensure the user is a trainer
    if not hasattr(request.user, 'trainerprofile'):
        messages.error(request, "Access denied! Only trainers can create workouts.")
        return redirect('home')

    trainer = getattr(request.user, 'trainerprofile', None)

    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.trainer = trainer
            workout.save()
            messages.success(request, "Workout created successfully ✅")
            return redirect('trainer_dashboard')
    else:
        form = WorkoutForm()

    return render(request, 'create_workout.html', {'form': form})


def update_workout(request, id):
    workout = Workout.objects.get(id=id)

    if request.method == "POST":
        workout.name = request.POST['name']
        workout.duration_minutes = request.POST['duration']
        workout.calories_burned = request.POST['calories']
        workout.plan = request.POST['plan']
        workout.save()
        return redirect('trainer_dashboard')

    return render(request, 'update_workout.html', {'workout': workout})

    trainer, created = TrainerProfile.objects.get_or_create(user=request.user)



def delete_workout(request, id):
    workout = Workout.objects.get(id=id)
    workout.delete()
    return redirect('trainer_dashboard')




#---- MPIPIP



from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, ClientProfile

@receiver(post_save, sender=CustomUser)
def create_client_profile(sender, instance, created, **kwargs):
    """
    Automatically create a ClientProfile for new users with role='user'.
    """
    if created and instance.role == 'user':
        ClientProfile.objects.create(user=instance)

        
from django.shortcuts import get_object_or_404, redirect
from .models import Trainer, Client

def follow_trainer(request, trainer_id):
    client = Client.objects.get(user=request.user)
    trainer = get_object_or_404(Trainer, id=trainer_id)

    # 🔥 THIS IS YOUR LINE
    client.trainer = trainer
    client.save()

    return redirect('client_dashboard')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Session, TrainerProfile

@login_required
def join_session(request, session_id):
    # Get the session object
    session = get_object_or_404(Session, id=session_id)

    # Check if user is allowed (for example, client who booked it)
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to join a session!")
        return redirect('login')

    # Optional: only clients who booked this session can join
    if hasattr(request.user, 'clientprofile'):
        if request.user.clientprofile not in session.clients.all():
            messages.error(request, "You are not enrolled in this session.")
            return redirect('user_dashboard')

    # Mark session as joined (custom field or logic)
    session.joined_users.add(request.user)
    messages.success(request, f"You have successfully joined the session: {session.title}")
    
    return redirect('user_dashboard')


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SessionForm
from .models import Session, TrainerProfile

@login_required
def schedule_session(request):
    # Ensure user is a trainer
    if not hasattr(request.user, 'trainerprofile'):
        messages.error(request, "Only trainers can schedule sessions!")
        return redirect('home')

    trainer = getattr(request.user, 'trainerprofile', None)

    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.trainer = trainer
            session.save()
            form.save_m2m()  # If you have ManyToMany fields
            messages.success(request, "Session scheduled successfully ✅")
            return redirect('trainer_dashboard')
    else:
        form = SessionForm()

    return render(request, 'trainer/schedule_session.html', {'form': form})



from django.shortcuts import render, get_object_or_404, redirect
from .models import Session, Workout
from datetime import datetime

def update_session(request, id):
    session = get_object_or_404(Session, id=id)

    if request.method == 'POST':
        # Get POST values
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        session_type = request.POST.get('session_type')
        notes = request.POST.get('notes')
        workout_id = request.POST.get('workout')

        # Only assign if date is provided
        if date_str:
            try:
                session.date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return render(request, 'update_session.html', {
                    'session': session,
                    'workouts': Workout.objects.filter(trainer=session.trainer),
                    'error': 'Invalid date format. Use YYYY-MM-DD.'
                })

        # Only assign if time is provided
        if time_str:
            session.time = time_str

        # Assign session_type and notes
        if session_type:
            session.session_type = session_type
        if notes is not None:
            session.notes = notes

        # Assign workout if selected
        if workout_id:
            session.workout = Workout.objects.get(id=workout_id)

        session.save()
        return redirect('trainer_dashboard')

    return render(request, 'update_session.html', {
        'session': session,
        'workouts': Workout.objects.filter(trainer=session.trainer)
    })

# DELETE SESSION
def delete_session(request, id):
    session = get_object_or_404(Session, id=id)
    session.delete()
    return redirect('trainer_dashboard')


from django.contrib.auth.decorators import login_required
from .models import ClientProfile, Session


from django.shortcuts import render, get_object_or_404, redirect
from .models import Workout, Plan
from .forms import WorkoutForm
from django.contrib.auth.decorators import login_required

@login_required
def update_workout(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    plans = Plan.objects.all()  # All plans for dropdown

    if request.method == "POST":
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            return redirect('trainer_dashboard')
        else:
            error = "Please correct the errors below."
    else:
        form = WorkoutForm(instance=workout)
        error = None

    context = {
        'form': form,
        'plans': plans,
        'error': error,
    }
    return render(request, 'update_workout.html', context)


from django.shortcuts import render
from .models import TrainerProfile, Workout, Badge, ClientProfile
from django.shortcuts import render
from .models import Trainer, Workout, Session  # make sure Session exists
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Client, Trainer, Workout, Session
import json
from django.shortcuts import render
from Home.models import Session

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Trainer, Client

@login_required
def follow_trainer(request, trainer_id):
    client = user = request.user
    trainer = get_object_or_404(Trainer, id=trainer_id)
    client.following.add(trainer)
    return redirect('client_dashboard')

@login_required
def unfollow_trainer(request, trainer_id):
    client = user = request.user
    trainer = get_object_or_404(Trainer, id=trainer_id)
    client.following.remove(trainer)
    return redirect('client_dashboard')


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_clients():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "dashboard_updates",
        {
            "type": "send_update",
            "data": {"message": "new_update"}
        }
    )
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TrainerProfile, Workout, Plan

from django.shortcuts import render, redirect
from .forms import WorkoutForm
from django.contrib.auth.decorators import login_required
def add_workout(request):
    plans = Plan.objects.all()
    error = None

    if request.method == "POST":
        name = request.POST.get('name')
        duration = request.POST.get('duration')
        calories = request.POST.get('calories')
        plan_id = request.POST.get('plan')

        try:
            trainer = request.user.trainerprofile
            plan = Plan.objects.get(id=plan_id) if plan_id else None

            Workout.objects.create(
                name=name,
                duration_minutes=duration,   # ✅ correct field
                calories_burned=calories,    # ✅ correct field
                plan=plan,
                trainer=trainer
            )

            return redirect('trainer_dashboard')

        except Exception as e:
            error = str(e)

    return render(request, 'add_workout.html', {'plans': plans, 'error': error})


@login_required
def create_client_profile(request):
    if request.method == 'POST':
        # create profile logic here
        ClientProfile.objects.create(user=request.user)
        return redirect('client_dashboard')
    return render(request, 'create_profile.html')