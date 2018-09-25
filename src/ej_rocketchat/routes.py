from logging import getLogger

from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import redirect

from boogie.router import Router
from ej_users.routes import login as ej_login
from . import forms
from .decorators import security_policy, requires_rc_perm
from .models import RCConfig, RCAccount
from .rocket import rocket

log = getLogger('ej')
app_name = 'ej_rocketchat'
urlpatterns = Router(
    template=['ej_rocketchat/{name}.jinja2'],
)


@urlpatterns.route('', decorators=[requires_rc_perm, security_policy])
def iframe(request):
    ask_password_form = None
    ask_password = False

    # Superuser must type the password since it is not stored in the database
    if request.user.is_superuser:
        ask_password = True
        password, ask_password_form = ask_admin_password(request)
        token = rocket.admin_token
        username = rocket.admin_username
        if password:
            rocket.password_login(rocket.admin_username, password)
            ask_password = False

    else:
        account = rocket.find_or_create_account(request.user)
        #account = rocket.login(request.user)
        if account is None:
            print('aaaaaaaaaaaaaaaaaaaaaaaaccount')
            return redirect('rocket:register')
        
        print(dir(account))
        account = rocket.login(request.user)
        token = account.auth_token
        #print(token)
        username = account.username
        user_rc_id = account.user_rc_id
        #print(test.auth_token)

    return {
        'rocketchat_url': rocket.url,
        'username': username,
        'auth_token': token,
        'auth_token_repr': repr(token),
        'user_id': user_rc_id,
        'ask_password_form': ask_password_form,
        'ask_password': ask_password,
    }


def ask_admin_password(request):
    password = None
    form = forms.AskAdminPasswordForm.bind(request)
    if form.is_valid_post():
        password = form.cleaned_data['password']
    return password, form


@urlpatterns.route('register/', decorators=[requires_rc_perm, security_policy])
def register(request):
    if RCAccount.objects.filter(user=request.user).exists():
        return redirect('rocket:iframe')

    form = forms.CreateUsernameForm.bind(request, user=request.user)
    if form.is_valid_post():
        return redirect('rocket:iframe')
    return {'form': form}


@urlpatterns.route('config/', decorators=[security_policy])
def config(request):
    if not request.user.is_superuser:
        raise Http404

    config = RCConfig.objects.default_config(raises=False)
    form_kwargs = {}
    if config:
        form_kwargs['data'] = {'rocketchat_url': config.url}
    form = forms.RocketIntegrationForm.bind(request, **form_kwargs)

    if form.is_valid_post():
        password = form.cleaned_data['password']
        username = form.cleaned_data['username']
        rocket.password_login(username, password)
        return redirect('rocket:iframe')

    return {'form': form}


@urlpatterns.route('intro/', login=True, decorators=[security_policy])
def intro():
    return {}


@urlpatterns.route('login/',
                   decorators=[security_policy],
                   template='ej_users/login.jinja2')
def login(request):
    log.info(f'login attempt via /talks/login: {request.user}')
    if request.user.is_authenticated:
        return redirect(request.GET.get('next', ['/talks/'])[0])
    return ej_login(request, redirect_to='/talks/')


@urlpatterns.route('check-login/',
                   decorators=[security_policy])
def check_login(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    if request.user.is_superuser:
        auth_token = rocket.admin_token
    else:
        auth_token = rocket.get_auth_token(request.user)
    return JsonResponse({'loginToken': auth_token})
