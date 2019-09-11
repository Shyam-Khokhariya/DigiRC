from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
from urllib.parse import urlencode


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
        elif 'logged_status' in request.session:
            if any(path in request.path for path in {'login'}):
                return redirect('home')
        else:
            if "logout" in request.path:
                return redirect('login')
