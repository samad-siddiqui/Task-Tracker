from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.views.generic import (
    View, TemplateView, ListView, DetailView, CreateView, UpdateView
)
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import (
    UserRegisterForm, LoginForm, UserProfileForm,
    UserUpdateForm, ProjectForm, TaskForm, CommentForm
)
from .models import Project, Task


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registration successful.")
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')
    redirect_authenticated_user = True

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    template_name = 'logout.html'
    next_page = reverse_lazy('user-login')


class ProfileView(LoginRequiredMixin, View):
    template_name = 'profile.html'

    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=request.user.profile)
        return render(
            request, self.template_name, {'u_form': u_form, 'p_form': p_form})

    def post(self, request):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')

        return render(
            request, self.template_name, {'u_form': u_form, 'p_form': p_form})


class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name, {'title': 'Home'})


# --- Projects ---
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project_list.html'
    context_object_name = 'projects'


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.object.tasks.all()
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'create_project.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        messages.success(self.request, "Project created successfully!")
        return super().form_valid(form)


# --- Tasks ---
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added successfully!")
            return redirect('task_detail', pk=task.pk)

        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'create_task.html'
    form_class = TaskForm
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        messages.success(self.request, "Task created successfully!")
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'edit_task.html'
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Task updated successfully!")
        return super().form_valid(form)
