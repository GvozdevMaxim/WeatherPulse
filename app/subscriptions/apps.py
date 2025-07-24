from django.apps import AppConfig


class SubscriptionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.subscriptions'

    def ready(self):
        import app.subscriptions.tasks
        from django.db.utils import OperationalError, ProgrammingError
        try:
            from app.subscriptions.periodic_setup import setup_periodic_tasks
            setup_periodic_tasks()
        except (OperationalError, ProgrammingError):
            pass

