from django.urls import path
from Home import views
from django.conf import settings
from django.conf.urls.static import static
from .views import forgot_password, reset_password, reset_password, trainer_profile_update, verify_email, verify_email
# ✅ Correct import
from .views import (
    forgot_password,
    reset_password,
    trainer_profile_update,
    verify_email
)
# WRONG: top-level import in urls.py or settings.py
from Home.models import TrainerProfile

urlpatterns = [
    path('', views.index, name='home'),


    # Pages
    path('save-mood/', views.save_mood, name='save_mood'),
    path('save-progress/', views.save_progress, name='save_progress'),
    path('yoga/', views.yoga, name='yoga'),
 
    path("weightloss/", views.weightloss, name="weightloss"),
    path('add_weight/', views.add_weight, name='add_weight'),
   
    path('dietplans/', views.dietplans, name='dietplans'),
    path('strengthtraining/', views.strenghtraining, name='strenghtraining'),
    path('cardio/', views.cardio, name='cardio'),
    path('hiit/', views.hiit, name='hiit'),

    # Trainers Hub
  # Trainers Hub
    path('trainers/', views.trainers_hub, name='trainers_hub'),
    path('client_dashboard/',views.client_dashboard,name= 'client_dashboard'),
    path('book_session/', views.book_session, name='book_session'),
    path('trainer/<int:trainer_id>/review/', views.submit_review, name='submit_review'),

    path('get_trainers/', views.get_trainers, name='get_trainers'),

   path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('client/follow/<int:trainer_id>/', views.follow_trainer, name='follow_trainer'),
    path('client/unfollow/<int:trainer_id>/', views.unfollow_trainer, name='unfollow_trainer'),

    

    # Membership
    path('membership/', views.membership_page, name='membership'),
    path('membership/create/<int:plan_id>/', views.create_transaction, name='create_transaction'),
    path('membership/callback/', views.payment_callback, name='payment_callback'),

    # Progress / API
    path('progress/', views.progress_page, name='progress_page'),
    path('api/exercises/', views.exercise_api, name='exercise_api'),

    # Community

    path('community/', views.community, name='community'),
    path('api/posts/', views.get_posts, name='get_posts'),
    path('api/posts/create/', views.create_post, name='create_post'),
    path('api/posts/<int:post_id>/like/', views.like_post, name='like_post'),
    path('api/posts/<int:post_id>/comment/', views.add_comment, name='add_comment'),


    # Dashboard

    # Contact
    path('contact/', views.contact, name='contact'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('trainer/dashboard/', views.trainer_dashboard, name='trainer_dashboard'),
    path('trainer/analytics/',views.trainer_analytics, name='trainer_analytics'),
    path('trainer/session/manage/<int:session_id>/', views.manage_session, name='edit_session'),
    path('trainer/session/manage/', views.manage_session, name='create_session'),
    path('trainer/session/<int:session_id>/users/', views.session_users, name='session_users'),
    path('trainer/user/<int:user_id>/progress/', views.add_user_progress, name='add_user_progress'),

    #trainer side
    path('trainer/clients/', views.trainer_clients, name='trainer_clients'),
    path('trainer/earnings/', views.trainer_earnings, name='trainer_earnings'),
    path('trainer/reviews/', views.trainer_reviews, name='trainer_reviews'),
    path('trainer/notifications/', views.trainer_notifications, name='trainer_notifications'), 
    path('trainer/sessions/', views.trainer_sessions, name='trainer_sessions'),
    path('trainer/view_client/<int:client_id>/', views.trainer_view_client, name='trainer_view_client'),
    path('trainer/clients/add/', views.add_client, name='add_client'),
    path('trainer/profile/update/', views.trainer_profile_update, name='trainer_profile_update'),
    
    path('trainer/add-workout/', views.add_workout, name='add_workout'),
    path('trainer/add-diet/', views.add_diet, name='add_diet'),
    path('add-session/', views.add_session, name='add_session'),


    path("booking/<int:id>/<str:action>/", views.booking_action, name="booking_action"),
    path("trainer/analytics/", views.trainer_analytics, name="trainer_analytics"),
    path("trainer/session/approve/<int:booking_id>/", views.approve_session, name="approve_session"),
    path("trainer/session/reject/<int:booking_id>/", views.reject_session, name="reject_session"),
path("trainer/session/complete/<int:booking_id>/", views.complete_session, name="complete_session"),

    path('trainer/session/add/', views.add_session, name='add_session'),
# Home/urls.py
path('trainer/session/start/', views.strenghtraining, name='start_training'),
    path('trainer/upload-report/', views.upload_report, name='upload_report'),

    path('trainer/create-profile/', views.create_trainer_profile, name='create_trainer_profile'),

    # Workout URLs
    path('trainer/workout/create/', views.create_workout, name='create_workout'),

    # Join Session
    path('trainer/session/<int:session_id>/join/', views.join_session, name='join_session'),

    # Profile Update
    path('trainer/profile/update/', views.trainer_profile_update, name='trainer_profile_update'),
    path('save-workout/', views.save_workout, name='save_workout'),  # ✅ This is important


    path("verify/<uidb64>/<token>/", verify_email, name="verify"),
    path("forgot-password/", forgot_password, name="forgot_password"),
    path("reset/<uidb64>/<token>/", reset_password, name="reset_password"),
    path('send-otp/', views.send_otp, name='send_otp'),


    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
# trainer signup

    path('trainer/workout/create/', views.create_workout, name='create_workout'),
    path('trainer/session/schedule/', views.schedule_session, name='schedule_session'),
    path('session/join/<int:session_id>/', views.join_session, name='join_session'),

    path('workout/delete/<int:id>/', views.delete_workout, name='delete_workout'),
    path('assign-workout/', views.assign_workout, name='assign_workout'),

    path('follow-trainer/<int:trainer_id>/', views.follow_trainer, name='follow_trainer'),
# straight trainning save historyyy

    path('add-workout/', views.add_workout, name='add_workout'),
# urls.py
    path('update-workout/<int:pk>/', views.update_workout, name='update_workout'),    # urls.py
    path('delete-workout/<int:id>/', views.delete_workout, name='delete_workout'),
    path('add-session/', views.add_session, name='add_session'),
    path('update-session/<int:id>/', views.update_session, name='update_session'),
    path('delete-session/<int:id>/', views.delete_session, name='delete_session'),
    path('update-workout/<int:pk>/', views.update_workout, name='update_workout'),

path('trainers/', views.trainers_hub, name='trainers_hub'),

]



   
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
