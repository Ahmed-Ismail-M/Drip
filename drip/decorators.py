from django.http import HttpResponse

def auth_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("Not Authorized")
    return wrapper_func

def allowed_users(allowed_roles: list):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            print(request.user.groups.all()[0].name)
            if request.user.groups.exists():
                if request.user.groups.all()[0].name in allowed_roles:
                    return view_func(request, *args, **kwargs)
            return HttpResponse("Not Authorized")
        return wrapper_func
    return decorator

