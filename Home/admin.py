from django.contrib import admin
from .models import (
     ClientWorkout, Contact, CustomUser, Exercise, MembershipPlan, UserSubscription,
     Post, Comment, MembershipTransaction,
    Trainer, TrainerReview, TrainerNotification,
    TrainerSession,  UserProgress, TrainerBooking, Workout, WorkoutPlan,
)

from django.conf import settings
from django.db import models
from .models import *
from django.contrib.auth.admin import UserAdmin




# ------------------ Helper decorator ------------------
def safe_register(model):
    """
    Decorator to safely register a model with admin.
    Unregisters first if already registered.
    """
    def decorator(admin_class):
        if model in admin.site._registry:
            admin.site.unregister(model)
        admin.site.register(model, admin_class)
        return admin_class
    return decorator

# ------------------ Contact ------------------
@safe_register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')
    search_fields = ('name', 'email', 'message')
    ordering = ('-created_at',)

class TrainerReviewInlineForUser(admin.TabularInline):
    model = TrainerReview
    extra = 0
    readonly_fields = ('user', 'rating', 'review_text', 'created_at')
    can_delete = False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only show reviews if the user is a trainer
        return qs.filter(trainer__user=self.parent_object) if hasattr(self, 'parent_object') else qs.none()

class TrainerBookingInlineForUser(admin.TabularInline):
    model = TrainerBooking
    extra = 0
    readonly_fields = ('user', 'session_date', 'session_time', 'created_at')
    can_delete = False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(trainer__user=self.parent_object) if hasattr(self, 'parent_object') else qs.none()

# ----------------- CustomUser Admin -----------------
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')    
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)
    readonly_fields = ('role',)  # Optional: make role readonly

    # Only show trainer-related inlines if the user is a trainer
    def get_inline_instances(self, request, obj=None):
        inlines = []
        if obj and obj.role == 'Trainer':
            inlines = [TrainerReviewInlineForUser, TrainerBookingInlineForUser]
        return [inline(self.model, self.admin_site) for inline in inlines]

@admin.register(TrainerBooking)
class TrainerBookingAdmin(admin.ModelAdmin):
    list_display = ("trainer", "user", "session_date", "session_time")
    list_filter = ("trainer", "session_date")

    
# ------------------ Exercise ------------------
@safe_register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'duration', 'calories', 'date')
    list_filter = ('date', 'name')
    search_fields = ('user__username', 'name')
    ordering = ('-date',)


# ------------------ MembershipPlan ------------------
@safe_register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days')
    search_fields = ('name',)
    ordering = ('price',)

# ------------------ UserSubscription ------------------
@safe_register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'active')
    list_filter = ('active', 'plan')
    search_fields = ('user__username', 'plan__name')
    ordering = ('-start_date',)



@safe_register(MembershipTransaction)
class MembershipTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'amount', 'status', 'created_at', 'order_id')
    list_filter = ('status', 'plan')
    search_fields = ('user__username', 'plan__name', 'order_id')
    ordering = ('-created_at',)

# ------------------ Post & Comment ------------------
@safe_register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('text_preview', 'user', 'likes', 'created_at')
    search_fields = ('text', 'user__username')
    ordering = ('-created_at',)

    def text_preview(self, obj):
        return obj.text[:50] if obj.text else "(No text)"
    text_preview.short_description = 'Post Text'

from django.contrib import admin
from .models import Comment


admin.site.register(Comment)


# ------------------ Trainer ------------------
from django.contrib import admin
from .models import Trainer

@safe_register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ("name", "spec", "exp", "hourly_rate", "is_verified")
    list_filter = ("is_verified", "spec")
    search_fields = ("name", "spec")


# ------------------ TrainerReview ------------------
@admin.register(TrainerReview)
class TrainerReviewAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'user', 'rating', 'created_at')
    list_filter = ('trainer', 'rating', 'created_at')
    search_fields = ('trainer__name', 'user__username', 'review_text')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

# ------------------ TrainerBooking ------------------
@safe_register(TrainerBooking)
class TrainerBookingAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'user', 'session_date', 'session_time', 'created_at')
    list_filter = ('trainer', 'session_date')
    search_fields = ('trainer__name', 'user__username')
    ordering = ('-session_date', 'session_time')
    readonly_fields = ('created_at',)


# ------------------ TrainerSession & SessionBooking ------------------


from django.contrib import admin
from .models import TrainerSession


@admin.register(TrainerSession)
class TrainerSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'trainer', 'session_type', 'date', 'time')
    list_filter = ('session_type', 'date')
    search_fields = ('title', 'trainer__username')




# ------------------ TrainerNotification ------------------
@safe_register(TrainerNotification)
class TrainerNotificationAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'title', 'message', 'is_read', 'created_at')
    list_filter = ('trainer', 'is_read', 'created_at')
    search_fields = ('trainer__name', 'title', 'message')
    ordering = ('-created_at',)



# ------------------ UserProgress ------------------
@safe_register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight', 'bmi', 'progress_date')
    list_filter = ('progress_date',)
    search_fields = ('user__username',)
    ordering = ('-progress_date',)




# ------------------ WorkoutPlan Admin ------------------
@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'trainer', 'created_at')
    list_filter = ('trainer', 'created_at')
    search_fields = ('title', 'trainer__name')
    ordering = ('-created_at',)


from django.contrib import admin
from .models import Workout, Plan, ClientWorkout

class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan', 'duration_minutes', 'calories_burned')

admin.site.register(Workout, WorkoutAdmin)
admin.site.register(Plan)
admin.site.register(ClientWorkout)