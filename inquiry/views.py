from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from authapp.models import CompanyProfile
from . import models
from .models import Inquiry, TruckType, TruckCapacity, TruckLength, AxelType, ModeOfShipment , Address,Division, Cluster,OrderQuantity,TruckDetails,CreditDays,PaymentTerms,Transporter
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseRedirect
from datetime import datetime, timedelta
import pandas as pd
from django.contrib import messages
from decimal import Decimal
# Create your views here.

@login_required
def inquiry_form_1(request):
    user = request.user
    if user.is_authenticated:
        companies = CompanyProfile.objects.all()
        truck_types = TruckType.objects.all()
        truck_details = TruckDetails.objects.all()
        order_quantity = OrderQuantity.objects.all()
        truck_lengths = TruckLength.objects.all()
        axel_types = AxelType.objects.all()
        mode_of_shipments = ModeOfShipment.objects.all()
        
        context = {
            'company_id': user.company.company_id,
            'company_name': user.company.company_name,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'companies': companies,
            'truck_types': truck_types,
            'truck_details': truck_details,
            'order_quantity': order_quantity,
            'truck_lengths': truck_lengths,
            'axel_types': axel_types,
            'mode_of_shipments': mode_of_shipments
        }
        
        return render(request, 'inquiry/inquiry_form_1.html', context)
    else:
        return redirect('/auth/login')

@login_required
def inquiry_form_2(request):
    user = request.user
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method")

    # Extracting data from form 1
    customer_id = request.POST.get('customer')
    do_be_po = request.POST.get('do_be_po')  
    consignment_description = request.POST.get('consignment_description') 
    seal_no = request.POST.get('seal_no')
    container_no = request.POST.get('container_no')
    truck_detail_id = request.POST.get('truck_number')
    truck_type_id = request.POST.get('truck_type')
    order_quantity_id = request.POST.get('order_quantity')
    truck_length_id = request.POST.get('length')  # This line is now used as truck_length
    axel_type_id = request.POST.get('axle_type')
    loading_by_consignor = request.POST.get('loading_by_consignor')
    unloading_by_consignee = request.POST.get('unloading_by_consignee')
    mode_of_shipment_id = request.POST.get('mode_of_shipment')

    # Validate and fetch actual objects from IDs
    try:
        customer = CompanyProfile.objects.get(pk=customer_id)
        truck_details = TruckDetails.objects.get(t_id=truck_detail_id)
        truck_type = TruckType.objects.get(tt_id=truck_type_id)
        order_quantity = OrderQuantity.objects.get(oq_id=order_quantity_id)
        truck_length = TruckLength.objects.get(tl_id=truck_length_id)
        axel_type = AxelType.objects.get(axel_id=axel_type_id)
        mode_of_shipment = ModeOfShipment.objects.get(ms_id=mode_of_shipment_id)
    except (CompanyProfile.DoesNotExist, TruckDetails.DoesNotExist, TruckType.DoesNotExist, OrderQuantity.DoesNotExist, TruckLength.DoesNotExist, AxelType.DoesNotExist, ModeOfShipment.DoesNotExist):
        return HttpResponseBadRequest("Invalid data provided")

    # Create and save the inquiry object
    inquiry = Inquiry(
        DO_BE_PO_NO=do_be_po,
        CONSIGNMENT_DESCRIPTION=consignment_description,
        seal_no=seal_no,
        container_no=container_no,
        loading_by_consignor=loading_by_consignor,
        unloading_by_consignee=unloading_by_consignee
    )
    inquiry.save()

    # Set ManyToMany fields
    inquiry.customer.set([customer])
    inquiry.truck_details.set([truck_details])
    inquiry.truck_type.set([truck_type])
    inquiry.order_quantity.set([order_quantity])
    inquiry.length.set([truck_length])
    inquiry.axel_type.set([axel_type])
    inquiry.mode_of_shipment.set([mode_of_shipment])
    inquiry.save()

    # Fetch data for form 2
    addresses = Address.objects.all()

    context = {
        'company_id': user.company.company_id,
        'company_name': user.company.company_name,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'addresses': addresses,
        'inquiry_id': inquiry.inquiry_id
    }
    return render(request, 'inquiry/inquiry_form_2.html', context)



