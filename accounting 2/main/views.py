


# Create your views here.
# views.py 
from django.shortcuts import render, redirect , get_object_or_404
from .forms import ClintsForm
from .models import clints
from django.contrib import messages
from django.http import HttpResponse
from django.utils.encoding import smart_str  # Import smart_str for encoding



import csv

def add_clint(request):
    if request.method == 'POST':
        form = ClintsForm(request.POST)
        if form.is_valid():
            form.save()
              # Redirect to a list of clients or another page
    else:
        form = ClintsForm()
    return render(request, 'clint/Add_clint.html', {'form': form})




def test(request):

    x = " willcpome to my site "
    return render(request, 'test/test.html' , {'x' : x})





def clint_list(request):
    clints_list = clints.objects.filter(created_by=request.user.id)
    return render(request, 'clint/clint_list.html', {'clints': clints_list})



def fatch_clint(request , id):

    clint = clints.objects.get(pk=id)

    return render(request, 'clint/fatch_clint.html', {'clint': clint})


def delete_clint(request, id):
    clints_list = clints.objects.filter(created_by=request.user.id)
    clint = get_object_or_404(clints, pk=id)
    if request.method == 'POST':
        clint.delete()
        messages.success(request, 'Client deleted successfully.')
        return redirect('clint_list')
    return render(request, 'clint/fatch_clint.html', {'clint': clint })


def update_clint(request, id):
    clint = get_object_or_404(clints, pk=id , created_by=request.user.id)
    
    if request.method == 'POST':
        form = ClintsForm(request.POST, instance=clint)
        if form.is_valid():
            form.save()
            return redirect('fatch_clint', id=id)  # Redirect to client detail page
    else:
        form = ClintsForm(instance=clint)
    
    return render(request, 'clint/update_clint.html', {'form': form})


# views.py


def upload_clients(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file, delimiter=';')

        for row in reader:
            client, created = clints.objects.get_or_create(
                clint_name=row['clint_name'],
                defaults={
                    'clint_tex': row['tax_no'] if row['tax_no'] else None,
                    'clint_email': row['email'],
                    'c_number': row['c_number'],
                    'c_sorce': row['c_srorse'],
                    'clint_iban': row['c_iban'] if row['c_iban'] else None,
                    'is_company': row['companyORnot'].strip().lower() == 'true',
                    'clint_tr_name': row['c_tr_name'],
                    'image': row['img'] if row['img'] else None,
                }
            )
            if not created:
                # Update only the empty fields of the existing client
                if not client.clint_tex and row['tax_no']:
                    client.clint_tex = row['tax_no']
                if not client.clint_email and row['email']:
                    client.clint_email = row['email']
                if not client.c_number and row['c_number']:
                    client.c_number = row['c_number']
                if not client.c_sorce and row['c_srorse']:
                    client.c_sorce = row['c_srorse']
                if not client.clint_iban and row['c_iban']:
                    client.clint_iban = row['c_iban']
                if not client.clint_tr_name and row['c_tr_name']:
                    client.clint_tr_name = row['c_tr_name']
                if not client.image and row['img']:
                    client.image = row['img']
                client.is_company = row['companyORnot'].strip().lower() == 'true'
                client.save()

        messages.success(request, "Clients uploaded successfully")
        return redirect('upload_clients')

    return render(request, 'clint/upload_clients.html')


def download_clints_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="clints.csv"'

    writer = csv.writer(response)
    writer.writerow([
        smart_str('ID'),
        smart_str('Name'),
        smart_str('Email'),
        smart_str('Contact Number'),
        smart_str('Source'),
        smart_str('Is Company'),
        smart_str('IBAN'),
        smart_str('Image'),
    ])

    clints_list = clints.objects.all()
    for clint in clints_list:
        writer.writerow([
            clint.id,
            smart_str(clint.clint_name),
            smart_str(clint.clint_email),
            smart_str(clint.c_number),
            smart_str(clint.c_sorce),
            clint.is_company,
            smart_str(clint.clint_iban),
            smart_str(clint.image if clint.image else ''),
        ])

    return response