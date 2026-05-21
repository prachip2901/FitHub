from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.conf import settings
from .models import (
    ClientProfile, CustomUser, Trainer, Client, TrainerProfile, TrainerSession, TrainerReview,
    SessionBooking, UserProgress, MembershipPlan, UserSubscription,
    Post, Comment, Contact, Workout
)

# Helper to apply Bootstrap classes
def bootstrap_field(widget, placeholder=""):
    widget.attrs.update({'class': 'form-control', 'placeholder': placeholder})
    return widget


# ------------------ User Forms ------------------
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            placeholder = f"Enter {field.label}"
            field.widget = bootstrap_field(field.widget, placeholder)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']  # 'paid' remove

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            placeholder = f"Enter {field.label}"
            field.widget = bootstrap_field(field.widget, placeholder)



# ------------------ Trainer Profile Form ------------------

from django import forms
from .models import TrainerProfile

from django import forms
from .models import TrainerProfile

class TrainerProfileForm(forms.ModelForm):
    class Meta:
        model = TrainerProfile
        fields = ['specialization', 'experience', 'price', 'bio', 'profile_image']
        widgets = {
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E.g., Yoga, Cardio, Strength Training'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your experience in years'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your session price'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write a short bio about yourself'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# ------------------ Client Forms ------------------
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['user', 'trainer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-select'})


# ------------------ Trainer Session Forms ------------------
from django import forms
from .models import TrainerSession

class TrainerSessionForm(forms.ModelForm):
    class Meta:
        model = TrainerSession
        fields = ['title', 'session_type', 'date', 'time', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'session_type': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# ------------------ Trainer Review Forms ------------------
class TrainerReviewForm(forms.ModelForm):
    class Meta:
        model = TrainerReview
        fields = ['trainer', 'review_text', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['review_text'].widget = forms.Textarea(
            attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Write your review...'}
        )
        self.fields['rating'].widget = forms.NumberInput(
            attrs={'min': 1, 'max': 5, 'class': 'form-control', 'placeholder': 'Rating 1-5'}
        )
        self.fields['trainer'].widget.attrs.update({'class': 'form-select'})


# ------------------ Session Booking Forms ------------------
class SessionBookingForm(forms.ModelForm):
    class Meta:
        model = SessionBooking
        fields = ['session', 'user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['session'].widget.attrs.update({'class': 'form-select'})
        self.fields['user'].widget.attrs.update({'class': 'form-select'})

from django import forms
from .models import Session
# Session Form
# -------------------------------
from django import forms
from .models import Session, ClientProfile, Workout
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        # Exclude trainer; we assign it in the view
        fields = ['client', 'workout', 'session_type', 'date', 'time', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Optional notes'}),
        }

    def __init__(self, *args, **kwargs):
        trainer = kwargs.pop('trainer', None)  # allow passing trainer to filter clients
        super().__init__(*args, **kwargs)

        # Style all fields
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class') is None:
                field.widget.attrs['class'] = 'form-control'

        # Client dropdown: filter only clients related to this trainer (if trainer provided)
        if trainer:
            self.fields['client'].queryset = ClientProfile.objects.filter(trainer=trainer)
        else:
            self.fields['client'].queryset = ClientProfile.objects.all()

        # Workout dropdown: show only active workouts

        
class UserProgressForm(forms.ModelForm):
    class Meta:
        model = UserProgress
        fields = ['weight', 'bmi', 'exercise', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['exercise'].widget = forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Exercises done today'})
        self.fields['notes'].widget = forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Additional notes'})
        self.fields['weight'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Weight in kg'})
        self.fields['bmi'].widget.attrs.update({'class': 'form-control', 'placeholder': 'BMI'})




# ------------------ Membership Plan & Subscription Forms ------------------
class MembershipPlanForm(forms.ModelForm):
    class Meta:
        model = MembershipPlan
        fields = ['name', 'price', 'duration_days']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': f"Enter {field.label}"})

class UserSubscriptionForm(forms.ModelForm):
    class Meta:
        model = UserSubscription
        fields = ['user', 'plan', 'end_date', 'active']  # removed start_date

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update({'class': 'form-select'})
        self.fields['plan'].widget.attrs.update({'class': 'form-select'})
        self.fields['end_date'].widget.attrs.update({'class': 'form-control', 'type': 'date'})
        self.fields['active'].widget.attrs.update({'class': 'form-check-input'})



# ------------------ Post & Comment Forms ------------------
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget = forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Write something...'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget = forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Add a comment...'})


# ------------------ Contact Form ------------------
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your email'})
        self.fields['message'].widget.attrs.update({'class': 'form-control', 'rows': 4, 'placeholder': 'Your message'})


from django import forms
from .models import TrainerAccount

class TrainerAccountForm(forms.ModelForm):
    class Meta:
        model = TrainerAccount
        fields = ['user', 'balance']  # usually, 'created' and 'updated' are not editable
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }

from django import forms

class CalculatorForm(forms.Form):
    age = forms.IntegerField(min_value=10, max_value=100)
    height = forms.FloatField(min_value=50, max_value=250)
    weight = forms.FloatField(min_value=20, max_value=200)
    gender = forms.ChoiceField(choices=[('male','Male'),('female','Female')])
    activity = forms.ChoiceField(choices=[('1.2','Sedentary'),('1.375','Lightly Active'),
                                          ('1.55','Moderately Active'),('1.725','Very Active')])
    goal = forms.ChoiceField(choices=[('0','Maintain Weight'),('-300','Fat Loss -300 kcal'),
                                      ('-500','Aggressive Fat Loss -500 kcal')])



from django import forms
from .models import Workout, Plan
from django import forms
from .models import Workout

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'duration_minutes', 'calories_burned', 'description', 'title', 'plan']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Workout Name'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration (minutes)'}),
            'calories_burned': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Calories'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'plan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Plan'}),
        }


# class WorkoutForm(forms.ModelForm):
   #--- class Meta:
     #   model = Workout
     #   fields = ['title', 'description', 'plan']

   #  plan = forms.ModelChoiceField(queryset=Plan.objects.all(), empty_label="Select Plan")
class TrainerForm(forms.ModelForm):
    class Meta:
        model = TrainerProfile
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specialization'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Experience (Years)'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Session Price'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bio'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }