from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import PostForm

from .models import Post

# Create your views here.
def home(request):
    User = request.user
    Posts = Post.objects.all().order_by('-created_at')

    context = {
        'user': User,
        'posts': Posts,
        'total_posts': Posts.count(),
    }

    return render(request, 'home.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado')
            return render(request, 'auth.html', {'page': page})

        user = authenticate(request, username=username, password=password)   

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos')


    context = {'page': page}

    return render(request, 'auth.html', context)


def signup(request):
    page = 'signup'
    form = UserCreationForm()

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during signup')

    context = {'page': page, 'form': form}

    return render(request, 'auth.html', context)



def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post criado com sucesso!')
            return redirect('home') 
    else:
        form = PostForm()

    type = 'create'

    context = {'form': form, 'type': type}

    return render(request, 'create_post.html', context)


def update_post(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post atualizado com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Erro ao atualizar o post')

   
    type = 'update'
    context = {'form': form, 'type': type}

    return render(request, 'create_post.html', context)
    

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})