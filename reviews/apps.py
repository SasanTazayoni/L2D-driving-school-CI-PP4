from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """
    This class represents the configuration for the 'reviews' app within a Django project.
    It sets the default auto field to 'BigAutoField' for models within the 'reviews' app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'
