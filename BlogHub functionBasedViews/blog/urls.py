from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # HOME
    path('', views.home, name='home'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('post_list/', views.post_list, name='post-list'),
    path('post/create/', views.post_create, name='post-create'),
    path('post/<slug:slug>/', views.post_detail, name='post-detail'),
    path('post/<slug:slug>/update/', views.post_update, name='post-update'),
    path('post/<slug:slug>/delete/', views.post_delete, name='post-delete'),
    path('category/<str:category_name>/', views.category_posts, name='category_posts'),
    path('author/<str:author_name>/', views.author_posts, name='author_posts'),
    path('search_results/', views.search_results, name='search_results'),

    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('custom_login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]

