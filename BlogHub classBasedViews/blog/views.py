from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
from datetime import datetime

# Create your views here.
#Function-basd view
#cbv: class based view
def home(request): #user request -> user data, url parameter 
    posts_list = [
        {
            'id': 1,  # ⭐ Make sure all posts have IDs!
            'title': 'Getting Started with Django',
            'author': 'Sarah Johnson',
            'category': 'Technology',
            'excerpt': 'Learn the fundamentals of Django development',
            'date': '2025-01-15',
            'published': True,
            'reading_time': '8 min'
        },
        {
            'id': 2,
            'title': 'Mastering CSS Grid Layout',
            'author': 'Mike Chen',
            'category': 'Design',
            'excerpt': 'CSS Grid revolutionized responsive design',
            'date': '2025-01-20',
            'published': True,
            'reading_time': '6 min'
        },
        {
            'id': 3,
            'title': 'Traveling Through Southeast Asia',
            'author': 'Emma Rodriguez',
            'category': 'Travel',
            'excerpt': 'Discover hidden gems of Southeast Asia',
            'date': '2025-01-25',
            'published': True,
            'reading_time': '10 min'
        },
        {
            'id': 4,
            'title': 'Understanding Machine Learning Basics',
            'author': 'Dr. James Wilson',
            'category': 'Education',
            'excerpt': 'Machine learning concepts demystified',
            'date': '2025-01-28',
            'published': False,
            'reading_time': '12 min'
        },
        {
            'id': 5,
            'title': 'Top 10 Photography Tips',
            'author': 'Lisa Anderson',
            'category': 'Photography',
            'excerpt': 'Transform your photography skills',
            'date': '2025-02-01',
            'published': True,
            'reading_time': '7 min'
        },
        {
            'id': 6,
            'title': 'Building REST APIs with Django',
            'author': 'Carlos Martinez',
            'category': 'Technology',
            'excerpt': 'Create powerful REST APIs using Django REST Framework',
            'date': '2025-02-05',
            'published': True,
            'reading_time': '15 min'
        },
        {
            'id': 7,
            'title': 'Minimalist Interior Design Trends',
            'author': 'Sophie Laurent',
            'category': 'Design',
            'excerpt': 'Less is more in modern interior design',
            'date': '2025-02-08',
            'published': False,
            'reading_time': '5 min'
        },
        {
            'id': 8,
            'title': 'Healthy Meal Prep for Busy Professionals',
            'author': 'Jennifer Lee',
            'category': 'Health',
            'excerpt': 'Save time and eat healthy with these meal prep tips',
            'date': '2025-02-10',
            'published': True,
            'reading_time': '9 min'
        },
    ]
    
    featured_posts = [p for p in posts_list if p['id'] >= 6][:4]
    context = {
        'site_name': 'BlogHub',
        'tagline': 'Your Platform for Sharing Ideas',
        'total_posts': 247,
        'categories_count': 23,
        'total_authors': 45,
        'current_year': datetime.now().year,
        'featured_topics': [
            'Technology',
            'Design',
            'Travel',
            'Education',
            'Lifestyle'
        ],
        'features': [
            {'icon': '✍️', 'title': 'Easy Publishing', 'description': 'Write and publish posts effortlessly'},
            {'icon': '🎨', 'title': 'Beautiful Design', 'description': 'Professional templates for your content'},
            {'icon': '👥', 'title': 'Engage Readers', 'description': 'Build your audience and community'},
            {'icon': '�', 'title': 'Analytics', 'description': 'Track your post performance'},
        ],
        'is_featured_active': True,
        'spotlight_topic': 'Web Development',
        'featured_posts': featured_posts
    }
    return render(request, 'blog/home.html', context)

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

