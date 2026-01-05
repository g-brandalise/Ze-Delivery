
from store.models import Partner
from rest_framework_gis.serializers import GeoModelSerializer

class PartnerSerializer(GeoModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'

