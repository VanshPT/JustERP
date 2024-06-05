from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from authapp.models import CompanyProfile
from . import models
from .models import Inquiry, TruckType, TruckCapacity, TruckLength, AxelType, ModeOfShipment , Address,Division, Cluster
from django.http import HttpResponseBadRequest, HttpResponse
from datetime import datetime, timedelta
import pandas as pd
# Create your views here.

@login_required
def inquiry_form_1(request):
    user=request.user
    if user.is_authenticated:
        companies=CompanyProfile.objects.all()
        truck_types=models.TruckType.objects.all()
        truck_capacity=models.TruckCapacity.objects.all()
        truck_lengths=models.TruckLength.objects.all()
        axel_types=models.AxelType.objects.all()
        mode_of_shipments=models.ModeOfShipment.objects.all()
        context={'company_id':user.company.company_id,'company_name':user.company.company_name, 'username':user.username, 'first_name':user.first_name, 'last_name': user.last_name, 'email': user.email, 'companies':companies,'truck_types': truck_types, 'truck_capacity':truck_capacity,'truck_length':truck_lengths, 'axel_types':axel_types,'mode_of_shipments':mode_of_shipments}
    return render(request, 'inquiry/inquiry_form_1.html',context)


@login_required
def inquiry_form_2(request):
    user = request.user
    if user.is_authenticated:
        if request.method != 'POST':
            return HttpResponseBadRequest("Invalid request method")

        # Extracting data from form 1
        customer_id = request.POST.get('customer')
        do_be_po = request.POST.get('do_be_po')  # Remove this line
        consignment_description = request.POST.get('consignment_description')  # Remove this line
        seal_no = request.POST.get('seal_no')
        container_no = request.POST.get('container_no')
        truck_type_id = request.POST.get('truck_type')
        truck_capacity_id = request.POST.get('truck_capacity')
        truck_length_id = request.POST.get('length')  # Remove this line
        axel_type_id = request.POST.get('axle_type')
        loading_by_consignor = request.POST.get('loading_by_consignor')
        unloading_by_consignee = request.POST.get('unloading_by_consignee')
        mode_of_shipment_id = request.POST.get('mode_of_shipment')

        # Validate and fetch actual objects from IDs
        try:
            customer = CompanyProfile.objects.get(pk=customer_id)
            truck_type = TruckType.objects.get(tt_id=truck_type_id)
            truck_capacity = TruckCapacity.objects.get(tc_id=truck_capacity_id)
            truck_length = TruckLength.objects.get(tl_id=truck_length_id)
            axel_type = AxelType.objects.get(axel_id=axel_type_id)
            mode_of_shipment = ModeOfShipment.objects.get(ms_id=mode_of_shipment_id)
        except (CompanyProfile.DoesNotExist, TruckType.DoesNotExist, TruckCapacity.DoesNotExist, TruckLength.DoesNotExist, AxelType.DoesNotExist, ModeOfShipment.DoesNotExist):
            return HttpResponseBadRequest("Invalid data provided")

        # Create and save the inquiry object
        inquiry = Inquiry(
            customer=customer,
            DO_BE_PO_NO=do_be_po,  # Update this line
            CONSIGNMENT_DESCRIPTION=consignment_description,  # Update this line
            seal_no=seal_no,
            container_no=container_no,
            truck_type=truck_type,
            truck_capacity=truck_capacity,
            length=truck_length,  # Update this line
            axel_type=axel_type,
            loading_by_consignor=loading_by_consignor,
            unloading_by_consignee=unloading_by_consignee,
            mode_of_shipment=mode_of_shipment
        )
        inquiry.save()

        # Fetch data for form 2
        addresses = Address.objects.all()

        context = {
            'company_id': user.company.company_id, 'company_name': user.company.company_name,
            'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name,
            'email': user.email,
            'addresses': addresses,
            'inquiry_id': inquiry.inquiry_id
        }
        return render(request, 'inquiry/inquiry_form_2.html', context)


@login_required
def inquiry_form_3(request):
    user = request.user
    if user.is_authenticated:
        # Assuming inquiry_id is passed as a POST parameter
        inquiry_id = request.POST.get('inquiry_id')
        if inquiry_id:
            try:
                # Fetch the existing Inquiry object
                inquiry = Inquiry.objects.get(inquiry_id=inquiry_id)

                # Update the fields of the Inquiry object with data from form 2
                # Assuming you receive data from form 2 as POST parameters
                inquiry.pickup_address = Address.objects.get(address_id=request.POST.get('pickup_address'))
                inquiry.freight_value = request.POST.get('freight_value')
                inquiry.planned_loading_datetime = request.POST.get('planned_loading_datetime')
                inquiry.destination_address = Address.objects.get(address_id=request.POST.get('unloading_address'))
                inquiry.price_value = request.POST.get('price_value')
                inquiry.planned_unloading_datetime = request.POST.get('planned_unloading_datetime')

                # Save the updated Inquiry object
                inquiry.save()
                divisions=Division.objects.all()
                clusters=Cluster.objects.all()
                # Pass inquiry_id to the template for form 3
                context = {'company_id': user.company.company_id, 'company_name': user.company.company_name,
                           'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name,
                           'email': user.email, 'inquiry_id': inquiry_id, 'divisions':divisions, 'clusters':clusters}
                return render(request, 'inquiry/inquiry_form_3.html', context)
            except Inquiry.DoesNotExist:
                return HttpResponseBadRequest("Invalid Inquiry ID")
        else:
            return HttpResponseBadRequest("No Inquiry ID provided")
    return HttpResponseBadRequest("User is not authenticated")


