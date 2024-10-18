# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from .models import Blog
from .forms import BlogForm
from taggit.models import Tag
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    blogs = Blog.objects.all().order_by('-created_at')
    tag = request.GET.get('tag')
    if tag:
        blogs = blogs.filter(tags__name__icontains=tag)
    return render(request, 'blog/home.html', {'blogs': blogs})

def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            form.save_m2m()  # For tags
            return redirect('home')
    else:
        form = BlogForm()
    return render(request, 'blog/create_blog.html', {'form': form})

@login_required
def update_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    tag_list = list(blog.tags.values_list('name', flat=True))
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BlogForm(instance=blog)
        form.initial['tags'] = ', '.join(tag_list)
    return render(request, 'blog/update_blog.html', {'form': form, 'blog': blog})

@login_required
def delete_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        blog.delete()
        return redirect('home')
    return render(request, 'blog/delete_blog.html', {'blog': blog})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            # Send welcome email
            subject = 'Welcome to Our Mblog!'
            message = f'Hi {user.username},\n\nThank you for signing up on our blog platform. We hope you enjoy your stay!\n\nBest regards,\nThe Team'
            recipient_list = [user.email]
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'blog/login.html', {'form': form})
