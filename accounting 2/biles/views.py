from django.shortcuts import render , get_object_or_404 , redirect

from users.models import CustomUser
from .forms import MainProductForm ,JarForm , PackageForm , ProductHamForm
from django.contrib.auth import authenticate, login, logout
from .models import ProductHam , Package , Jar ,MainProduct  , ProductHam, UdsBill_inner, UdsBills
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import csv
import uuid
from django.http import HttpResponse
from django.utils.encoding import smart_str  # Import smart_str for encoding

from customers.models import Costomers
from customers.forms import CostomersForm , CostomersFormAdvanv
from django.utils import timezone





from django.contrib.auth.forms import AuthenticationForm
# Create your views here.





 # --------------------------  this page for adding  ProductHam -----------------

def addProductHam(request):
    if request.method == 'POST':
        form = ProductHamForm(request.POST)
        if form.is_valid():
             main_product = form.save(commit=False)
             main_product.created_by = request.user

       
             main_product.save()
              # Redirect to a list of clients or another page
    else:
        form = ProductHamForm()
    return render(request, 'ProductHam/add.html', {'form': form})


def ProductHam_List(request):
    ProductHam_List = ProductHam.objects.filter(created_by=request.user.id)
    return render(request, 'ProductHam/list.html', {'ProductHam': ProductHam_List})




def fatch_ProductHam(request , id):

    productHamm = ProductHam.objects.get(pk=id)
   
    return render(request, 'ProductHam/view.html', {'ProductHam': productHamm})



def update_ProductHam(request, id):
    ProductHamm = get_object_or_404(ProductHam, pk=id , created_by=request.user.id)
    
    if request.method == 'POST':
        form = ProductHamForm(request.POST, instance=ProductHamm)
        if form.is_valid():
            form.save()
            return redirect('fatch_ProductHam', id=id)  # Redirect to client detail page
    else:
        form = ProductHamForm(instance=ProductHamm)
    
    return render(request, 'ProductHam/edit.html', {'form': form})




def delete_ProductHamm(request, id):
    ProductHamm = ProductHam.objects.filter(created_by=request.user.id)
    ProductHamm_list = get_object_or_404(ProductHamm, pk=id)
    if request.method == 'POST':
        ProductHamm_list.delete()
        messages.success(request, 'ProductHamm deleted successfully.')
        return redirect('ProductHam_List')
    return render(request, 'ProductHam/view.html', {'ProductHam': ProductHamm_list })





