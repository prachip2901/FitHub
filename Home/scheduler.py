from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from datetime import timedelta
from .models import Session

def check_sessions():
    now = timezone.localtime()

    upcoming_time = now + timedelta(minutes=10)

    sessions = Session.objects.filter(
        date=upcoming_time.date(),
        time__hour=upcoming_time.hour,
        time__minute=upcoming_time.minute
    )

    for s in sessions:
        print(f"🔔 Reminder: {s.client.user.username} session at {s.time}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_sessions, 'interval', minutes=1)
    scheduler.start()