from django.contrib import admin
from .models import Project, ProjectRecycle


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(ProjectRecycle)
class ProjectRecycleAdmin(admin.ModelAdmin):
    
    actions = ['recover']
    
    def get_queryset(self, queryset):
        return ProjectRecycle.deleted.filter(is_deleted=True)


    @admin.action(description="Recover Projects")
    def recover(self, request, queryset):
        queryset.update(is_deleted=False, deleted_at=None)
