from django.apps import AppConfig



from django.apps import AppConfig
import sys

class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Home'

    def ready(self):
        # 🔥 RUN ONLY IN MAIN SERVER (avoid error)
        if 'runserver' in sys.argv:
            from .scheduler import start_scheduler
            start_scheduler()


