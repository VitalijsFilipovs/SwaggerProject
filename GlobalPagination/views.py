from rest_framework import viewsets, permissions
from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskSerializer
from .permissions import IsOwnerOrReadOnly

from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import SignUpForm

def home(request):
    return HttpResponse("<h1>Welcome to SwaggerProject</h1>"
                        "<p><a href='/swagger/'>Swagger</a> | <a href='/redoc/'>Redoc</a></p>")

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return SubTask.objects.filter(owner=self.request.user)

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

class LogoutAnyMethodView(View):
    def get(self, request):
        return self._logout_and_redirect(request)

    def post(self, request):
        return self._logout_and_redirect(request)

    def _logout_and_redirect(self, request):
        next_url = request.GET.get('next') or request.POST.get('next') or '/'
        if not url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={*settings.ALLOWED_HOSTS, 'localhost', '127.0.0.1'}
        ):
            next_url = '/'
        logout(request)
        return redirect(next_url)
