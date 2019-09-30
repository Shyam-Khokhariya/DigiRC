from django.shortcuts import redirect
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
        elif 'logged_status' in request.session:
            path = str(request.session['usertype']).lower() + "/dashboard"
            if 'logout' in request.path:
                pass
            elif path not in request.path:
                return redirect(str(request.session['usertype']).lower() + "-dashboard")
        elif 'dashboard' in request.path:
            return redirect('home')
