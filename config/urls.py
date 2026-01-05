
from django.contrib import admin
from django.urls import path

from store.views import PartnerDetailView
from store.views import PartnerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('partner/', PartnerView.as_view(), name = 'partner_create_search'),
    path('partner/<uuid:pk>/' , PartnerDetailView.as_view(), name =  'partner_create_search'),


]