def posts(request):
    """Posts page view - display all blog posts"""
    posts_list = [
        {
            'id': 1,  # ⭐ Make sure all posts have IDs!
            'title': 'Getting Started with Django',
            'author': 'Sarah Johnson',
            'category': 'Technology',
            'excerpt': 'Learn the fundamentals of Django development',
            'date': '2025-01-15',
            'published': True,
            'reading_time': '8 min'
        },
        {
            'id': 2,
            'title': 'Mastering CSS Grid Layout',
            'author': 'Mike Chen',
            'category': 'Design',
            'excerpt': 'CSS Grid revolutionized responsive design',
            'date': '2025-01-20',
            'published': True,
            'reading_time': '6 min'
        },
        {
            'id': 3,
            'title': 'Traveling Through Southeast Asia',
            'author': 'Emma Rodriguez',
            'category': 'Travel',
            'excerpt': 'Discover hidden gems of Southeast Asia',
            'date': '2025-01-25',
            'published': True,
            'reading_time': '10 min'
        },
        {
            'id': 4,
            'title': 'Understanding Machine Learning Basics',
            'author': 'Dr. James Wilson',
            'category': 'Education',
            'excerpt': 'Machine learning concepts demystified',
            'date': '2025-01-28',
            'published': False,
            'reading_time': '12 min'
        },
        {
            'id': 5,
            'title': 'Top 10 Photography Tips',
            'author': 'Lisa Anderson',
            'category': 'Photography',
            'excerpt': 'Transform your photography skills',
            'date': '2025-02-01',
            'published': True,
            'reading_time': '7 min'
        },
        {
            'id': 6,
            'title': 'Building REST APIs with Django',
            'author': 'Carlos Martinez',
            'category': 'Technology',
            'excerpt': 'Create powerful REST APIs using Django REST Framework',
            'date': '2025-02-05',
            'published': True,
            'reading_time': '15 min'
        },
        {
            'id': 7,
            'title': 'Minimalist Interior Design Trends',
            'author': 'Sophie Laurent',
            'category': 'Design',
            'excerpt': 'Less is more in modern interior design',
            'date': '2025-02-08',
            'published': False,
            'reading_time': '5 min'
        },
        {
            'id': 8,
            'title': 'Healthy Meal Prep for Busy Professionals',
            'author': 'Jennifer Lee',
            'category': 'Health',
            'excerpt': 'Save time and eat healthy with these meal prep tips',
            'date': '2025-02-10',
            'published': True,
            'reading_time': '9 min'
        },
    ]
    
    context = {
        'page_title': 'All Blog Posts',
        'posts': posts_list,
        'total_posts': len(posts_list),
    }
    return render(request, 'blog/posts.html', context)

