from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model for the organization platform.

    We inherit Django's authentication functionality
    and leave room for future organizational features.
    """

    pass