@login_required
def inquiry_form_3(request):
    user = request.user
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method")

    # Assuming inquiry_id is passed as a POST parameter
    inquiry_id = request.POST.get('inquiry_id')
    if not inquiry_id:
        return HttpResponseBadRequest("No Inquiry ID provided")

    try:
        # Fetch the existing Inquiry object
        inquiry = Inquiry.objects.get(inquiry_id=inquiry_id)

        # Update the fields of the Inquiry object with data from form 2
        pickup_address = Address.objects.get(address_id=request.POST.get('pickup_address'))
        destination_address = Address.objects.get(address_id=request.POST.get('unloading_address'))

        inquiry.freight_value = request.POST.get('freight_value')
        inquiry.planned_loading_datetime = request.POST.get('planned_loading_datetime')
        inquiry.price_value = request.POST.get('price_value')
        inquiry.planned_unloading_datetime = request.POST.get('planned_unloading_datetime')

        # Save the updated Inquiry object
        inquiry.save()

        # Set ManyToMany fields
        inquiry.pickup_address.set([pickup_address])
        inquiry.destination_address.set([destination_address])
        inquiry.save()

        # Fetch data for form 3
        divisions = Division.objects.all()
        clusters = Cluster.objects.all()
        payment_terms=PaymentTerms.objects.all()
        credit_days=CreditDays.objects.all()


        # Pass inquiry_id to the template for form 3
        context = {
            'company_id': user.company.company_id,
            'company_name': user.company.company_name,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'inquiry_id': inquiry_id,
            'divisions': divisions,
            'clusters': clusters,
            'payment_terms':payment_terms,
            'credit_days':credit_days
        }
        return render(request, 'inquiry/inquiry_form_3.html', context)
    
    except Inquiry.DoesNotExist:
        return HttpResponseBadRequest("Invalid Inquiry ID")
    except Address.DoesNotExist:
        return HttpResponseBadRequest("Invalid Address ID")