def post_detail(request, post_id):
    all_posts = [{
            'id': 1,  # ⭐ Make sure all posts have IDs!
            'title': 'Getting Started with Django',
            'author': 'Sarah Johnson',
            'category': 'Technology',
            'excerpt': 'Learn the fundamentals of Django development',
            'date': '2025-01-15',
            'published': True,
            'reading_time': '8 min'
        },
        {
            'id': 2,
            'title': 'Mastering CSS Grid Layout',
            'author': 'Mike Chen',
            'category': 'Design',
            'excerpt': 'CSS Grid revolutionized responsive design',
            'date': '2025-01-20',
            'published': True,
            'reading_time': '6 min'
        },
        {
            'id': 3,
            'title': 'Traveling Through Southeast Asia',
            'author': 'Emma Rodriguez',
            'category': 'Travel',
            'excerpt': 'Discover hidden gems of Southeast Asia',
            'date': '2025-01-25',
            'published': True,
            'reading_time': '10 min'
        },
        {
            'id': 4,
            'title': 'Understanding Machine Learning Basics',
            'author': 'Dr. James Wilson',
            'category': 'Education',
            'excerpt': 'Machine learning concepts demystified',
            'date': '2025-01-28',
            'published': False,
            'reading_time': '12 min'
        },
        {
            'id': 5,
            'title': 'Top 10 Photography Tips',
            'author': 'Lisa Anderson',
            'category': 'Photography',
            'excerpt': 'Transform your photography skills',
            'date': '2025-02-01',
            'published': True,
            'reading_time': '7 min'
        },
        {
            'id': 6,
            'title': 'Building REST APIs with Django',
            'author': 'Carlos Martinez',
            'category': 'Technology',
            'excerpt': 'Create powerful REST APIs using Django REST Framework',
            'date': '2025-02-05',
            'published': True,
            'reading_time': '15 min'
        },
        {
            'id': 7,
            'title': 'Minimalist Interior Design Trends',
            'author': 'Sophie Laurent',
            'category': 'Design',
            'excerpt': 'Less is more in modern interior design',
            'date': '2025-02-08',
            'published': False,
            'reading_time': '5 min'
        },
        {
            'id': 8,
            'title': 'Healthy Meal Prep for Busy Professionals',
            'author': 'Jennifer Lee',
            'category': 'Health',
            'excerpt': 'Save time and eat healthy with these meal prep tips',
            'date': '2025-02-10',
            'published': True,
            'reading_time': '9 min'
        },
    ]
    
    # Find the post with matching ID
    post = next((p for p in all_posts if p['id'] == post_id), None)
    
    # If post not found, raise 404
    if post is None:
        raise Http404(f"Post {post_id} not found")
    
    # Post found! Show details
    context = {
        'post': post,
    }
    return render(request, 'blog/post_detail.html', context)    

def redirect_to_home(request):
    return redirect('blog:home')

def category_posts(request, category_name):
    all_posts = [
        {'id': 1, 'title': 'Getting Started with Django', 'author': 'Sarah Johnson', 'category': 'Technology',
         'excerpt': 'A comprehensive guide to Django', 'published': True},
        {'id': 2, 'title': 'CSS Grid Layout Guide', 'author': 'Mike Chen', 'category': 'Technology',
         'excerpt': 'Master CSS Grid', 'published': True},
        {'id': 3, 'title': 'Travel Tips for Europe', 'author': 'Emily Davis', 'category': 'Travel',
         'excerpt': 'Essential travel advice', 'published': True},
        {'id': 4, 'title': 'Healthy Breakfast Recipes', 'author': 'Jennifer Lee', 'category': 'Health',
         'excerpt': 'Start your day right', 'published': False},
        {'id': 5, 'title': 'JavaScript ES6 Features', 'author': 'David Wilson', 'category': 'Technology',
         'excerpt': 'Modern JavaScript features', 'published': True},
        {'id': 6, 'title': 'Photography Basics', 'author': 'Alex Brown', 'category': 'Art',
         'excerpt': 'Learn photography', 'published': True},
        {'id': 7, 'title': 'Meditation for Beginners', 'author': 'Lisa Martinez', 'category': 'Health',
         'excerpt': 'Find your inner peace', 'published': False},
        {'id': 8, 'title': 'Building REST APIs', 'author': 'Tom Anderson', 'category': 'Technology',
         'excerpt': 'API development guide', 'published': True},
    ]
    if category_name != category_name.lower():
        # Redirect to lowercase version
        return redirect(request,'blog:category_posts', category_name=category_name.lower())
    
    filtered_posts = [
        post for post in all_posts
        if post['category'].lower() == category_name
    ]
    
    # On Day 3 with database, this becomes:
    # filtered_posts = Post.objects.filter(category__iexact=category_name)
    
    context = {
        'category_name': category_name.title(),
        'posts': filtered_posts,
        'total_posts': len(filtered_posts),
    }
    return render(request, 'blog/category_posts.html', context)

