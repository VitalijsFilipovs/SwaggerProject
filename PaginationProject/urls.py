from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.contrib.auth import views as auth_views
from GlobalPagination.forms import EmailAuthenticationForm
from GlobalPagination.views import home, LogoutAnyMethodView, SignUpView

schema_view = get_schema_view(
    openapi.Info(
        title="Task Manager API",
        default_version='v1',
        description="Документация к API для управления задачами",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Аутентификация
    path("accounts/login/", auth_views.LoginView.as_view(
        authentication_form=EmailAuthenticationForm
    ), name="login"),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path("accounts/logout/", LogoutAnyMethodView.as_view(), name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),  # password reset и т.д.

    # Главная и админка
    path('', home, name='home'),
    path('admin/', admin.site.urls),

    # API
    path('api/global/', include('GlobalPagination.urls')),  # это из GlobalPagination
    path('api/listings/', include('listings.urls')),        # это — объявления
    path('api/bookings/', include('bookings.urls')),
    path('api/reviews/', include('reviews.urls')),

    # Документация
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
