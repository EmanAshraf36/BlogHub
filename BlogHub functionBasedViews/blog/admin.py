from django.contrib import admin
from .models import Category, Tag, Post, Comment

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone

from .models import Category, Tag, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "created_at"]
    list_display_links = ["name"]
    search_fields = ["name", "slug", "description"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["name"]
    list_per_page = 25


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "created_at"]
    list_display_links = ["name"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["name"]
    list_per_page = 25


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ["author", "content", "is_approved", "created_at"]
    readonly_fields = ["created_at"]
    show_change_link = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # List page
    list_display = [
        "title",
        "author",
        "category",
        "status_badge",
        "is_featured",
        "views_count",
        "created_at",
        "published_at",
    ]
    list_display_links = ["title"]
    list_filter = [
        "status",
        "is_featured",
        "allow_comments",
        "category",
        "tags",
        "created_at",
        "published_at",
    ]
    search_fields = [
        "title",
        "slug",
        "excerpt",
        "content",
        "author__username",
        "category__name",
        "tags__name",
    ]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
    list_per_page = 25

    # Readonly fields
    readonly_fields = ["views_count", "created_at", "updated_at", "published_at"]

    # Inlines
    inlines = [CommentInline]

    # Form layout
    fieldsets = (
        (
            "Basic Information",
            {
                "fields": ("title", "slug", "author", "category", "tags"),
            },
        ),
        (
            "Content",
            {
                "fields": ("excerpt", "content"),
            },
        ),
        (
            "Status & Visibility",
            {
                "fields": ("status", "is_featured", "allow_comments"),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("views_count", "published_at", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    # Custom column for colored status badge
    def status_badge(self, obj):
        colors = {
            obj.Status.DRAFT: "gray",
            obj.Status.PUBLISHED: "green",
            obj.Status.ARCHIVED: "red",
        }
        color = colors.get(obj.status, "gray")
        return format_html(
            '<span style="background-color:{};color:white;padding:2px 8px;border-radius:3px;font-size:12px;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = "Status"
    status_badge.admin_order_field = "status"

    # Custom actions
    actions = ["publish_posts", "mark_as_featured", "unfeature_posts"]

    def publish_posts(self, request, queryset):
        updated = queryset.update(
            status=Post.Status.PUBLISHED,
            published_at=timezone.now(),
        )
        self.message_user(request, f"{updated} post(s) marked as published.")

    publish_posts.short_description = "Mark selected posts as Published"

    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f"{updated} post(s) marked as featured.")

    mark_as_featured.short_description = "Mark selected posts as Featured"

    def unfeature_posts(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f"{updated} post(s) unfeatured.")

    unfeature_posts.short_description = "Unfeature selected posts"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "post",
        "author",
        "short_content",
        "is_approved",
        "created_at",
    ]
    list_filter = ["is_approved", "created_at", "post"]
    search_fields = ["content", "author__username", "post__title"]
    ordering = ["-created_at"]
    list_per_page = 25

    def short_content(self, obj):
        return (obj.content[:50] + "...") if len(obj.content) > 50 else obj.content

    short_content.short_description = "Comment"