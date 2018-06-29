from django.views import generic

from user.forms import UserRegisterForm


class IndexView(generic.TemplateView):
    # Index View
    template_name = 'user/index.html'


class RegisterView(generic.FormView):
    template_name = 'user/register.html'
    form_class = UserRegisterForm
    success_url = ''
