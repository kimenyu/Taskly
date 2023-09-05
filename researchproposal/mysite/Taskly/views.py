from django.shortcuts import render, redirect
from .models import User, Task
from django.contrib.auth import get_user_model, login, authenticate, logout
from .forms import UserRegistrationForm, PositionForm, UserLoginForm, UserUpdateForm, SetPasswordForm, PasswordResetForm, TaskForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .decorators import user_not_authenticated
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import Task  # Import your Task model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .models import Task  # Import your Task model
from .forms import TaskForm  # Import your TaskForm if you have one
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .models import Task
from .forms import TaskForm
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST


# Create your views here.
def homeView(request):
    return render(request, 'Taskly/home.html')

@require_POST
def mark_as_completed(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = True
    task.save()
    return redirect('Taskly:homepage')

from django.contrib import messages

class taskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'Taskly/task_form.html'
    success_url = reverse_lazy('Taskly:homepage')

    def form_valid(self, form):
        # Check if a task with the same title already exists for the current user
        existing_task = Task.objects.filter(user=self.request.user, title=form.cleaned_data['title']).first()
        
        if existing_task:
            messages.error(self.request, 'Task with this title already exists.')
            return self.form_invalid(form)  # Display an error message
        else:
            form.instance.user = self.request.user
            return super().form_valid(form)  # Proceed with task creation
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error_message'] = messages.get_messages(self.request)
        return context

class taskListView(LoginRequiredMixin, ListView):
    model = Task

    def get_queryset(self):
        # Filter tasks to show only the ones belonging to the logged-in user
        return Task.objects.filter(user=self.request.user)

class taskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'Taskly/task_update_form.html'
    success_url = reverse_lazy('Taskly:homepage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    
class taskDetailView(LoginRequiredMixin, DetailView):
    model = Task

    def get_queryset(self):
        # Filter tasks to show only the ones belonging to the logged-in user
        return Task.objects.filter(user=self.request.user)

class taskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'Taskly/task_confirm_delete.html'
    success_url = reverse_lazy('Taskly:homepage')

    def get_queryset(self):
        # Filter tasks to show only the ones belonging to the logged-in user
        return Task.objects.filter(user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.mark_as_completed()  # Mark the task as completed before deleting it
        return super().post(request, *args, **kwargs)

@login_required(login_url='Taskly:login')
def search_view(request):
    query = request.GET.get('q')
    if query:
        results = Task.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        results = []
    return render(request, 'Taskly/search.html', {'results': results, 'query': query})

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('Taskly:login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('Taskly:login')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("Taskly/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

@user_not_authenticated
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('Taskly:homepage')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = UserRegistrationForm()

    return render(
        request=request,
        template_name="Taskly/register.html",
        context={"form": form}
    )
    
@user_not_authenticated
def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                return redirect("Taskly:homepage")

        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test")
                    continue
                
                messages.error(request, error) 
 

    form = UserLoginForm()

    return render(
        request=request,
        template_name="Taskly/login.html",
        context={"form": form}
        )

def profile(request, username):
    if request.method == "POST":
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()
            messages.success(request, f'{user_form.username}, Your profile has been updated!')
            return redirect("Taskly:profile", user_form.username)

        for error in list(form.errors.values()):
            messages.error(request, error)

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        #form.fields['description'].widget.attrs = {'rows': 1}
        return render(
            request=request,
            template_name="Taskly/profile.html",
            context={"form": form}
            )
    
    return redirect("Taskly:homepage")

@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('Taskly:login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'Taskly/password_reset_confirm.html', {'form': form})

@user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("Taskly/template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        <h2>Password reset sent</h2><hr>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        </p>
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('Taskly:homepage')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="Taskly/password_reset.html", 
        context={"form": form}
        )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('Taskly:login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'Taskly/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("Taskly:homepage")


@login_required(login_url='login')
def userhome(request):
    return render(request, 'Taskly/home.html')

@login_required
def logoutUser(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("Taskly:login")