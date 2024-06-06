from django.db import models
from authapp.models import CompanyProfile

# Create your models here.
# dropdown models 
class TruckCapacity(models.Model):
    tc_id = models.AutoField(primary_key=True)
    truck_capacity = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.truck_capacity)
    
class OrderQuantity(models.Model):
    oq_id = models.AutoField(primary_key=True)
    order_quantity = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.order_quantity)
    
class TruckLength(models.Model):
    tl_id = models.AutoField(primary_key=True)
    truck_length = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.truck_length
    

class TruckType(models.Model):
    tt_id=models.AutoField(primary_key=True)
    truck_type=models.CharField(max_length=100, default='Cement Truck')

    def __str__(self):
        return self.truck_type
class TruckDetails(models.Model):
    t_id = models.AutoField(primary_key=True)
    truck_number = models.CharField(max_length=100, unique=True)
    truck_capacity=models.ForeignKey(TruckCapacity, on_delete=models.CASCADE, blank=True,null=True)
    truck_length=models.ForeignKey(TruckLength, on_delete=models.CASCADE, blank=True,null=True,default=1)
    ageing_duration=models.TimeField(default='20:00')
    

    def __str__(self):
        return f"{self.truck_number}-{self.truck_capacity}"



class AxelType(models.Model):
    axel_id = models.AutoField(primary_key=True)
    axel_type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.axel_type

class ModeOfShipment(models.Model):
    ms_id = models.AutoField(primary_key=True)
    mode_of_shipment = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.mode_of_shipment
    
class Address(models.Model):
    address_id=models.AutoField(primary_key=True)
    customer = models.CharField(max_length=100)
    address_point = models.CharField(max_length=100, blank=True, null=True)
    landmark = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)  # Assuming pincode as a string
    landline_number = models.CharField(max_length=11, blank=True, null=True)
    mobile_number = models.CharField(max_length=10)
    gst_number = models.CharField(max_length=15, blank=True, null=True)
  

    def __str__(self):
        return f"{self.address_point},{self.city}, {self.state}"
    
class Division(models.Model):
    division_id = models.AutoField(primary_key=True)
    division_name = models.CharField(max_length=100)

    def __str__(self):
        return self.division_name

class Cluster(models.Model):
    cluster_id = models.AutoField(primary_key=True)
    cluster_name = models.CharField(max_length=100)

    def __str__(self):
        return self.cluster_name
    

#building models for inquiry form
class Inquiry(models.Model):
    #part1
    inquiry_id=models.AutoField(primary_key=True)
    customer = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    DO_BE_PO_NO = models.IntegerField()
    CONSIGNMENT_DESCRIPTION = models.CharField(max_length=500)
    seal_no = models.IntegerField()
    container_no = models.IntegerField()
    truck_details=models.ForeignKey(TruckDetails, on_delete=models.CASCADE)
    truck_type = models.ForeignKey(TruckType, on_delete=models.CASCADE)
    order_quantity = models.ForeignKey(OrderQuantity, on_delete=models.CASCADE)
    length = models.ForeignKey(TruckLength, on_delete=models.CASCADE)
    axel_type = models.ForeignKey(AxelType, on_delete=models.CASCADE)
    loading_by_consignor = models.CharField(max_length=3)
    unloading_by_consignee = models.CharField(max_length=3)
    mode_of_shipment = models.ForeignKey(ModeOfShipment, on_delete=models.CASCADE)
    #part2
    pickup_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='pickup_address', null=True, blank=True)
    freight_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    planned_loading_datetime = models.DateTimeField(blank=True, null=True)
    destination_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='destination_address', null=True, blank=True)
    price_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    planned_unloading_datetime = models.DateTimeField(blank=True, null=True)
    #part3
    division = models.ForeignKey(Division, on_delete=models.CASCADE, blank=True, null=True)
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE, blank=True, null=True)
    payment_terms = models.CharField(max_length=100, blank=True, null=True)
    credit_days = models.CharField(max_length=100, blank=True, null=True)
    insurance = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f"Inquiry {self.inquiry_id} for {self.customer}"