@login_required
def inquiry_uploader(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseBadRequest("User is not authenticated")

    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        if file.name.endswith('.csv') or file.name.endswith('.CSV'):
            data = pd.read_csv(file)
        elif file.name.endswith('.xlsx') or file.name.endswith('.XLSX'):
            data = pd.read_excel(file)
        else:
            return HttpResponseBadRequest("Invalid file format. Please upload a CSV or XLSX file.")

        # Default values
        default_truck_length, _ = TruckLength.objects.get_or_create(truck_length='22 feet')
        default_axel_type, _ = AxelType.objects.get_or_create(axel_type='MULTI')
        default_cluster, _ = Cluster.objects.get_or_create(cluster_name='CEMENT BAGS')
        default_truck_type, _ = TruckType.objects.get_or_create(truck_type='Cement Truck')
        payment_terms,_=PaymentTerms.objects.get_or_create(payment_terms="Credit")
        credit_days,_=CreditDays.objects.get_or_create(credit_days="30 days")

        for index, row in data.iterrows():
            try:
                customer = user.company
                do_be_po_no = row['Contract']
                consignment_description = row['Material']
                seal_no = row['Contract Qty']
                container_no = row['SO Qty']

                truck_desc, _ = TruckDetails.objects.get_or_create(t_id=(row['Usage']))

                order_quantity, _ = OrderQuantity.objects.get_or_create(order_quantity=row['SO Pnd Qty'])

                # Find or create pickup and destination addresses
                pickup_address, _ = Address.objects.get_or_create(
                    customer=customer,
                    address_point=row['District'],
                    state=row['State'],
                    defaults={'customer': customer}
                )

                destination_address, _ = Address.objects.get_or_create(
                    customer=customer,
                    address_point=row['U_District'],
                    state=row['State'],
                    defaults={'customer': customer}
                )

                freight_value = row['Freight']
                planned_loading_datetime_str = f"{row['Date']} {row['Time']}"
                planned_loading_datetime = pd.to_datetime(planned_loading_datetime_str) + pd.Timedelta(days=1)
                price_value = row['Price']
                planned_unloading_datetime = planned_loading_datetime + pd.Timedelta(days=1)

                division, _ = Division.objects.get_or_create(division_name=row['Material Typ'])

                mode_of_shipment_name = row['D Channel']
                mode_of_shipment, _ = ModeOfShipment.objects.get_or_create(mode_of_shipment=mode_of_shipment_name)

                inquiry = Inquiry(
                    DO_BE_PO_NO=do_be_po_no,
                    CONSIGNMENT_DESCRIPTION=consignment_description,
                    seal_no=seal_no,
                    container_no=container_no,
                    loading_by_consignor='Yes',
                    unloading_by_consignee='Yes',
                    freight_value=freight_value,
                    planned_loading_datetime=planned_loading_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                    price_value=price_value,
                    planned_unloading_datetime=planned_unloading_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                    insurance='No'
                )
                inquiry.save()

                # Set ManyToMany fields
                inquiry.customer.set([customer])
                inquiry.truck_details.set([truck_desc])
                inquiry.truck_type.set([default_truck_type])
                inquiry.order_quantity.set([order_quantity])
                inquiry.length.set([default_truck_length])
                inquiry.axel_type.set([default_axel_type])
                inquiry.mode_of_shipment.set([mode_of_shipment])
                inquiry.pickup_address.set([pickup_address])
                inquiry.destination_address.set([destination_address])
                inquiry.division.set([division])
                inquiry.cluster.set([default_cluster])
                inquiry.payment_terms.set([payment_terms])
                inquiry.credit_days.set([credit_days])

            except Exception as e:
                return HttpResponseBadRequest(f"Error processing row {index + 1}: {str(e)}")

        return redirect('/inquiry/inquiry-table')
    context = {
            'company_id': user.company.company_id,
            'company_name': user.company.company_name,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
    }

    return render(request, 'inquiry/inquiry_uploader.html',context)

@login_required
def inquiry_table(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            # Ensure that the inquiry_id is provided in the form submission
            inquiry_id = request.POST.get('inquiry_id')
            if not inquiry_id:
                return HttpResponseBadRequest("No Inquiry ID provided")

            try:
                # Fetch the existing Inquiry object
                inquiry = Inquiry.objects.get(inquiry_id=inquiry_id)

                # Update the fields of the Inquiry object with data from form 3
                division_id = request.POST.get('division')
                cluster_id = request.POST.get('cluster')
                payment_terms = request.POST.get('payment_terms')
                credit_days = request.POST.get('credit_days')
                insurance = request.POST.get('insurance')
                pickup_address_ids = request.POST.getlist('pickup_address')
                destination_address_ids = request.POST.getlist('destination_address')

                # Fetch the Division and Cluster objects
                division = Division.objects.get(pk=division_id)
                cluster = Cluster.objects.get(pk=cluster_id)
                credit_days=CreditDays.objects.get(cd_id=credit_days)
                payment_terms=PaymentTerms.objects.get(p_id=payment_terms)

                # Update the Inquiry object with form 3 data
                inquiry.division.set([division])
                inquiry.cluster.set([cluster])
                inquiry.payment_terms.set([payment_terms])
                inquiry.credit_days.set([credit_days])
                inquiry.insurance = insurance

                # Set ManyToMany fields
                pickup_addresses = Address.objects.filter(pk__in=pickup_address_ids)
                destination_addresses = Address.objects.filter(pk__in=destination_address_ids)
                inquiry.pickup_address.set(pickup_addresses)
                inquiry.destination_address.set(destination_addresses)

                # Save the updated Inquiry object
                inquiry.save()

            except Inquiry.DoesNotExist:
                return HttpResponseBadRequest("Invalid Inquiry ID")
            except (Division.DoesNotExist, Cluster.DoesNotExist):
                return HttpResponseBadRequest("Invalid Division or Cluster ID")
            except Address.DoesNotExist:
                return HttpResponseBadRequest("Invalid Address ID")

        inquiries = Inquiry.objects.all().prefetch_related('customer', 'truck_details', 'truck_type', 'order_quantity', 'length', 'axel_type', 'mode_of_shipment', 'pickup_address', 'destination_address', 'division', 'cluster')
        addresses = Address.objects.all()
        truck_types = TruckType.objects.all()
        truck_details = TruckDetails.objects.all()

        # Prepare context data
        context = {
            'company_id': user.company.company_id,
            'company_name': user.company.company_name,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'inquiries': inquiries,
            'addresses': addresses,
            'truck_details': truck_details,
            'truck_types': truck_types
        }

        # Render inquiry table page with data
        return render(request, 'inquiry/inquiry_table.html', context)
    return HttpResponseBadRequest("User is not authenticated")

@login_required
def placement_table(request):
    user = request.user
    if user.is_authenticated:
        inquiries = Inquiry.objects.all()
        addresses = Address.objects.all()
        truck_types = TruckType.objects.all()
        truck_details = TruckDetails.objects.all()
        transporters=Transporter.objects.all()
        
        context = {
            'company_id': user.company.company_id,
            'company_name': user.company.company_name,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'inquiries': inquiries,
            'addresses': addresses,
            'truck_details': truck_details,
            'truck_types': truck_types,
            'transporters':transporters
        }
        
        return render(request, "inquiry/placement_table.html", context)


@login_required
def merge(request):
    if request.method == 'POST':
        selected_inquiry_ids = request.POST.get('selected_inquiry_ids', '').split(',')
        
        print("Selected Inquiry IDs:", selected_inquiry_ids)

        if not selected_inquiry_ids or selected_inquiry_ids == ['']:
            messages.error(request, "No Inquiries Selected!")
            return redirect("/inquiry/placement-table")
        
        # Check if the number of selected inquiries exceeds the limit
        if len(selected_inquiry_ids) > 3:
            messages.error(request, "No more than 3 Inquiries can be merged!")
            return redirect("/inquiry/placement-table")

        # Initialize the base inquiry for merging
        base_inquiry = Inquiry.objects.get(inquiry_id=selected_inquiry_ids[0])

        # Initialize a dictionary to track merged fields counts
        merged_fields_count = {}

        # Initialize the total do_be_po_no count
        total_do_be_po_no_count = 0

        # Initialize the total order quantity
        total_order_quantity = 0

        # Loop through selected inquiries to calculate the total do_be_po_no count
        for inquiry_id in selected_inquiry_ids:
            inquiry = Inquiry.objects.get(inquiry_id=inquiry_id)
            do_be_po_nos = getattr(inquiry, 'DO_BE_PO_NO').split('/')
            
            # Update the total do_be_po_no count
            total_do_be_po_no_count += len(do_be_po_nos)

            print("Inquiry ID:", inquiry_id)
            print("Do_be_po_no values:", do_be_po_nos)
            print("Count of do_be_po_no values:", len(do_be_po_nos))

        # Print the total do_be_po_no count
        print("Total count of do_be_po_no values for all selected inquiries:", total_do_be_po_no_count)

        # Check if the total do_be_po_no count exceeds the limit
        if total_do_be_po_no_count > 3:
            messages.error(request, "Merging would exceed the limit of 3 do_be_po_no values!")
            return redirect("/inquiry/placement-table")

        # Loop through selected inquiries starting from the first one
        for inquiry_id in selected_inquiry_ids:
            inquiry = Inquiry.objects.get(inquiry_id=inquiry_id)

            print("Base Inquiry before merging:", base_inquiry)
            print("Inquiry to merge:", inquiry)

            # Calculate the order_quantity sum
            order_quantities = inquiry.order_quantity.all()
            inquiry_order_quantity_sum = sum(float(qty.order_quantity) for qty in order_quantities)
            print(f"Order quantities for Inquiry {inquiry_id}: {[qty.order_quantity for qty in order_quantities]}")
            print(f"Sum of order quantities for Inquiry {inquiry_id}: {inquiry_order_quantity_sum}")
            
            total_order_quantity += inquiry_order_quantity_sum
            print(f"Running total of order quantities: {total_order_quantity}")

            # Merge CharField and ManyToManyField values
            for field in Inquiry._meta.get_fields():
                field_name = field.name
                field_type = field.get_internal_type()

                if field_type == 'CharField':
                    base_value = getattr(base_inquiry, field_name)
                    inquiry_value = getattr(inquiry, field_name)
                    if base_value != inquiry_value:
                        combined_value = f"{base_value} / {inquiry_value}"
                    else:
                        combined_value = base_value
                    setattr(base_inquiry, field_name, combined_value)

                elif field_type == 'ManyToManyField':
                    if field_name != 'order_quantity':
                        # Merge ManyToManyField values
                        base_values = list(getattr(base_inquiry, field_name).all())
                        inquiry_values = list(getattr(inquiry, field_name).all())
                        combined_values = base_values + inquiry_values
                        unique_combined_values = list(set(combined_values))

                        # Count the number of merged values for the field
                        merged_fields_count[field_name] = len(unique_combined_values)

                        print(f"Merged values for {field_name}:", unique_combined_values)
                        print(f"Count of merged values for {field_name}:", merged_fields_count[field_name])

                        # Check if merging exceeds the limit for any field
                        if merged_fields_count[field_name] > 3:
                            messages.error(request, f"Merging would exceed the limit of 3 items for field: {field_name}!")
                            return redirect("/inquiry/placement-table")
                        else:
                            getattr(base_inquiry, field_name).set(unique_combined_values)

        # Handle the total order_quantity
        print(f"Total order quantity after merging all selected inquiries: {total_order_quantity}")
        if total_order_quantity > 0:
            order_quantity_str = str(total_order_quantity)
            order_quantity_instance, created = OrderQuantity.objects.get_or_create(order_quantity=order_quantity_str)
            base_inquiry.order_quantity.set([order_quantity_instance])

        # Save the merged base inquiry
        base_inquiry.save()
        messages.success(request, "Inquiries Merged Successfully!")

    return HttpResponseRedirect('/inquiry/placement-table')
