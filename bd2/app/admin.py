from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.Worker)
admin.site.register(models.Substitution)
admin.site.register(models.SubstitutionReason)
admin.site.register(models.Permission)
admin.site.register(models.PermissionChangeReason)
admin.site.register(models.LogEntry)
admin.site.register(models.Position)