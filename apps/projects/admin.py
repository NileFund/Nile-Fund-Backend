from django.contrib import admin
from .models import Project, ProjectPicture, Tag


class ProjectPictureInline(admin.TabularInline):
    model = ProjectPicture
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'category', 'status', 'is_featured', 'total_target', 'created_at']
    list_filter = ['status', 'is_featured', 'category']
    search_fields = ['title', 'owner__email']
    list_editable = ['is_featured', 'status']
    inlines = [ProjectPictureInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']
