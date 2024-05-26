from django.shortcuts import redirect
from django.urls import resolve
from home.models import Module
from django.contrib import messages

class ModulePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        resolved_path = resolve(request.path)
        path_segments = resolved_path.route.split('/') 
        if user.is_authenticated:
            for segment in path_segments:
                try:
                    module = Module.objects.get(module_code=segment)
                    
                    user_permissions = user.permissions.all()
                    has_permission = any(module in permission.modules.all() for permission in user_permissions)

                    if not has_permission:
                        messages.error(request, "You do not have permission to access this module!")
                        return redirect('/home/error/')
                except Module.DoesNotExist:
                    pass
        
        return self.get_response(request)
