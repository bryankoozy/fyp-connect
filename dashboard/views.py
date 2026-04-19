# dashboard/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FYPPost
from .forms import FYPPostForm


def home_redirect(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if request.user.role == 'admin':
        return redirect('dashboard:admin_home')
    return redirect('dashboard:student_home')


@login_required
def admin_home(request):
    if request.user.role != 'admin':
        return redirect('dashboard:student_home')
    return render(request, 'dashboard/admin_home.html')


@login_required
def student_home(request):
    if request.user.role != 'student':
        return redirect('dashboard:admin_home')
    posts = FYPPost.objects.filter(status='open').exclude(author=request.user)
    my_posts = FYPPost.objects.filter(author=request.user)
    return render(request, 'dashboard/student_home.html', {
        'posts': posts,
        'my_posts': my_posts,
    })


@login_required
def create_post(request):
    if request.user.role != 'student':
        return redirect('dashboard:admin_home')
    if request.method == 'POST':
        form = FYPPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('dashboard:student_home')
    else:
        form = FYPPostForm()
    return render(request, 'dashboard/create_post.html', {'form': form})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(FYPPost, pk=pk, author=request.user)
    post.delete()
    messages.success(request, 'Post deleted.')
    return redirect('dashboard:student_home')