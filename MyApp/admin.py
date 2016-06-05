from django.contrib import admin
from MyApp.models import *


class BundleAdmin(admin.ModelAdmin):
    list_display = ('name', 'upload_datetime',)
    readonly_fields = ('likes', 'scan_times', 'comments', 'upload_datetime', 'last_edit_datetime')


class CommentStatisticsAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'id_bundle', 'amount',)
    readonly_fields = ('datetime', 'amount',)


class CommentLocationAdmin(admin.ModelAdmin):
    list_display = ('id_location', 'id_bundle', 'amount',)
    readonly_fields = ('amount',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id_bundle', 'id_location', 'datetime',)
    readonly_fields = ('datetime',)


class ScanStatisticsAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'id_bundle', 'amount',)
    readonly_fields = ('datetime', 'amount',)


class ScanLocationAdmin(admin.ModelAdmin):
    list_display = ('id_location', 'id_bundle', 'amount',)
    readonly_fields = ('amount',)


class ScanAdmin(admin.ModelAdmin):
    list_display = ('id_bundle', 'id_location', 'datetime',)
    readonly_fields = ('datetime',)


class LocationsAdmin(admin.ModelAdmin):
    list_display = ('province', 'city', 'county',)


admin.site.register(Bundle, BundleAdmin)
admin.site.register(CommentStatistics, CommentStatisticsAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentLocation, CommentLocationAdmin)
admin.site.register(ScanStatistics, ScanStatisticsAdmin)
admin.site.register(Scan, ScanAdmin)
admin.site.register(ScanLocation, ScanLocationAdmin)
admin.site.register(Locations, LocationsAdmin)
