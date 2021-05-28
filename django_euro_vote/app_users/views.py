from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Setting
from django.contrib.auth.mixins import UserPassesTestMixin

class AllowNewUsersTest(UserPassesTestMixin):
    def test_func(self):
        setting = Setting.objects.get(id=1)
        return setting.allow_new_users

class SignUpView(AllowNewUsersTest, generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'app_users/signup.html'

