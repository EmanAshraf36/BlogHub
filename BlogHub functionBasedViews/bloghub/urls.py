from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='blog:home'   # where to go after logout
    ), name='logout'),
    
    path('register/', user_views.register, name='register'),
    
    path('', include('blog.urls')),
]
