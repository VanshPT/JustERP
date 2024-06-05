from django.contrib import admin
from .models import (
    TruckType,
    TruckCapacity,
    TruckLength,
    AxelType,
    ModeOfShipment,
    Address,
    Division,
    Cluster,
    Inquiry
)

# Register your models here
admin.site.register(TruckType)
admin.site.register(TruckCapacity)
admin.site.register(TruckLength)
admin.site.register(AxelType)
admin.site.register(ModeOfShipment)
admin.site.register(Address)
admin.site.register(Division)
admin.site.register(Cluster)
admin.site.register(Inquiry)
