
from django.contrib.gis.db import models
import uuid

class Partner(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default = uuid.uuid4,
        editable=False
    )

    trading_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    document = models.CharField(max_length=50, unique=True)


    address = models.PointField()
    coverage_area = models.MultiPolygonField()

    def __str__(self):
        return self.trading_name

