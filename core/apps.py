from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    This class is responsible for configuring the behavior of the 'core' app
    within a Django project. It sets the default auto field to 'BigAutoField'
    for models within the 'core' app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
