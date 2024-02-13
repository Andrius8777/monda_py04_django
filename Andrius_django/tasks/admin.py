from django.contrib import admin
from . import models


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner']
    list_display_links = ['name', 'id']
    list_filter = ['owner']
    
    
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_done', 'deadline', 'project', 'owner', 'created_at']
    list_filter = ['is_done', 'deadline', 'created_at']
    search_fields = ['name', 'description', 'project__name', 'owner__last_name', 'owner__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        (_("general").title(), {
            "fields": (
                ('name', 'deadline', 'is_done'), 'description',
            ),
        }),
        (_('Ownership'), {
            "fields": (
                ('owner', 'project'),
            ),
        }),
        (_('Temporal Tracking'), {
            "fields": (
                ('created_at', 'updated_at', 'id'),
            ),
        }),
    )
    
    
admin.site.register(models.Project)
admin.site.register(models.Task)