from django.urls import path, reverse_lazy, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import taskListView, taskCreateView, taskUpdateView, taskDetailView

app_name ='Taskly'

urlpatterns = [
    path('', views.homeView, name='home'),
    path('home', views.taskListView.as_view(), name='homepage'),
    path('register/', views.register, name='register'),  # Added trailing slash for consistency
    path('login/', views.login_view, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),  # Added trailing slash for consistency
    path('profile/<username>/', views.profile, name='profile'),
    path("password_change", views.password_change, name="password_change"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
    path('search/', views.search_view, name='search'),
    path('task/create/', taskCreateView.as_view(), name='task-create'),
    path('task/<slug:slug>/update/', taskUpdateView.as_view(), name='task-update'),
    path('task/<slug:slug>/', taskDetailView.as_view(), name='task-detail'),
    path('task/<slug:slug>/delete/', views.taskDeleteView.as_view(), name='task-delete'),
    path('mark-as-completed/<int:pk>/', views.mark_as_completed, name='mark-as-completed'),
    
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)