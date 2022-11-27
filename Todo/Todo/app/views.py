from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate , login as loginUser , logout
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
# Create your views here.
from app.forms import TODOForm
from app.models import TODO
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user = user).order_by('priority')
        # app/templates/app/index.html
        #return render(request, 'index.html')
        #return render(request, 'app/index.html', context={'form' : form , 'todos' : todos})
        return render(request, 'app/index.html', {'form' : form , 'todos' : todos})
        #return HttpResponse('HOME PAGE')

def login(request):
    if request.method == 'GET':
        form1 = AuthenticationForm()
        context = {
            "form" : form1
        }
        # app/templates/app/login.html
        return render(request, 'app/login.html', context )
        #return HttpResponse("Hello, Django!")
    else:
        form = AuthenticationForm(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username , password = password)
            if user is not None:
                loginUser(request , user)
                return redirect(reverse('home'))
        else:
            context = {
                "form" : form
            }
            return render(request , 'app/login.html' , {
                'form' : form
            } )


def signup(request):

    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            "form" : form
        }
        return render(request , 'app/signup.html' , context)
    else:
        print(request.POST)
        form = UserCreationForm(request.POST)  
        context = {
            "form" : form
        }
        if form.is_valid():
            user = form.save()
            print(user)
            if user is not None:
                return redirect('login')
        else:
            return render(request , 'app/signup.html' , context)



@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        form = TODOForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            print(todo)
            return redirect("home")
        else: 
            return render(request , 'app/index.html' , {'form' : form})


def delete_todo(request , id ):
    print(id)
    TODO.objects.get(pk = id).delete()
    return redirect('home')

def change_todo(request , id  , status):
    todo = TODO.objects.get(pk = id)
    todo.status = status
    todo.save()
    return redirect('home')


def signout(request):
    logout(request)
    return redirect('login')