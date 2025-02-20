from django.contrib import admin
from .models import Facility, Booking


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'capacity', 'created_at')
    search_fields = ('name', 'location')
    list_filter = ('location',)
    ordering = ('name',)
    list_per_page = 20


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'facility',
        'date',
        'start_time',
        'end_time',
        'status',
        'created_at')
    list_filter = ('status', 'facility', 'date')
    search_fields = ('user__username', 'facility__name')
    ordering = ('-date', '-start_time')
    list_editable = ('status',)
    list_per_page = 20
    date_hierarchy = 'date'

    fieldsets = (
        ('Booking Information', {
            'fields': ('user', 'facility', 'date', 'start_time', 'end_time', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
