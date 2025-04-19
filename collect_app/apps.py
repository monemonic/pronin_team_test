from django.apps import AppConfig


class CollectAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collect_app'

    def ready(self) -> None:
        """Импортирование сигналов для приложения."""
        import collect_app.signals