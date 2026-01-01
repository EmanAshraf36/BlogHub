from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('about/', views.about, name = 'about'),
    path('contact/', views.contact, name = 'contact'),
    path('posts/',views.posts, name = 'posts'), #name = mapped to named routes
    path('post_detail/<int:post_id>/', views.post_detail, name = 'post_detail'),
    path('category/<str:category_name>/', views.category_posts, name='category_posts'),
    path('search_results/', views.search_results, name='search_results'),
    path('author/<str:author_name>/', views.author_posts,name = 'author_posts'),

]