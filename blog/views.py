from django.shortcuts import render
from .models import Blog
from .forms import BlogForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect

# List all blogs
def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blog/blog_list.html', {'blogs': blogs})

# Create a new blog
@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('blog_list')
    else:
        form = BlogForm()
    return render(request, 'blog/blog_form.html', {'form': form})  # Corrected path

# Edit a blog
@login_required
def blog_edit(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('blog_list')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog/blog_form.html', {'form': form})  # Corrected path

# Delete a blog
@login_required
def blog_delete(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog/blog_confirm_delete.html', {'blog': blog})  # Corrected path

# User registration
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm  # Make sure to import your form

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Proper password hashing
            user.save()
            login(request, user)  # Automatically logs in the user
            return redirect('blog_list')  # Redirect to blog list after successful registration
    else:
        form = UserRegistrationForm()  # Instantiate the empty form on GET request
    
    # Return the registration form template
    return render(request, 'registration/register.html', {'form': form})
