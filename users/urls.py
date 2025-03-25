from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    RegisterView,
    ProfileView,
    CustomLoginView,
    CustomLogoutView,
    HomeView,
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("register/", RegisterView.as_view(), name="user-register"),
    path("login/", CustomLoginView.as_view(), name="user-login"),
    path('logout/', CustomLogoutView.as_view(), name='user-logout'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # Project URLs
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path(
        'projects/<int:pk>/', ProjectDetailView.as_view(),
        name='project_detail'),
    path('projects/new/', ProjectCreateView.as_view(), name='create_project'),

    # Task URLs
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/new/', TaskCreateView.as_view(), name='create_task'),
    path('task/<int:pk>/edit/', TaskUpdateView.as_view(), name='edit_task'),
]

# Serving media files in debug mode
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
