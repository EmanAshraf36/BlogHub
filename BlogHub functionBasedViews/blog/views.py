from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.urls import reverse, reverse_lazy
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post, Category
from .forms import PostForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.
#Function-basd view

def post_list(request):
    posts_queryset = Post.objects.filter(
        status=Post.Status.PUBLISHED
    ).select_related('author','category').prefetch_related('tags')

    paginator = Paginator(posts_queryset, 10)
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)

    featured_posts = Post.objects.filter(
        status = Post.Status.PUBLISHED,
        is_featured = True
    )[:3]

    context = {
        'posts': posts,
        'featured_posts':featured_posts,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.select_related('author','category').prefetch_related('tags'),
        slug=slug, #from db = from param
        status = Post.Status.PUBLISHED
    )

    post.views_count += 1
    post.save(update_fields=['views_count'])

    related_posts = Post.objects.filter(
        category= post.category,
        status = Post.Status.PUBLISHED
    ).exclude(id = post.id)[:3]

    comments = post.comments.filter(is_approved=True)
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
    }
    return render(request, 'blog/post_detail.html', context)

@login_required(login_url='/login')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid:
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'post created successfully!')
            return redirect('blog:post-detail', slug=post.slug)
        else:
            # Form has errors
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PostForm()
    
    context = {
        'form': form,
    }
    return render(request, 'blog/post_form.html', context)

#update
@login_required(login_url='/login/')
def post_update(request, slug):
    post_obj = get_object_or_404(Post, slug=slug)

    if request.user != post_obj.author:
        messages.error(request, "You are not allowed to update this post.")
        return redirect('blog:post-detail', slug=post_obj.slug)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post_obj)
        if form.is_valid():
            saved_post = form.save()
            messages.success(request, "Post updated successfully.")
            return redirect('blog:post-detail', slug=saved_post.slug)
        else:
            messages.error(request, "Please review the form and fix the issues.")
    else:
        form = PostForm(instance=post_obj)

    return render(request, 'blog/post_form.html', {
        'form': form,
        'post': post_obj
    })

#delete
@login_required(login_url='/login/')
def post_delete(request, slug):
    post_obj = get_object_or_404(Post, slug=slug)

    if request.user.id != post_obj.author_id:
        messages.error(request, "You cannot delete a post you don't own.")
        return redirect('blog:post-detail', slug=post_obj.slug)

    if request.method == "POST":
        post_obj.delete()
        messages.success(request, "The post has been removed.")
        return redirect('blog:post-list')

    return render(request, 'blog/post_confirm_delete.html', {
        'post': post_obj
    })


# DB-based implementations for home, posts, category_posts, search_results, author_posts
def home(request):
    published_posts = (
        Post.objects.filter(status=Post.Status.PUBLISHED)
        .select_related("author", "category")
        .prefetch_related("tags")
    )

    featured_posts = published_posts.filter(is_featured=True)[:4]

    categories = Category.objects.all().order_by("name")

    context = {
        'site_name': 'BlogHub',
        'tagline': 'Your Platform for Sharing Ideas',
        'total_posts': published_posts.count(),
        'categories_count': Category.objects.count(),
        'total_authors': published_posts.values("author").distinct().count(),
        'current_year': datetime.now().year,
        'featured_topics': ['Technology','Design','Travel','Education','Lifestyle'],
        'features': [
            {'icon': '✍️', 'title': 'Easy Publishing', 'description': 'Write and publish posts effortlessly'},
            {'icon': '🎨', 'title': 'Beautiful Design', 'description': 'Professional templates for your content'},
            {'icon': '👥', 'title': 'Engage Readers', 'description': 'Build your audience and community'},
            {'icon': '📈', 'title': 'Analytics', 'description': 'Track your post performance'},
        ],
        'is_featured_active': featured_posts.exists(),
        'spotlight_topic': 'Web Development',
        'featured_posts': featured_posts,
        'categories': categories,
    }
    return render(request, 'blog/home.html', context)