@login_required
def uplode_ProductHam(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']
        try:
            decoded_file = csv_file.read().decode('utf-8-sig').splitlines()
            reader = csv.DictReader(decoded_file, delimiter=';')

            for row in reader:
                product_name = row['product_name']
                top = int(row.get('top', 0))  # Convert to integer, default to 0 if empty
                percentage = int(row.get('percentage', 0))  # Convert to integer, default to 0 if empty
                image = row.get('image', '')  # Handle optional image field

                product, created = ProductHam.objects.get_or_create(
                    product_name=product_name,
                    defaults={
                        'top': top,
                        'percentage': percentage,
                        'image': image,
                        'created_by': request.user,
                    }
                )

                if not created:
                    # Update fields if product already exists
                    product.top = top
                    product.percentage = percentage
                    if image:
                        product.image = image
                    product.save()

            messages.success(request, "Products uploaded successfully")
            return redirect('uplode_ProductHam')

        except Exception as e:
            messages.error(request, f"An error occurred while processing the file: {e}")
            return redirect('uplode_ProductHam')

    return render(request, 'ProductHam/uplode.html')








@login_required
def uplode_ProductHam(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']
        try:
            decoded_file = csv_file.read().decode('utf-8-sig').splitlines()
            reader = csv.DictReader(decoded_file, delimiter=';')

            # Fetch all existing products to compare with CSV data
            existing_products = ProductHam.objects.all()
            existing_product_names = {product.product_name for product in existing_products}

            for row in reader:
                product_name = row['product_name']
                top = int(row.get('top', 0))  # Convert to integer, default to 0 if not provided
                percentage = int(row.get('percentage', 0))  # Convert to integer, default to 0 if not provided
                image = row.get('image', '')  # Handle optional field

                # Check if product with the same name exists in both CSV and database
                if product_name in existing_product_names:
                    product = ProductHam.objects.get(product_name=product_name)
                    # Update existing product from CSV data
                    product.top = top
                    product.percentage = percentage
                    product.image = image  # Update image regardless if it's empty or not
                    product.save()
                    existing_product_names.remove(product_name)  # Remove from set to track existing records
                else:
                    # Create new product since product_name doesn't exist in the database
                    ProductHam.objects.create(
                        product_name=product_name,
                        top=top,
                        percentage=percentage,
                        image=image,
                        created_by=request.user
                    )

            # Delete any products that exist in the database but not in the CSV file
            ProductHam.objects.filter(product_name__in=existing_product_names).delete()

            messages.success(request, "Products uploaded successfully")
            return redirect('uplode_ProductHam')

        except Exception as e:
            messages.error(request, f"An error occurred while processing the file: {e}")
            return redirect('uplode_ProductHam')

    return render(request, 'ProductHam/uplode.html')




def download_ProductHam_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="ProductHam.csv"'

    writer = csv.writer(response)
    writer.writerow([
        smart_str('id'),
        smart_str('product_name'),
        smart_str('top'),
        smart_str('percentage'),
        smart_str('image'),
    ])

    ProductHamlist = ProductHam.objects.all()
    for ProductHamm in ProductHamlist:
        writer.writerow([
            ProductHamm.id,
            smart_str(ProductHamm.product_name),
            smart_str(ProductHamm.top),
            smart_str(ProductHamm.percentage),
            smart_str(ProductHamm.image if ProductHamm.image else ''),
        ])

    return response



 # --------------------------  this page for adding  ProductHam -----------------





 # --------------------------  this page for adding  pakage -----------------



def addPakage(request):
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
             main_product = form.save(commit=False)
             main_product.created_by = request.user

       
             main_product.save()
              # Redirect to a list of clients or another page
    else:
        form = PackageForm()
    return render(request, 'Pakage/add.html', {'form': form})


def pakage_List(request):
    Package_List = Package.objects.filter(created_by=request.user.id)
    return render(request, 'Pakage/list.html', {'Package': Package_List})


def fatch_pakage(request , id):

    Package_fatch =Package.objects.get(pk=id)
   
    return render(request, 'pakage/view.html', {'pakage': Package_fatch})



def update_pakage(request, id):
    pakage = get_object_or_404(Package, pk=id , created_by=request.user.id)
    
    if request.method == 'POST':
        form = PackageForm(request.POST, instance=pakage)
        if form.is_valid():
            form.save()
            return redirect('fatch_pakage', id=id)  # Redirect to client detail page
    else:
        form = PackageForm(instance=pakage)
    
    return render(request, 'pakage/edit.html', {'form': form})






def delete_pakage(request, id):
    pakage = Package.objects.filter(created_by=request.user.id)
    pakage_list = get_object_or_404(pakage, pk=id)
    if request.method == 'POST':
        pakage_list.delete()
        messages.success(request, 'pakage deleted successfully.')
        return redirect('pakage_List')
    return render(request, 'pakage/view.html', {'pakage': pakage_list })

@login_required
def uplode_package(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']
        try:
            decoded_file = csv_file.read().decode('utf-8-sig').splitlines()
            reader = csv.DictReader(decoded_file, delimiter=';')

            for row in reader:
                package_id = int(row['id'].strip())  # Convert id to integer
                package_name = row['package_name'].strip()
                package_arabic = row.get('package_arabic', '').strip()  # Handle optional fields gracefully
                image = row.get('image', '').strip()  # Handle optional fields gracefully

                # Check if package with the same id exists
                try:
                    package = Package.objects.get(id=package_id)
                except Package.DoesNotExist:
                    package = None

                if package:
                    # Update existing package from CSV data
                    if package_name:
                        package.package_name = package_name
                    if package_arabic:
                        package.package_arabic = package_arabic
                    if image:
                        package.image = image
                    package.save()
                else:
                    # Create new package since id doesn't exist in the model
                    Package.objects.create(
                        id=package_id,
                        package_name=package_name,
                        package_arabic=package_arabic,
                        image=image,
                        created_by=request.user
                    )

            messages.success(request, "Packages uploaded successfully")
            return redirect('uplode_package')

        except Exception as e:
            messages.error(request, f"An error occurred while processing the file: {e}")
            return redirect('uplode_package')

    return render(request, 'Pakage/uplode.html')


def download_pakage_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="pakage.csv"'

    writer = csv.writer(response)
    writer.writerow([
        smart_str('id'),
        smart_str('package_name'),
        smart_str('package_arabic'),

        smart_str('image'),
    ])

    pakagelist = Package.objects.all()
    for pakage in pakagelist:
        writer.writerow([
            pakage.id,
            smart_str(pakage.package_name),
            smart_str(pakage.package_arabic),
            smart_str(pakage.image if pakage.image else ''),
        ])

    return response



 # --------------------------  this page for adding  ProductHam -----------------





 # --------------------------  this page for adding  pakage -----------------







def addjar(request):
    if request.method == 'POST':
        form = JarForm(request.POST)
        if form.is_valid():
             main_product = form.save(commit=False)
             main_product.created_by = request.user

       
             main_product.save()
              # Redirect to a list of clients or another page
    else:
        form = JarForm()
    return render(request, 'jar/add.html', {'form': form})




def jar_List(request):
    jar_List = Jar.objects.filter(created_by=request.user.id)
    return render(request, 'jar/list.html', {'form': jar_List})





def fatch_jar(request , id):

    jar_fatch =Jar.objects.get(pk=id)
   
    return render(request, 'jar/view.html', {'form': jar_fatch})


def update_jar(request, id):
    jar = get_object_or_404(Jar, pk=id , created_by=request.user.id)
    
    if request.method == 'POST':
        form = JarForm(request.POST, instance=jar)
        if form.is_valid():
            form.save()
            return redirect('fatch_jar', id=id)  # Redirect to client detail page
    else:
        form = JarForm(instance=jar)
    
    return render(request, 'jar/edit.html', {'form': form})





def delete_jar(request, id):
    jar = Jar.objects.filter(created_by=request.user.id)
    Jar_list = get_object_or_404(jar, pk=id)
    if request.method == 'POST':
        Jar_list.delete()
        messages.success(request, 'jar deleted successfully.')
        return redirect('jar_List')
    return render(request, 'jar/view.html', {'form': Jar_list })

@login_required
def uplode_jar(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']
        try:
            decoded_file = csv_file.read().decode('utf-8-sig').splitlines()
            reader = csv.DictReader(decoded_file, delimiter=';')

            required_fields = ['jar_name', 'image']

            for row in reader:
                if not all(field in row for field in required_fields):
                    messages.error(request, "CSV file is missing one or more required fields.")
                    return redirect('uplode_jar')

                jar_name = row['jar_name']
                image = row['image'] if row['image'] else None

                jar, created = Jar.objects.get_or_create(
                    jar_name=jar_name,
                    defaults={
                        'image': image,
                        'created_by': request.user,  # Set created_by to the current user
                    }
                )

                if not created:
                    if not jar.image and image:
                        jar.image = image
                    jar.save()

            messages.success(request, "jar uploaded successfully")
            return redirect('uplode_jar')

        except Exception as e:
            messages.error(request, f"An error occurred while processing the file: {e}")
            return redirect('uplode_jar')

    return render(request, 'jar/uplode.html')


def download_jar_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="jar.csv"'

    writer = csv.writer(response)
    writer.writerow([
        smart_str('id'),
        smart_str('jar_name'),
   

        smart_str('image'),
    ])

    jar = Jar.objects.filter(created_by=request.user.id)
    for i in jar:
        writer.writerow([
            i.id,
            smart_str(i.jar_name),
         
            smart_str(i.image if i.image else ''),
        ])

    return response










 # --------------------------  this page for ending jar -----------------



def addProduct(request):
    if request.method == 'POST':
        form = MainProductForm(request.POST, user=request.user.id)
        if form.is_valid():
            main_product = form.save(commit=False)
            main_product.created_by = request.user.id
            main_product.save()
        #    return redirect('main_product_list')   Update with your success URL
    else:
        form = MainProductForm(user=request.user)
    return render(request, 'product/add.html', {'form': form})




def Product_List(request):
    product = MainProduct.objects.filter(created_by=request.user.id)

    return render(request, 'product/list.html', {'form': product})



def fatch_Product(request , id):

    product = MainProduct.objects.get(pk=id)
    print(product)
   
    return render(request, 'product/view.html', {'form': product})



def update_Product(request, id):
    product = get_object_or_404(MainProduct, pk=id , created_by=request.user.id)
    
    if request.method == 'POST':
        form = MainProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('fatch_Product', id=id)  # Redirect to client detail page
    else:
        form = MainProductForm(instance=product)
    
    return render(request, 'product/edit.html', {'form': form})



def delete_Product(request, id):
    product = MainProduct.objects.filter(created_by=request.user.id)
    product_list = get_object_or_404(product, pk=id)
    if request.method == 'POST':
        product_list.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('Product_List')
    return render(request, 'product/view.html', {'form': product_list })


def uplode_product(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']
        try:
            decoded_file = csv_file.read().decode('utf-8-sig').splitlines()
            reader = csv.DictReader(decoded_file, delimiter=';')

            required_fields = ['product_name', 'product_type', 'product_ham', 'jar', 'package', 
                               'image', 'net_weight', 'top_weight', 'amount_inside', 'qr']

            for row in reader:
                if not all(field in row for field in required_fields):
                    messages.error(request, "CSV file is missing one or more required fields.")
                    return redirect('uplode_product')

                product_name = row['product_name']
                product_type = row['product_type']
                product_ham = int(row['product_ham']) if row['product_ham'] else None
                jar = int(row['jar']) if row['jar'] else None
                package = int(row['package']) if row['package'] else None
                net_weight = int(row['net_weight']) if row['net_weight'] else None
                top_weight = int(row['top_weight']) if row['top_weight'] else None
                amount_inside = int(row['amount_inside']) if row['amount_inside'] else None
                qr = int(row['qr']) if row['qr'] else None
                image = row['image'] if row['image'] else None

                product_ham_instance = ProductHam.objects.get(pk=product_ham)
                jar_instance = Jar.objects.get(pk=jar)
                package_instance = Package.objects.get(pk=package)

                main_product, created = MainProduct.objects.get_or_create(
                    qr=qr,
                    defaults={
                        'product_name': product_name,
                        'product_type': product_type,
                        'product_ham': product_ham_instance,
                        'jar': jar_instance,
                        'package': package_instance,
                        'image': image,
                        'net_weight': net_weight,
                        'top_weight': top_weight,
                        'amount_inside': amount_inside,
                        'created_by': request.user,
                    }
                )

                if not created:
                    main_product.product_name = product_name
                    main_product.product_type = product_type
                    main_product.product_ham = product_ham_instance
                    main_product.jar = jar_instance
                    main_product.package = package_instance
                    main_product.image = image
                    main_product.net_weight = net_weight
                    main_product.top_weight = top_weight
                    main_product.amount_inside = amount_inside
                    main_product.created_by = request.user

                    main_product.save()

            messages.success(request, "MainProduct uploaded successfully")
            return redirect('uplode_product')

        except Exception as e:
            messages.error(request, f"An error occurred while processing the file: {e}")
            return redirect('uplode_product')

    return render(request, 'product/upload.html')


def download_product_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    # Define the response and set the content type to 'text/csv'
    
    response['Content-Disposition'] = 'attachment; filename="main_products.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['product_name', 'product_type', 'product_ham', 'jar', 'package', 
                     'image', 'net_weight', 'top_weight', 'amount_inside', 'qr'])

    # Write the data rows
    for product in MainProduct.objects.filter(created_by=request.user.id):
        writer.writerow([
            product.product_name,
            product.product_type,
            product.product_ham.pk,
            product.jar.pk,
            product.package.pk,
            product.image,
            product.net_weight,
            product.top_weight,
            product.amount_inside,
            product.qr,
        ])

    return response






def add_costomer(request):
    if request.method == 'POST':
        form = CostomersFormAdvanv(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()
            
            

            return redirect('costomers_List')
              # Redirect to a list of clients or another page
    else:
        form = CostomersFormAdvanv()
    return render(request, 'costomers/add.html', {'form': form})





def costomers_List(request):
    Costomers_List = Costomers.objects.filter(created_by=request.user.id)
    return render(request, 'costomers/list.html', {'form': Costomers_List})





def update_costomers(request, id):
    costomer = get_object_or_404(Costomers, pk=id , created_by=request.user.id)
    
    if request.method == 'POST':
        form = CostomersFormAdvanv(request.POST, instance=costomer)
        if form.is_valid():
            form.save()
            return redirect('fatch_costomers', id=id)  # Redirect to client detail page
    else:
        form = CostomersFormAdvanv(instance=costomer)
    
    return render(request, 'costomers/edit.html', {'form': form})





def fatch_costomers(request , id):

    costomer = Costomers.objects.get(pk=id)
   
    return render(request, 'costomers/view.html', {'form': costomer})


def delete_costomers(request, id):
    costomer = Costomers.objects.filter(created_by=request.user.id)
    costomer_list = get_object_or_404(costomer, pk=id)
    if request.method == 'POST':
        costomer_list.delete()
        messages.success(request, 'ProductHamm deleted successfully.')
        return redirect('costomers_List')
    return render(request, 'ProductHam/view.html', {'form': costomer_list })








def download_costomers_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
  
    
    response['Content-Disposition'] = 'attachment; filename="costomers.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['id','name', 'tex',  'email', 'number', 'address' ,'token', 'is_company', 'company', 'image'])

    # Write the data rows
    for i in Costomers.objects.filter(created_by=request.user.id):
        writer.writerow([
            i.id,
            i.name,
            i.tex,
            i.email,
            i.number,
            i.address,
            i.token,
            i.is_company,
            i.company,
            i.image,
        
        ])

    return response




#








@login_required
def upload_customers(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file, delimiter=';')

        for row in reader:
            # Generate a unique token if not provided or if the provided token already exists
            token = row.get('token', str(uuid.uuid4()))
            while Costomers.objects.filter(token=token).exists():
                token = str(uuid.uuid4())

            customer, created = Costomers.objects.get_or_create(
                name=row.get('name', ''),
                defaults={
                    'created_by': request.user,
                    'image': row.get('image', None),
                    'tex': row.get('tex', None),
                    'email': row.get('email', None),
                    'number': row.get('number', None),
                    'is_company': row.get('is_company', '').strip().lower() == 'true',
                    'company': row.get('company', None),
                    'address': row.get('address', None),
                    'token': token
                }
            )
            if not created:
                # Update only the empty fields of the existing customer
                if not customer.image and row.get('image'):
                    customer.image = row.get('image')
                if not customer.tex and row.get('tex'):
                    customer.tex = row.get('tex')
                if not customer.email and row.get('email'):
                    customer.email = row.get('email')
                if not customer.number and row.get('number'):
                    customer.number = row.get('number')
                if not customer.is_company and row.get('is_company'):
                    customer.is_company = row.get('is_company', '').strip().lower() == 'true'
                if not customer.company and row.get('company'):
                    customer.company = row.get('company')
                if not customer.address and row.get('address'):
                    customer.address = row.get('address')
                if not customer.token and row.get('token'):
                    customer.token = row.get('token')
                customer.save()

        messages.success(request, "Customers uploaded successfully")
        return redirect('upload_customers')

    return render(request, 'costomers/upload.html')





@login_required
def upload_uds_bills(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']
        try:
            decoded_file = csv_file.read().decode('utf-8-sig').splitlines()
            reader = csv.DictReader(decoded_file, delimiter=';')

            required_fields = ['id', 'customer', 'is_paid', 'created_at', 'note', 'price', 'net', 'top']

            # Check if all required fields are present
            headers = reader.fieldnames
            missing_fields = [field for field in required_fields if field not in headers]
            if missing_fields:
                messages.error(request, f"CSV file is missing required fields: {', '.join(missing_fields)}.")
                return redirect('upload_uds_bills')

            for row in reader:
                try:
                    uds_bill_id = int(row['id'].strip()) if row['id'] else None
                    customer_id = int(row['customer'].strip()) if row['customer'] else None
                    is_paid = row['is_paid'].strip().lower() == 'true'
                    created_at = timezone.datetime.strptime(row['created_at'].strip(), '%d-%b-%y').date() if row['created_at'] else None
                    note = row['note'].strip() if row['note'] else None
                    net = int(row['net'].strip()) if row['net'] else 0
                    top = int(row['top'].strip()) if row['top'] else 0
                    price = int(row['price'].strip()) if row['price'] else 0

                    # Retrieve the customer object
                    customer = Costomers.objects.get(pk=customer_id)

                    # Create or update UdsBills object
                    uds_bill, created = UdsBills.objects.get_or_create(
                        id=uds_bill_id,
                        defaults={
                            'created_by': request.user,
                            'customer': customer,
                            'is_paid': is_paid,
                            'created_at': created_at,
                            'note': note,
                            'price': price,
                            'net': net,
                            'top': top,
                        }
                    )

                    # If not created, update the existing UdsBills object
                    if not created:
                        uds_bill.created_by = request.user
                        uds_bill.customer = customer
                        uds_bill.is_paid = is_paid
                        uds_bill.created_at = created_at
                        uds_bill.note = note
                        uds_bill.price = price
                        uds_bill.net = net
                        uds_bill.top = top
                        uds_bill.save()

                except Exception as e:
                    messages.error(request, f"Error processing row: {str(e)}")
                    continue

            messages.success(request, "UdsBills uploaded successfully")
            return redirect('upload_uds_bills')

        except Exception as e:
            messages.error(request, f"An error occurred while processing the file: {str(e)}")
            return redirect('upload_uds_bills')

    return render(request, 'product/upload.html')







@login_required
def upload_uds_bills_inner(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']
        try:
            decoded_file = csv_file.read().decode('utf-8-sig').splitlines()
            reader = csv.DictReader(decoded_file, delimiter=';')  # Change delimiter to ';' for semicolon-separated values

            required_fields = ['uds_bill', 'main_product', 'amount', 'price']

            headers = reader.fieldnames
            if not all(field in headers for field in required_fields):
                missing_fields = [field for field in required_fields if field not in headers]
                messages.error(request, f"CSV file is missing required fields: {', '.join(missing_fields)}.")
                return redirect('upload_uds_bills_inner')

            for row in reader:
                if not all(field in row for field in required_fields):
                    messages.error(request, "CSV file is missing one or more required fields in a row.")
                    return redirect('upload_uds_bills_inner')

                uds_bill_id = int(row['uds_bill'])
                main_product_id = int(row['main_product'])
                amount = int(row['amount'])
                price = float(row['price'].replace(',', '.'))

                try:
                    uds_bill = UdsBills.objects.get(pk=uds_bill_id)
                    main_product = MainProduct.objects.get(pk=main_product_id)
                except UdsBills.DoesNotExist:
                    messages.error(request, f"UdsBill with id {uds_bill_id} does not exist.")
                    continue
                except MainProduct.DoesNotExist:
                    messages.error(request, f"MainProduct with id {main_product_id} does not exist.")
                    continue

                UdsBill_inner.objects.create(
                    created_by=request.user,
                    uds_bill=uds_bill,
                    main_product=main_product,
                    amount=amount,
                    price=price
                )

            messages.success(request, "UdsBill_inner uploaded successfully")
            return redirect('upload_uds_bills_inner')

        except Exception as e:
            messages.error(request, f"An error occurred while processing the file: {e}")
            return redirect('upload_uds_bills_inner')

    return render(request, 'product/upload.html')





def fetch_bills_list_usd(request):

   

    # Fetch all UdsBills objects for the given customer
    bills = UdsBills.objects.filter(created_by=request.user.id).order_by('-created_at')
    
    return render(request, 'uds_biles/list.html', {'form': bills})






def view_bill(request ,id):

   


    

    # Fetch all UdsBills objects for the given customer

    bills = UdsBills.objects.filter(pk=id ,)
    bill_instance = get_object_or_404(UdsBills,pk=id )
    user_id = bill_instance.created_by.id
    records = UdsBill_inner.objects.filter(uds_bill= id)



    user = CustomUser.objects.filter(pk =user_id)








      
    return render(request, 'uds_inner/view.html', {'form': bills , 'form_in' :records  ,  'user' : user})





def testt(request):
    return render(request, 'uds_inner/view.html')
