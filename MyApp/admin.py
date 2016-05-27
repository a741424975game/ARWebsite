from django.contrib import admin
from MyApp.models import *


class BundleAdmin(admin.ModelAdmin):
    list_display = ('name', 'upload_datetime',)
    readonly_fields = ('upload_datetime', 'last_edit_datetime')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id_bundle', 'datetime',)
    readonly_fields = ('datetime',)


class ScanAdmin(admin.ModelAdmin):
    list_display = ('id_bundle', 'datetime',)
    readonly_fields = ('datetime',)


admin.site.register(Bundle, BundleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentLocation)
admin.site.register(Scan, ScanAdmin)
admin.site.register(ScanLocation)
