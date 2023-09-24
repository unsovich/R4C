from django.apps import AppConfig


class RobotsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # для поддержки больших автоинкрементных полей
    name = 'robots'
