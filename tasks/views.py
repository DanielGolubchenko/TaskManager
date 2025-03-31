from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, TaskForm, TagForm
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required 
from .models import Task, Tag
from django.contrib import messages

def welcome(request):
    """Not implemented yet"""
    return render(request, 'welcome.html')

@login_required
def home(request):
    tags = Tag.objects.all()
    tag_name = request.GET.get('tag')

    if tag_name:  
        tasks = Task.objects.filter(tags__name=tag_name)
    else:
        tasks = Task.objects.all()

    return render(request, 'home.html', {'tags': tags, 'tasks': tasks})

@login_required
def tasks(request):
    # Filter by status
    tasks_completed = Task.objects.filter(user=request.user, status='Completed')
    tasks_canceled = Task.objects.filter(user=request.user, status='Canceled')
    tasks_in_progress = Task.objects.filter(user=request.user, status='In progress')
    tasks_pending = Task.objects.filter(user=request.user, status='Pending')

    return render(request, 'tasks.html', {
        'tasks_completed': tasks_completed,
        'tasks_canceled': tasks_canceled,
        'tasks_in_progress': tasks_in_progress,
        'tasks_pending': tasks_pending
    })

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

def register(request):
    '''This view function is used to register a new user'''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log in the user after registration
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})

def login_view(request):
    '''This view function is used to log in an existing user'''
    if request.method == 'POST':
        # Create an instance of the AuthenticationForm class with the data from the request
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']  # Use cleaned_data to access form fields
            password = form.cleaned_data['password']
            # Authenticate the user using the username and password
            user = authenticate(request, username=username, password=password)

            # If the user is authenticated, log them in
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                # If authentication fails, add a custom error message
                messages.error(request, 'Invalid username or password.')

        else:
            # If the form is invalid, check if the errors are for username or password
            messages.error(request, 'Invalid username or password.')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@login_required  # require the user to be logged in to access this view
def task_create(request):
    tags = Tag.objects.all()  # Retrieve all tags

    if request.method == "POST":
        task_form = TaskForm(request.POST)
        tag_form = TagForm(request.POST)

        # Check which button was clicked
        if "add_tag" in request.POST:
            if tag_form.is_valid():
                tag_form.save()
            return render(request, "task_form.html", {"task_form": task_form, "tag_form": tag_form, "tags": tags})

        elif "edit_tag" in request.POST:
            tag_id = request.POST.get("tag_id")
            tag = get_object_or_404(Tag, id=tag_id)
            tag.name = request.POST.get("new_name")
            tag.save()
            return render(request, "task_form.html", {"task_form": task_form, "tag_form": tag_form, "tags": tags})

        elif "delete_tag" in request.POST:
            tag_id = request.POST.get("tag_id")
            tag = get_object_or_404(Tag, id=tag_id)
            tag.delete()
            return render(request, "task_form.html", {"task_form": task_form, "tag_form": tag_form, "tags": tags})

        else:  # New task form submitted
            if task_form.is_valid():
                task = task_form.save(commit=False)  # Don't save to the DB yet
                task.user = request.user  # Assign the current user to the task
                task.save()  # Save the task to the DB
                
                task_form.save_m2m()  # Save many-to-many relationships (tags)
                
                return redirect("tasks")

    else:
        task_form = TaskForm()
        tag_form = TagForm()

    return render(request, "task_form.html", {"task_form": task_form, "tag_form": tag_form, "tags": tags})



def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    tags = Tag.objects.all()
    tag_form = TagForm()

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = TaskForm(instance=task)

    return render(request, 'task_form.html', {
        'task_form': form,
        'tag_form': tag_form,
        'tags': tags  # pass the tags to the template
    })

def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('tasks')