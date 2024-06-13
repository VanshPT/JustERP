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
    truck_type=models.ForeignKey(TruckType, on_delete=models.CASCADE, default=1)
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
        return f"{self.address_point},{self.state}"
    
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
    
class PaymentTerms(models.Model):
    p_id=models.AutoField(primary_key=True)
    payment_terms=models.CharField(max_length=100,default=1)

    def __str__(self):
        return self.payment_terms

class CreditDays(models.Model):
    cd_id=models.AutoField(primary_key=True)
    credit_days=models.CharField(max_length=100)

    def __str__(self):
        return self.credit_days

class  Transporter(models.Model):
    tr_id=models.AutoField(primary_key=True)
    transporter_name=models.CharField(max_length=100, unique=True)
    truck_details=models.ManyToManyField(TruckDetails)

    def __str__(self):
        return self.transporter_name

#building models for inquiry form
class Inquiry(models.Model):
    #part1
    inquiry_id=models.AutoField(primary_key=True)
    customer = models.ManyToManyField(CompanyProfile)
    DO_BE_PO_NO = models.CharField(max_length=100)
    CONSIGNMENT_DESCRIPTION = models.CharField(max_length=500)
    seal_no = models.CharField(max_length=100)
    container_no = models.CharField(max_length=100)
    truck_details=models.ManyToManyField(TruckDetails)
    truck_type = models.ManyToManyField(TruckType)
    order_quantity = models.ManyToManyField(OrderQuantity)
    length = models.ManyToManyField(TruckLength)
    axel_type = models.ManyToManyField(AxelType)
    loading_by_consignor = models.CharField(max_length=3)
    unloading_by_consignee = models.CharField(max_length=3)
    mode_of_shipment = models.ManyToManyField(ModeOfShipment)
    #part2
    pickup_address = models.ManyToManyField(Address, related_name='pickup_address', null=True, blank=True)
    freight_value = models.CharField(max_length=100, blank=True, null=True)
    planned_loading_datetime = models.CharField(max_length=200,blank=True, null=True)
    destination_address = models.ManyToManyField(Address, related_name='destination_address', null=True, blank=True)
    price_value = models.CharField(max_length=100, blank=True, null=True)
    planned_unloading_datetime = models.CharField(max_length=200,blank=True, null=True)
    #part3
    division = models.ManyToManyField(Division, blank=True, null=True)
    cluster = models.ManyToManyField(Cluster,  blank=True, null=True)
    payment_terms = models.ManyToManyField(PaymentTerms,null=True,blank=True)
    credit_days = models.ManyToManyField(CreditDays, blank=True, null=True)
    insurance = models.CharField(max_length=100, blank=True, null=True)
    unmerged_order_quantities=models.CharField(max_length=200, blank=True, null=True)
    metadata = models.JSONField(null=True, blank=True)

    def __str__(self):
        customer_names = ", ".join([company.company_name for company in self.customer.all()])
        return f"Inquiry {self.inquiry_id} for {customer_names}"
    
class Assign(models.Model):
    assign_id = models.AutoField(primary_key=True)
    customer = models.ManyToManyField(CompanyProfile)
    DO_BE_PO_NO = models.CharField(max_length=100)
    CONSIGNMENT_DESCRIPTION = models.CharField(max_length=500)
    seal_no = models.CharField(max_length=100)
    container_no = models.CharField(max_length=100)
    truck_details = models.ManyToManyField(TruckDetails)
    truck_type = models.ManyToManyField(TruckType)
    order_quantity = models.ManyToManyField(OrderQuantity)
    length = models.ManyToManyField(TruckLength)
    axel_type = models.ManyToManyField(AxelType)
    loading_by_consignor = models.CharField(max_length=3)
    unloading_by_consignee = models.CharField(max_length=3)
    mode_of_shipment = models.ManyToManyField(ModeOfShipment)
    
    # Part 2
    pickup_addresses = models.ManyToManyField(Address, related_name='assign_pickup_addresses', blank=True)
    freight_value = models.CharField(max_length=100, blank=True, null=True)
    planned_loading_datetime = models.CharField(max_length=200, blank=True, null=True)
    destination_addresses = models.ManyToManyField(Address, related_name='assign_destination_addresses', blank=True)
    price_value = models.CharField(max_length=100, blank=True, null=True)
    planned_unloading_datetime = models.CharField(max_length=200, blank=True, null=True)
    
    # Part 3
    divisions = models.ManyToManyField(Division, blank=True)
    clusters = models.ManyToManyField(Cluster, blank=True)
    payment_terms = models.ManyToManyField(PaymentTerms, blank=True)
    credit_days = models.ManyToManyField(CreditDays, blank=True)
    insurance = models.CharField(max_length=100, blank=True, null=True)
    unmerged_order_quantities = models.CharField(max_length=200, blank=True, null=True)
    metadata = models.JSONField(null=True, blank=True)
    transporter = models.ForeignKey(Transporter, on_delete=models.PROTECT)

    def __str__(self):
        return f"Assign ID: {self.assign_id} - DO_BE_PO_NO: {self.DO_BE_PO_NO} - Transporter: {self.transporter}"