from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404
from django.urls import reverse
from urllib.parse import urlencode
from django.conf import settings

app = settings.APP_NAME


class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    @staticmethod
    def process_view(request, view_func, view_args, view_kwargs):
        if 'admin' in request.path:
            return redirect('home')
        elif 'logout' in request.path:
            if 'logged_status' not in request.path:
                redirect('home')
        elif 'logged_status' in request.session:
            if str(request.session['usertype']) == 'manufacturer' and 'dashboard' not in request.path:
                return redirect('manu-dashboard')
        else:
            if 'dashboard' in request.path:
                return redirect('home')
