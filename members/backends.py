from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get(email=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
