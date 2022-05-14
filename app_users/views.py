from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Setting
from django.contrib.auth.mixins import UserPassesTestMixin
from app_users.models import ALLOW_NEW_USERS
from django.core.exceptions import ObjectDoesNotExist

class AllowNewUsersTest(UserPassesTestMixin):
    def test_func(self):
        try:
            setting : Setting = Setting.objects.get(name=ALLOW_NEW_USERS)
            return setting.enable
        except ObjectDoesNotExist as e:
            print(f"Create a setting for >> {ALLOW_NEW_USERS}")
            return True

class SignUpView(AllowNewUsersTest, generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'app_users/signup.html'

