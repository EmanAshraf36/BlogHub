from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='Category name'
    )
    slug = models.CharField(
        max_length=100,
        unique=True,
        help_text="URL-friendly version of cate name"
    )
    description = models.TextField(
        blank=True,
        help_text='Optional category description'        
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

#tags -> like categories but rel. many to many
class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text='Tag name (max 50 characters)'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        help_text='URL-friendly version of the name'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

#posts    
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft' #'database', 'human-readable'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    title = models.CharField(
        max_length=200,
        help_text='Post title (max 200 characters)'
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text='URL-friendly version of the title'
    )

    excerpt = models.TextField(
        blank=True,
        help_text='Short summary of the post'
    )

    content = models.TextField(
        help_text='Main content of the post'
    )

    status = models.CharField(
    max_length=10,
    choices=Status.choices,
    default=Status.DRAFT,
    help_text='Publication status'
    )

    is_featured = models.BooleanField(
        default=False,
        help_text='Feature this post on homepage'
    )

    allow_comments = models.BooleanField(
        default=True,
        help_text='Allow users to comment'
    )

    #Creating Relationships
    #
    author = models.ForeignKey(
        User, #one-to-many
        on_delete=models.CASCADE,
        related_name='posts' #to enable user.posts
    )

    category = models.ForeignKey(
        Category, #one-to-many
        on_delete=models.SET_NULL, #category = null
        null=True,
        blank=True,
        related_name='posts' 
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='posts'
    )

    views_count = models.IntegerField(
        default=0,
        help_text='Number of views'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(
        null=True, #database
        blank=True, #form-validation
        help_text='Date and time when published'
    )

    class Meta:
        ordering = ['-created_at'] #from most recent
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['-published_at'])
        ] #b-tree
    
    def __str__(self):
        return self.title   

    def save(self, *args, **kwargs):
        # Auto-generate slug
        if not self.slug:
            self.slug = slugify(self.title)
        
        # when status changes to published -> set published_at 
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs) #actual saving in db

#comments
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    content = models.TextField(
        help_text='Comment content'
    )

    is_approved = models.BooleanField(
        default=False,
        help_text='Approve comment for display'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', '-created_at']),
        ]
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'






















# Create your models here.
# class Post(models.Model):
#     title = models.CharField(max_length = 100)
#     content = models.TextField()
#     date_posted = models.DateTimeField(default=timezone.now) #auto_now_add: only when object is created, auto_now
#     author = models.ForeignKey(User, on_delete=models.CASCADE) #delete all posts from that user
#     #python3 manage.py makemigrations
#     '''
#     python3 manage.py sqlmigrate blog 0001
#     CREATE TABLE "blog_post" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL, "content" text NOT NULL, "date_posted" datetime NOT NULL, "author_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
#     CREATE INDEX "blog_post_author_id_dd7a8485" ON "blog_post" ("author_id");
#     COMMIT;
#     '''
#     #python3 manage.py migrate -> actually apply migrations
#     def __str__(self):
#         return self.title
    