@login_required
def inquiry_uploader(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseBadRequest("User is not authenticated")

    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        if file.name.endswith('.csv'):
            data = pd.read_csv(file)
        elif file.name.endswith('.xlsx') or file.name.endswith('.XLSX'):
            data = pd.read_excel(file)
        else:
            return HttpResponseBadRequest("Invalid file format. Please upload a CSV or XLSX file.")

        # Default values
        default_truck_length, _ = TruckLength.objects.get_or_create(truck_length='22 feet')
        default_axel_type, _ = AxelType.objects.get_or_create(axel_type='MULTI')
        default_cluster, _ = Cluster.objects.get_or_create(cluster_name='CEMENT BAGS')

        for index, row in data.iterrows():
            try:
                customer = user.company
                do_be_po_no = row['Contract']
                consignment_description = row['Material']
                seal_no = row['Contract Qty']
                container_no = row['SO Qty']
                
                truck_type, _ = TruckType.objects.get_or_create(tt_id=(row['Usage']+1))

                # Ensure that the truck type is retrieved or created successfully
                # You might need to handle errors or constraints related to this operation

                truck_capacity, _ = TruckCapacity.objects.get_or_create(truck_capacity=row['SO Pnd Qty'])

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
                planned_loading_datetime = pd.to_datetime(planned_loading_datetime_str) + timedelta(days=1)
                price_value = row['Price']
                planned_unloading_datetime = planned_loading_datetime + timedelta(days=1)

                division, _ = Division.objects.get_or_create(division_name=row['Material Typ'])

                mode_of_shipment_name = row['D Channel']
                mode_of_shipment, _ = ModeOfShipment.objects.get_or_create(mode_of_shipment=mode_of_shipment_name)

                inquiry = Inquiry(
                    customer=customer,
                    DO_BE_PO_NO=do_be_po_no,
                    CONSIGNMENT_DESCRIPTION=consignment_description,
                    seal_no=seal_no,
                    container_no=container_no,
                    truck_type=truck_type,
                    truck_capacity=truck_capacity,
                    length=default_truck_length,
                    axel_type=default_axel_type,
                    loading_by_consignor='Yes',
                    unloading_by_consignee='Yes',
                    mode_of_shipment=mode_of_shipment,
                    pickup_address=pickup_address,
                    freight_value=freight_value,
                    planned_loading_datetime=planned_loading_datetime,
                    destination_address=destination_address,
                    price_value=price_value,
                    planned_unloading_datetime=planned_unloading_datetime,
                    division=division,
                    cluster=default_cluster,
                    payment_terms='Credit',
                    credit_days='30 days',
                    insurance='No'
                )
                inquiry.save()
            except Exception as e:
                return HttpResponseBadRequest(f"Error processing row {index + 1}: {str(e)}")

        return redirect('/inquiry/inquiry-table')

    context = {
        'company_id': user.company.company_id,
        'company_name': user.company.company_name,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }
    return render(request, 'inquiry/inquiry_uploader.html', context)

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

                # Fetch the Division and Cluster objects
                division = Division.objects.get(pk=division_id)
                cluster = Cluster.objects.get(pk=cluster_id)

                # Update the Inquiry object with form 3 data
                inquiry.division = division
                inquiry.cluster = cluster
                inquiry.payment_terms = payment_terms
                inquiry.credit_days = credit_days
                inquiry.insurance = insurance

                # Save the updated Inquiry object
                inquiry.save()

                # Fetch all inquiries
                inquiries = Inquiry.objects.all()

                # Prepare context data
                context = {
                    'company_id': user.company.company_id,
                    'company_name': user.company.company_name,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'inquiries': inquiries
                }

                # Redirect to inquiry table page with updated data
                return render(request, 'inquiry/inquiry_table.html', context)

            except Inquiry.DoesNotExist:
                return HttpResponseBadRequest("Invalid Inquiry ID")
            except (Division.DoesNotExist, Cluster.DoesNotExist):
                return HttpResponseBadRequest("Invalid Division or Cluster ID")

        elif request.method == 'GET':
            # Fetch all inquiries
            inquiries = Inquiry.objects.all()

            # Prepare context data
            context = {
                'company_id': user.company.company_id,
                'company_name': user.company.company_name,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'inquiries': inquiries
            }

            # Render inquiry table page with data
            return render(request, 'inquiry/inquiry_table.html', context)

        else:
            return HttpResponseBadRequest("Invalid request method")
    else:
        return HttpResponseBadRequest("User is not authenticated")