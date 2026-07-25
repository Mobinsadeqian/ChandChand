from django.apps import AppConfig


class MatchesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'matches'

    def ready(self):
        import os
        if os.environ.get('RUN_MAIN') != 'true':
            return

        from apscheduler.schedulers.background import BackgroundScheduler
        from .services import fetch_and_update_api_data

        scheduler = BackgroundScheduler()

        scheduler.add_job(fetch_and_update_api_data, 'interval', minutes=10)
        scheduler.start()
        


