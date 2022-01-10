from django.apps import AppConfig

# All functions of webapp is running at 'landing' app
class LandingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'landing'
