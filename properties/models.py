from django.db import models
from owners.models import Owner

class Property(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='properties')
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1)
    max_occupancy = models.PositiveIntegerField()
    nightly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Properties"