def posts(request):
    posts_qs = (
        Post.objects.filter(status=Post.Status.PUBLISHED)
        .select_related("author","category")
        .order_by("-published_at","-created_at")
    )

    context = {
        "page_title": "All Blog Posts",
        "posts": posts_qs,
        "total_posts": posts_qs.count(),
    }
    return render(request, "blog/posts.html", context)


def category_posts(request, category_name):
    normalized = category_name.lower()
    if category_name != normalized:
        return redirect('blog:category_posts', category_name=normalized)

    category = get_object_or_404(
        Category, #q is for 'or'
        Q(slug__iexact=normalized) | Q(name__iexact=normalized)
    )

    posts_qs = (
        Post.objects.filter(status=Post.Status.PUBLISHED, category=category)
        .select_related("author","category")
        .order_by("-published_at","-created_at")
    )

    context = {
        "category_name": category.name,
        "posts": posts_qs,
        "total_posts": posts_qs.count(),
    }
    return render(request, "blog/category_posts.html", context)


def search_results(request):
    query = (request.GET.get("q") or "").strip()
    category_param = (request.GET.get("category") or "").strip()

    posts_qs = (
        Post.objects.filter(status=Post.Status.PUBLISHED)
        .select_related("author","category")
        .prefetch_related("tags")
    )

    if query:
        posts_qs = posts_qs.filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query)
        )

    if category_param:
        posts_qs = posts_qs.filter(
            Q(category__slug__iexact=category_param) |
            Q(category__name__iexact=category_param)
        )

    categories = Category.objects.values_list("name", flat=True).order_by("name").distinct()

    context = {
        "query": query,
        "posts": posts_qs,
        "total_results": posts_qs.count(),
        "categories": categories,
        "selected_category": category_param,
    }
    return render(request, "blog/search_results.html", context)


def author_posts(request, author_name):
    normalized = author_name.lower()
    if author_name != normalized:
        return redirect('blog:author_posts', author_name=normalized)

    user = get_object_or_404(User, username__iexact=normalized)

    posts_qs = (
        Post.objects.filter(status=Post.Status.PUBLISHED, author=user)
        .select_related("author","category")
        .order_by("-published_at","-created_at")
    )

    context = {
        "author_name": user.username,
        "posts": posts_qs,
        "total_posts": posts_qs.count(),
    }
    return render(request, "blog/author_posts.html", context)

def about(request):
    context = {
        'company_name': 'BlogHub Team',
        'founded_year': 2025,
        'mission': 'Empowering writers to share their stories with the world',
        'team_size': 15,
        'values': ['Creativity', 'Community', 'Quality Content', 'Freedom of Expression'],
        'current_year': datetime.now().year,
    }
    return render(request, 'blog/about.html', context)

def contact(request):
    context = {
        'current_year': datetime.now().year,
        'email':'contact@bloghub.com',
        'phone':'+1-800-BLOGHUB',
        'address':'456 Writers Lane, Content City, CC 54321',
        'business-hours': 'Monday - Friday: 9AM - 6PM',
        'departments' : [{"name": "Support", "email": "support@bloghub.com"},
                        {"name": "Marketing", "email": "marketing@bloghub.com"},
                        {"name": "Editorial", "email": "editorial@bloghub.com"},
                        {"name": "Technical", "email": "tech@bloghub.com"}],

        'social_media' : [{"platform": "Facebook", "link": "https://facebook.com/bloghub"},
                        {"platform": "Twitter", "link": "https://twitter.com/bloghub"},
                        {"platform": "Instagram", "link": "https://instagram.com/bloghub"},
                        {"platform": "LinkedIn", "link": "https://linkedin.com/company/bloghub"}]
    }

    return render(request, 'blog/contact.html', context)

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = template_name = 'registration/signup.html'
    success_url = reverse_lazy('blog:post-list')
    
    def form_valid(self, form):
        # Save the user
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, f'Welcome {self.object.username}! Your account has been created.')
        return response
    
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True 
    
    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('blog:post-list'))
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)
    

from django.contrib import messages

class CustomLogoutView(LogoutView):
    next_page = 'blog:post-list'  # Redirect after logout
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, f'Goodbye, {request.user.username}! You have been logged out.')
        return super().dispatch(request, *args, **kwargs)