def search_results(request):
    query = request.GET.get('q', '').strip()
    category = (request.GET.get('category') or '').strip()

    all_posts = [
        {'id': 1, 'title': 'Getting Started with Django', 'author': 'Sarah Johnson', 'category': 'Technology',
         'excerpt': 'A comprehensive guide to Django web framework', 'published': True},
        {'id': 2, 'title': 'CSS Grid Layout Guide', 'author': 'Mike Chen', 'category': 'Technology',
         'excerpt': 'Master modern CSS Grid layouts', 'published': True},
        {'id': 3, 'title': 'Travel Tips for Europe', 'author': 'Emily Davis', 'category': 'Travel',
         'excerpt': 'Essential European travel advice', 'published': True},
        {'id': 4, 'title': 'Healthy Breakfast Recipes', 'author': 'Jennifer Lee', 'category': 'Health',
         'excerpt': 'Start your day right with these recipes', 'published': False},
        {'id': 5, 'title': 'JavaScript ES6 Features', 'author': 'David Wilson', 'category': 'Technology',
         'excerpt': 'Modern JavaScript features explained', 'published': True},
        {'id': 6, 'title': 'Photography Basics', 'author': 'Alex Brown', 'category': 'Art',
         'excerpt': 'Learn the art of photography', 'published': True},
        {'id': 7, 'title': 'Meditation for Beginners', 'author': 'Lisa Martinez', 'category': 'Health',
         'excerpt': 'Find your inner peace through meditation', 'published': False},
        {'id': 8, 'title': 'Building REST APIs', 'author': 'Tom Anderson', 'category': 'Technology',
         'excerpt': 'Complete guide to API development', 'published': True},
    ]
    
    # Search posts if query exists
    if not query:
        # If no query, return all posts
        search_results = all_posts
    else:
        search_results = [
            post for post in all_posts
            if query.lower() in post['title'].lower() or
            query.lower() in post['excerpt'].lower()
        ]

    if category:
        search_results = [p for p in search_results if p['category'].lower() == category.lower()]

    categories = sorted({p['category'] for p in all_posts})
    
    context = {
        'query': query,
        'posts': search_results,
        'total_results': len(search_results),
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'blog/search_results.html', context)

def author_posts(request, author_name):
    all_posts = [
        {'id': 1, 'title': 'Getting Started with Django', 'author': 'Sarah Johnson', 'category': 'Technology',
         'excerpt': 'A comprehensive guide to Django web framework', 'published': True},
        {'id': 2, 'title': 'CSS Grid Layout Guide', 'author': 'Mike Chen', 'category': 'Technology',
         'excerpt': 'Master modern CSS Grid layouts', 'published': True},
        {'id': 3, 'title': 'Travel Tips for Europe', 'author': 'Emily Davis', 'category': 'Travel',
         'excerpt': 'Essential European travel advice', 'published': True},
        {'id': 4, 'title': 'Healthy Breakfast Recipes', 'author': 'Jennifer Lee', 'category': 'Health',
         'excerpt': 'Start your day right with these recipes', 'published': False},
        {'id': 5, 'title': 'JavaScript ES6 Features', 'author': 'David Wilson', 'category': 'Technology',
         'excerpt': 'Modern JavaScript features explained', 'published': True},
        {'id': 6, 'title': 'Photography Basics', 'author': 'Alex Brown', 'category': 'Art',
         'excerpt': 'Learn the art of photography', 'published': True},
        {'id': 7, 'title': 'Meditation for Beginners', 'author': 'Lisa Martinez', 'category': 'Health',
         'excerpt': 'Find your inner peace through meditation', 'published': False},
        {'id': 8, 'title': 'Building REST APIs', 'author': 'Tom Anderson', 'category': 'Technology',
         'excerpt': 'Complete guide to API development', 'published': True},
    ]
    if author_name != author_name.lower():
        # Redirect to lowercase version
        return redirect('blog:author_posts', author_name = author_name.lower())
    
    filtered_posts = [
        post for post in all_posts
        if post['author'].lower() == author_name
    ]
    context = {
        'author_name': author_name.title(),
        'posts': filtered_posts,
        'total_posts': len(filtered_posts),
    }
    return render(request, 'blog/author_posts.html', context)
