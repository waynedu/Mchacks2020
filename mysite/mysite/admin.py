from django.contrib import admin
from .models import Person, Family
from django.conf import settings
from django.contrib import admin

admin.site.site_header = settings.ADMIN_SITE_HEADER


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'last_known_location']


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ['id', 'last_name']
