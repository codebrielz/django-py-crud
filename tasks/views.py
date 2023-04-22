from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required #es un decorador para indicar que el controlador esta protegido
# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    
    if request.method == 'GET':
        # render se utiliza para renderizar una pagina estatica html y el objeto que se ve es para enviarle información a esa pagina.
        return render(request, 'signup.html', {
        'form': UserCreationForm #<-- se utiliza para crear un formulario que ya viene creado de django
    })
    else:
        # Verificamos si la contraseña es correcta
        if request.POST['password1'] == request.POST['password2']:
           try:
            #    Intentamos registrar el usuario en la base de datos
                user = User.objects.create_user(username = request.POST['username'], password = request.POST['password1'])
                user.save()
                # Este login crea la cookie del usuario por nosotros.
                login(request, user)
                return redirect('tasks')
            #    si no puede, quiere decir que el usuario existe
           except IntegrityError:
               return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Username already exists'
            })
        # En el caso que no sea correcta la contraseña, enviamos el error al template.
        return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Password dont match'
            })

# para acceder debe estar registrado
@login_required
def tasks (request):
    #así recibo las tareas que sean solamente del usuario actual que este logeado
    #Podemos añadir otro filtro más si quereos, como por ejemplo el datecompleted(propiedad creada en el models.py) que tiene una
    # propiedad por defecto que es __isnull que si está vacío que me devuelva las tareas que esten de datecompleted vacío
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True) 
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed (request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') #Ahora recibo las tareas completadas y las ordeno por fecha 
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def taskDetail(request, task_id):
    if request.method == 'GET':
        # pk = primaryKey
        task = get_object_or_404(Task, pk = task_id, user=request.user) #1ero Model, 2ndo Primarykey, 3ero afirma si el usuario que esta haciendo la peticion de sus recursos sea el mismo usuario.
        # Llamamos el TaskForm para que llene los campos al editar
        form = TaskForm(instance=task) #Le pasamos la instancia de la tarea para que llene el formulario con los datos de la tarea
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user) #Obtengo la tarea actualizada para mostrar los datos frescos
            form = TaskForm(request.POST, instance = task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task':task, 'form':form, 'error': 'Error actualizando updating task'})
            
@login_required
def completeTask(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def deleteTask(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


@login_required
def createTask(request):
    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'form': TaskForm
        })
    else:
       try:
            form = TaskForm(request.POST) #Creamos los campos del formulario a partir de los campos enviados
            new_task = form.save(commit=False) #Si utilizamos el save() sin commit False, creara como una instancia dentro de la base de datos y lo guardara,
            # eso no lo quiero, por eso pongo commit=False, solo quiero que me devuelva los datos de dentro del form
            new_task.user = request.user #<-- Como la cookie contiene el sessionid pues puedo recuperar de la request el user
            new_task.save() #Esto generara el dato dentro de la base de datos
            return redirect("tasks")
       except ValueError:
            return render(request,"create_task.html", {
                'form': TaskForm,
                'error':'Please provide validate data'
            })
        
@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        # authenticate comprueba si el usuario y la contraseña coincide con la de la base de datos
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # Si el usuario esta vacío...
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'Username or password is incorrect'
            })
        # Si no...
        else:
            login(request, user)
            return redirect('tasks')
        
        