from django.contrib import admin
from store import models

class PartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'trading_name', 'owner_name', 'document', 'address', 'coverage_area')

    admin.site.register(models.Partner)
