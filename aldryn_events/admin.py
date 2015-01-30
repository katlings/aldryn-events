# -*- coding: utf-8 -*-
import django
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from django_tablib.admin import TablibAdmin

from cms.admin.placeholderadmin import PlaceholderAdmin
from cms.admin.placeholderadmin import FrontendEditableAdmin

from parler.admin import TranslatableAdmin

from .models import Event, EventCoordinator, Registration
from .forms import EventAdminForm


class EventAdmin(FrontendEditableAdmin, TranslatableAdmin, PlaceholderAdmin):
    form = EventAdminForm
    search_fields = ('translations__title', )
    list_display = (
        'title', 'start_date', 'start_time', 'end_date', 'end_time', 'is_published', 'slug', 'location'
    )
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    filter_horizontal = ('event_coordinators', )
    date_hierarchy = 'start_date'
    frontend_editable_fields = ('title', 'short_description', 'location')

    _prepopulated_fields = {"slug": ("title",)}

    _fieldsets = (
        (None, {'fields': (
            ('title', 'slug'),
            'short_description',
            'image',
            'flyer',
            ('location', 'location_lat', 'location_lng'),
        )}),
        (None, {'fields': (
            ('start_date', 'start_time',),
            ('end_date', 'end_time',),
        )}),
        (None, {'fields': (
            'register_link',
            'detail_link',
        )}),
        (_('registration'), {'fields': (
            ('enable_registration', 'registration_deadline_at'),
            'event_coordinators',
        )}),
        (_('publishing'), {'fields': (
            ('is_published', 'publish_at',)
        )}),
    )

    def get_prepopulated_fields(self, request, obj=None):
        return self._prepopulated_fields

    def get_fieldsets(self, request, obj=None):
        return self._fieldsets


class EventCoordinatorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email_address']


class RegistrationAdmin(TablibAdmin):
    # html is giving me Unicode Error when using accentuated characters, related issue create
    # on django-tablib:
    # https://github.com/joshourisman/django-tablib/issues/43
    formats = ['xls', 'csv', 'html']
    list_display = ('first_name', 'last_name', 'event')
    list_filter = ('event', )
    date_hierarchy = 'created_at'


admin.site.register(Event, EventAdmin)
admin.site.register(EventCoordinator, EventCoordinatorAdmin)
admin.site.register(Registration, RegistrationAdmin)
