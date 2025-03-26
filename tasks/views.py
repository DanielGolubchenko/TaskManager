from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, TaskForm, TagForm
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from .models import Task, Tag

def welcome(request):
    return render(request, 'welcome.html')

@login_required
def home(request):
    # If the user is in demo mode, we will check if the session has expired
    if request.session.get("is_demo", False):
        # If the session has expired, clear the session and redirect the user to the welcome page
        if not request.session.exists(request.session.session_key):
            request.session.flush()
            return redirect("welcome")
        
        # If the session is still active, render the demo home page
        return render(request, "demo_home.html", {"username": request.session["username"]})
    return render(request, 'home.html') # If the user is not in demo mode, render the home page

@login_required
def tasks(request):
    if request.session.get("is_demo", False):
        if not request.session.exists(request.session.session_key):
            request.session.flush()
            return redirect("welcome")
        return render(request, "demo_tasks.html", {"username": request.session["username"]})
    
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def profile(request):
    if request.session.get("is_demo", False):
        if not request.session.exists(request.session.session_key):
            request.session.flush()
            return redirect("welcome")
        return render(request, "demo_profile.html", {"username": request.session["username"]})
    
    return render(request, 'profile.html')

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

def login_view(request):
    '''This view function is used to log in an existing user'''
    if request.method == 'POST':
        # Create an instance of the AuthenticationForm class with the data from the request
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Authenticate the user using the username and password
            user = authenticate(request, username=username, password=password)

            # If the user is authenticated, log them in
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def demo_login(request):
    '''This view function is used to log in a demo user'''
    if "user_id" not in request.session:
        request.session["user_id"] = get_random_string(10) # Generate a random user ID for the demo user
        request.session["username"] = f"DemoUser-{request.session['user_id']}" # Generate a username for the demo user
        request.session["is_demo"] = True # Set the is_demo key in the session to True

    # Set the expiry time for the session to 5 minutes
    expiry_time = timezone.now() + timedelta(seconds=300)
    request.session['expiry_time'] = expiry_time.isoformat() # Store the expiry time in the session

    # Calculate the time remaining for the session to expire
    time_remaining_seconds = int((expiry_time - timezone.now()).total_seconds()) 
    request.session['time_remaining_seconds'] = time_remaining_seconds # Store the time remaining in the session

    request.session.set_expiry(300)

    return redirect("home")

def demo_logout(request):
    '''This view function is used to log out a demo user'''
    if "is_demo" in request.session:
        del request.session["is_demo"]
        del request.session["user_id"]
        del request.session["username"]
    return redirect("welcome")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Tag
from .forms import TaskForm, TagForm

@login_required  # Asegura que solo usuarios autenticados pueden crear tareas
def task_create(request):
    tags = Tag.objects.all()  # Obtener todos los tags disponibles

    if request.method == "POST":
        task_form = TaskForm(request.POST)
        tag_form = TagForm(request.POST)

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

        else:  # Creación de una nueva tarea
            if task_form.is_valid():
                task = task_form.save(commit=False)  # No guardamos aún en la BD
                task.user = request.user  # Asignamos el usuario actual
                task.save()  # Ahora sí guardamos en la BD
                return redirect("tasks")

    else:
        task_form = TaskForm()
        tag_form = TagForm()

    return render(request, "task_form.html", {"task_form": task_form, "tag_form": tag_form, "tags": tags})


def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    tags = Tag.objects.all()  # Obtener todos los tags
    tag_form = TagForm()  # Formulario para añadir tags

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
        'tags': tags  # Pasar los tags al template
    })

def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('tasks')

