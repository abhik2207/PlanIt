from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Task, Contact
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.urls import reverse

# Create your views here.
def homepage(request):
    allTasks = Task.objects.all()
    completedTasks = Task.objects.filter(user=request.user.id, taskCompleted=False)
    return render(request, 'todolist/homepage.html', {'completedTasks':completedTasks})

def about(request):
    return render(request, 'todolist/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        contact = Contact(name=name, email=email, phone=phone, content=content)
        contact.save()
    return render(request, 'todolist/contact.html')

def addTask(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        status = False
        user = request.user
        if 'completed' in request.POST:
            checkbox_value = request.POST.get('completed')
            if checkbox_value == 'on':
                status = True
        task = Task(taskTitle=title, taskDescription=description, taskCompleted=status, user=user)
        task.save()
        return redirect('/allTasks')
    return render(request, 'todolist/addTask.html')

def allTasks(request):
    allTasks = Task.objects.filter(user=request.user)
    return render(request, 'todolist/allTasks.html', {'allTasks': allTasks})

def editTask(request, id):
    task = get_object_or_404(Task, taskID=id)
    # task = Task.objects.get(taskID=id)
    return render(request, 'todolist/editTask.html', {'task':task})

def save_task(request, id):
    if request.method == 'POST':
        task = get_object_or_404(Task, taskID=id)
        # task = Task.objects.get(task_id=id)
        task.taskTitle = request.POST['tit']
        task.taskDescription = request.POST['desc']
        task.taskCompleted = request.POST['status']
        task.save()
        return redirect('/allTasks')
    return render(request, 'todolist/editTask.html', {'task':task})

def search(request):
    query = request.GET['query']
    taskTitle = Task.objects.filter(taskTitle__icontains = query)
    taskDescription = Task.objects.filter(taskDescription__icontains = query)
    searchResults = taskTitle.union(taskDescription)
    return render(request, 'todolist/search.html', {'searchResults':searchResults})

def delete(request, id):
    if request.method == 'POST':
        task = get_object_or_404(Task, taskID=id)
        task.delete()
        return redirect('/allTasks')
    return render(request, 'todolist/editTask.html', {'task':task})

def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['signupUsername']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # Checks
        if len(username)<3 or len(username)>20:
            return redirect('homepage')
        if not username.isalnum():
            return redirect('homepage')
        if pass1 != pass2:
            return redirect('homepage')
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        return redirect('homepage')
    else:
        return HttpResponse('404 - Not Found')


def handleLogin(request):
    if request.method == 'POST':
        loginUsername = request.POST['loginUsername']
        loginPassword = request.POST['loginPassword']
        user = authenticate(username=loginUsername, password=loginPassword)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            return redirect('homepage')
    else:
        return HttpResponse('404 - Not Found')


def handleLogout(request):
    logout(request)
    return redirect('homepage')