from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission


# models.py
from django.db import models
from django.conf import settings

# Custom user

from django.contrib.auth.models import AbstractUser



from django.db import models
from django.contrib.auth.models import AbstractUser

# ---------- CUSTOM USER ----------
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('trainer', 'Trainer'),
        ('user', 'User'),
    )
    is_trainer = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(blank=True)
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    fitness_goal = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Trainer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    spec = models.CharField(max_length=100, blank=True)
    exp = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    photo = models.ImageField(upload_to="trainers/", blank=True, null=True)
    hourly_rate = models.PositiveIntegerField(default=500)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True)
    following = models.ManyToManyField('Trainer', blank=True, related_name='followers')
    
    def __str__(self):
        return self.user.username

# Exercise
class Exercise(models.Model):
    EXERCISE_TYPES = [
        ('Yoga', 'Yoga'),
        ('HIIT', 'HIIT'),
        ('Strength Training', 'Strength Training'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exercises')
    name = models.CharField(max_length=50, choices=EXERCISE_TYPES)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    calories = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.name} ({self.date})"
    

# ------------------ Membership Plan & Subscription ------------------
class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_days = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

# ------------------ Transactions ------------------


class DemoTransaction(models.Model):
    order_id = models.CharField(max_length=50)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=(('pending','Pending'), ('success','Success'), ('failed','Failed')),
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_id} - {self.user.username}"

class MembershipTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=(('pending','Pending'), ('success','Success'), ('failed','Failed')),
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

   

# ------------------ Posts & Comments ------------------
class Post(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:30]}"

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    ser = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True,blank=True)    
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"

# ------------------ Trainer Review ------------------
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings  # <-- import settings


class TrainerReview(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # <-- use this instead of User
        on_delete=models.CASCADE
    )
    review_text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} review of {self.trainer}"







# ------------------ Trainer Session & Booking ------------------
from django.db import models
from django.conf import settings

class TrainerSession(models.Model):
    SESSION_TYPES = [
        ('Strength', 'Strength'),
        ('Cardio', 'Cardio'),
        ('Yoga', 'Yoga'),
        ('HIIT', 'HIIT'),
    ]

    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='trainer_sessions'
    )
    title = models.CharField(max_length=100)
    session_type = models.CharField(
    max_length=50, 
    choices=SESSION_TYPES, 
    default='Strength'  # pick a default value
    )
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.trainer}"


class SessionBooking(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    session = models.ForeignKey(TrainerSession, on_delete=models.CASCADE)
    booked_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} booked {self.session.title}"

# ------------------ Trainer Booking ------------------
from django.conf import settings
from django.db import models

class TrainerBooking(models.Model):
    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ← Use this, NOT auth.User
        on_delete=models.CASCADE,
        related_name='trainer_bookings'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_bookings'
    )
    session_date = models.DateField(blank=True,null=True)
    session_time = models.TimeField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trainer} - {self.user} on {self.session_date}"



# ------------------ Trainer Notification ------------------
class TrainerNotification(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.trainer.name} - {self.title}"

# ------------------ Trainer Account ------------------
class TrainerAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)   
    balance = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Account Balance: {self.balance}"

# ------------------ User Progress ------------------
class UserProgress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    weight = models.FloatField(default=0)
    bmi = models.FloatField(default=0)
    exercise = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    progress_date = models.DateField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.user.username} progress on {self.progress_date}"

# ------------------ Contact ------------------
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# other imports if needed

from django.conf import settings


class Earnings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount}"


from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



from django.conf import settings
from django.db import models

class MoodHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    mood = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.mood}"



class YogaVideo(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50)   # morning / power / relaxation
    video_url = models.URLField()
    thumbnail = models.URLField()

    def __str__(self):
        return self.title


from django.conf import settings
from django.db import models

class YogaStreak(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    streak = models.IntegerField(default=0)
    last_completed = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.streak}"

class YogaReminder(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    reminder_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} - {self.reminder_time}"

from django.db import models
from django.conf import settings

class WeightProgress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    week = models.IntegerField(1)
    weight = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Week {self.week}: {self.weight}kg"
    


from django.utils import timezone


class MealPlan(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    date = models.DateField(default=timezone.now)    
    breakfast = models.CharField(max_length=200)
    lunch = models.CharField(max_length=200)
    snack = models.CharField(max_length=200)
    dinner = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user.username} - {self.date}"


# ------------------ Booking ------------------
class Booking(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.trainer}"
    


from django.conf import settings
from django.utils import timezone

class Progress(models.Model):
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='progress_entries',
        default=1  # <-- set the ID of a default user for existing rows
    )
    workout_completed = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)

class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        default=1  # <-- set the ID of a default user for existing rows
    )
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


# ---------------- Notification ----------------
class Notification(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

from django.conf import settings
from django.db import models

class TrainerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100, blank=True)
    experience = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='trainers/', blank=True, null=True)
    followed_clients = models.ManyToManyField('Client', blank=True)

    def __str__(self):
        return self.user.username

#---    workout ---
    

# ==========================
# WorkoutPlan Model
# ==========================

class WorkoutPlan(models.Model):
    trainer = models.ForeignKey(
        'Trainer', on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.trainer.name}"
    



from django.db import models


class Session(models.Model):
    trainer = models.ForeignKey('TrainerProfile', on_delete=models.CASCADE,blank=True,null=True)
    client = models.ForeignKey('ClientProfile', on_delete=models.CASCADE, default=1)  # ID of an existing client    title = models.CharField(max_length=100,blank=True,null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)


    workout = models.ForeignKey('Workout', on_delete=models.SET_NULL, null=True, blank=True)  # 🔥 ADD THIS

    WORKOUT_TYPE = (
        ('Bodyweight Workouts', 'Bodyweight Workouts'),
        ('Cardio', 'Cardio'),
        ('HIIT', 'HIIT'),
        ('Yoga', 'Yoga'),
        ('Dumbell workouts', 'Dumbell workouts'),
    )

    workout_type = models.CharField(max_length=100, choices=WORKOUT_TYPE)

    SESSION_TYPE = (
        ('online', 'Online'),
        ('offline', 'Offline'),
    )
    session_type = models.CharField(
        max_length=10,
        choices=SESSION_TYPE,
        default='online'
    )

    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.date}"
    
    

from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Plan(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)   # Make sure this exists
    plan_name = models.CharField(max_length=50,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    duration_days = models.IntegerField(default=30)


    def __str__(self):
        return self.name  # ✅ must return a string


class Badge(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class DietPlan(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)
    details = models.TextField()


class ClientWorkout(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    workout = models.ForeignKey('Workout', on_delete=models.CASCADE, related_name='client_workouts')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.workout.name}"



class Workout(models.Model):
    name = models.CharField(max_length=100)
    duration_minutes = models.IntegerField(null=True, blank=True)
    calories_burned = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    # ForeignKeys
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

# Earnings
class Earning(models.Model):
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE)    
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    amount = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)



# Home/models.py
from django.db import models
from django.conf import settings  # important

class ClientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
