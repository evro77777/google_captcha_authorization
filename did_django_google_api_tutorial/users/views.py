from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView

from did_django_google_api_tutorial.mixins import form_errors, AjaxFormMixin, \
    recaptcha_validation
from users.forms import UserProfileForm, AuthForm, UserForm

result = 'Error'
message = 'Error message'

class AccountView(TemplateView):
    template_name = 'users/account.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def give_response(result, message):
    data = {'result': result, 'message': message}
    return JsonResponse(data)




def profile_view(request):
    user = request.user
    up = user.userprofile
    form = UserProfileForm(instance=up, data=request.POST)
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if form.is_valid():
            obj = form.save()
            obj.has_profile = True
            obj.save()
            return give_response(result='Success', message='Your profile has been updated.')
        else:
            return give_response(result='Error', message='There was an error, please try again.')
    return render(request, 'users/profile.html', {'form': form})




class SignUpView(AjaxFormMixin, FormView):
    template_name = 'users/sign_up.html'
    form_class = UserForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recaptcha_site_key'] = settings.RECAPTCHA_PUBLIC_KEY
        return context

    def form_valid(self, form):
        global result, message
        response = super().form_valid(form)
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            token = form.cleaned_data.get('token')
            captcha = recaptcha_validation(token)
            if captcha['success']:
                obj = form.save()
                obj.email = obj.username
                obj.save()
                up = obj.userprofile
                up.captcha_score = float(captcha['score'])
                up.save()

                login(self.request, obj, backend='django.contrib.auth.backends.ModelBackend')
                return give_response(result='Success', message='You are logged in.')
            else:
                return give_response(result='Error', message='There was an error, please try again.')

        return response


class SignInView(AjaxFormMixin, FormView):
    template_name = 'users/sign_in.html'
    form_class = AuthForm
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(self.request, username=username, password=password)
            if user:
                login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
                return give_response(result='Success', message='You are  logged in.')
            else:
                return give_response(result='Error', message=form_errors(form))
            # return give_response(result='Error', message='There was an error, please try again.')
        return response


def sign_out(request):
    logout(request)
    return redirect(reverse('users:sign-in'))
