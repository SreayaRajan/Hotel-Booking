from django.contrib.auth.backends import ModelBackend
from home.models import UserProfile  # Import your custom user model

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(email=email)
            if user.check_password(password):  # Check the password
                return user
        except UserProfile.DoesNotExist:
            return None
