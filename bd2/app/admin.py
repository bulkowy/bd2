from django.contrib import admin

# Register your models here.

from . import models, forms

@admin.register(models.Worker)
class WorkerAdmin(admin.ModelAdmin):
    form = forms.WorkerForm

    list_display = ['name', 'surname', 'position', 'supervisor']
    list_display_links = ['name', 'surname']
    list_filter = ['position', 'supervisor']

@admin.register(models.Substitution)
class SubstitutionAdmin(admin.ModelAdmin):
    form = forms.SubstitutionForm

    list_display = ['substitute_begin', 'substitute_end', 
        'substituted_worker', 'substituting_worker', 'reason'
    ]
    list_display_links = ['substitute_begin', 'substitute_end']
    list_filter = ['reason']
    search_fields = ['substituted_worker__name', 'substituted_worker__surname',
        'substituting_worker__name', 'substituting_worker__surname'
    ]

@admin.register(models.LogEntry)
class LogEntryAdmin(admin.ModelAdmin):

    readonly_fields = [
        'substitute_begin', 'substitute_end',
        'subbed', 'subbing', 'reason',
        'old_perms', 'new_perms']

    list_display = ['substitute_begin', 'substitute_end', 'subbed', 'subbing', 'reason']
    list_display_links = ['substitute_begin', 'substitute_end']
    list_filter = ['reason']
    search_fields = ['subbed', 'subbing']


admin.site.register(models.SubstitutionReason)
admin.site.register(models.Permission)
admin.site.register(models.PermissionChangeReason)
admin.site.register(models.Position)