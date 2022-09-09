from django.contrib import admin
from .models import Project, ProjectRecycle, Task, TaskRecycle
from django.utils.translation import gettext_lazy as _




class TaskTabularAdmin(admin.TabularInline):
    model = Task
    fields = ("title", "description",)



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    
    fieldsets = (
        (None, {"fields": ("title", 'description', 'owner', )}),
    )

    list_display = ("title", "description", 'owner', )
    search_fields = ("title", "description", 'owner', )
    ordering = ("id",)
    inlines = (TaskTabularAdmin,)




@admin.register(ProjectRecycle)
class ProjectRecycleAdmin(admin.ModelAdmin):
    
    actions = ['recover']
    
    def get_queryset(self, queryset):
        return ProjectRecycle.deleted.filter(is_deleted=True)


    @admin.action(description="Recover Projects")
    def recover(self, request, queryset):
        queryset.update(is_deleted=False, deleted_at=None)

    fieldsets = (
        (None, {"fields": ("title", 'description',)}),
    )

    list_display = ("title", "description", )
    search_fields = ("title", "description", )
    ordering = ("id",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("title", 'description', 'project')}),
    )

    list_display = ("title", 'project')
    search_fields = ("title", "description", 'project')
    ordering = ("id",)


@admin.register(TaskRecycle)
class TaskRecycleAdmin(admin.ModelAdmin):
    
    actions = ['recover']
    
    def get_queryset(self, queryset):
        return TaskRecycle.deleted.filter(is_deleted=True)


    @admin.action(description="Recover Projects")
    def recover(self, request, queryset):
        queryset.update(is_deleted=False, deleted_at=None)
