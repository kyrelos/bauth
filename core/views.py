from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate
import uuid


from core.models import *
from core.forms import *
from core import tasks
import random
from django.conf import settings
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, login as auth_login, logout
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm
)
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.sessions.models import Session


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.

    :param request:
    :param template_name:
    :param redirect_field_name:
    :param authentication_form:
    :param current_app:
    :param extra_context:
    :return: HttpResponse
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            account = form.get_user()
            try:
                Session.objects.get(session_key=account.active_session_key).delete()
            except ObjectDoesNotExist:
                pass
            auth_login(request, account)
            token = str(random.randint(0, 1000000))
            MyToken.objects.create(token=token, account=account)
            tasks.send_message.apply_async(countdown=1, args=[token])
            account.active_session_key = request.session.session_key
            account.secondary_auth = False
            account.save()

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


def register_page(request):
    """
    A view Register new users

    :param request:
    :return: HttpResponse
    """

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # import pdb;pdb.set_trace()
            account = Account.objects.create(email=form.cleaned_data['email'],
                                             phone=form.cleaned_data['phone'],
                                             username=form.cleaned_data['username'],
                                             first_name=form.cleaned_data['first_name'],
                                             last_name=form.cleaned_data['last_name'])
            account.set_password(form.cleaned_data['password'])
            phone_token = str(random.randint(0, 1000000))
            email_token = uuid.uuid1()
            MyToken.objects.create(token=phone_token, account=account)
            MyToken.objects.create(token=email_token, account=account)
            account.active_session_key = request.session.session_key
            account.save()
            tasks.send_message.apply_async(countdown=1, args=[phone_token])
            tasks.send_email.apply_async(countdown=1, args=[email_token,
                                                              request.get_host() + '/verify_email/?token={0}'.format(
                                                                  email_token)])
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            auth_login(request, user)

            return HttpResponseRedirect('/verify_phone/')
        else:
            return render(request, 'core/register.html', {'form': form})

    return render(request, 'core/register.html', {})


@login_required(login_url='/accounts/login/')
def verify_page(request):
    """
    A view to handle token validation

    :param request:
    :return: HttpResponse
    """
    if request.user.is_verified and request.user.secondary_auth:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = VerifyPhoneForm(request.POST)
            if form.is_valid():
                token = MyToken.objects.get(token=form.cleaned_data['token'])
                account = token.account
                if account == request.user:
                    if not account.is_phone_validated:
                        account.is_phone_validated = True
                    account.secondary_auth = True
                    account.save()
                    token.delete()
                    if account.is_verified:
                        return HttpResponseRedirect('/')
                    else:
                        return render(request, 'core/verify_phone.html', {'form': form})
                else:
                    form.add_error('token', ValidationError('Token Invalid'))
                    return render(request, 'core/verify_phone.html', {'form': form})
            else:
                return render(request, 'core/verify_phone.html', {'form': form})
        else:
            return render(request, 'core/verify_phone.html', {})


def verify_email(request):
    """
    A view to verify email address

    :param request:
    :return: HttpResponse
    """
    if request.method == 'GET':
        email_token = request.GET.get('token')
        if email_token:
            try:
                token = MyToken.objects.get(token=email_token)
                account = token.account
                if not account.is_email_validated:
                    account.is_email_validated = True
                    account.save()
                token.delete()
                if request.user == account:
                    return HttpResponseRedirect('/verify_phone/')
                else:
                    try:
                        logout(request)
                        Session.objects.get(session_key=account.active_session_key).delete()
                    except ObjectDoesNotExist:
                        pass
                    return HttpResponseRedirect('/verify_phone/')
            except ObjectDoesNotExist as e:
                logger.exception('email_token_not_found', exception=e.message)
                return HttpResponseRedirect('/verify_phone/')
            except MultipleObjectsReturned as e:
                MyToken.objects.filter(token=email_token).delete()
                logger.exception('email_token_duplicate', exception=e.message)
                return HttpResponseRedirect('/regenerate_token/?type=email')
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponse(status=405)

@login_required(login_url='/accounts/login/')
def regenrate_token(request):
    """
    A view to regenerate tokens

    :param request:
    :return: HttpResponse
    """
    if request.method == 'GET':
        token_type = request.GET.get('type')
        if token_type == 'email':
            email_token = uuid.uuid1()
            MyToken.objects.create(token=email_token, account=request.user)
            tasks.send_email.apply_async(countdown=1, args=[email_token,
                                                          request.get_host() + '/verify_email/?token={0}'.format(
                                                              email_token)])
        elif token_type == 'phone':
            phone_token = str(random.randint(0, 1000000))
            MyToken.objects.create(token=phone_token, account=request.user)
            tasks.send_message.apply_async(countdown=1, args=[phone_token])

        else:
            pass

        return HttpResponseRedirect('/verify_phone/')
    else:
        return HttpResponse(status=405)
