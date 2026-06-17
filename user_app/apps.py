from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_fields='django.db.models.BigAutoField'
    name = 'user_app'
    label='my_custom_user'
