from django.urls import path, reverse_lazy, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name ='Taskly'


urlpatterns = [
    path('', views.homepage, name='homepage'),
      # Added trailing slash for consistency
    path('register/', views.register, name='register'),  # Added trailing slash for consistency
    path('login/', views.login_view, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),  # Added trailing slash for consistency
    path(r'profile/<str:username>/', views.profile, name='profile'),
    path("password_change", views.password_change, name="password_change"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
    path('search/', views.search_view, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)