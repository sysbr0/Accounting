# customers/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from users.models import CustomUser
from .models import Costomers
from .forms import CostomersForm
from biles.models import ProductHam , Package , Jar ,MainProduct  , ProductHam  , UdsBills  , UdsBill_inner


def customer_login(request):
    if request.method == 'POST':
        customer_id = request.POST['customer_id']
        token = request.POST['token']
        try:
            customer = Costomers.objects.get(id=customer_id, token=token)
            # You may need to handle authentication logic here
            # For simplicity, we just set a session variable
            request.session['customer_id'] = customer.id
            return redirect('customer_panel')
        except Costomers.DoesNotExist:
            messages.error(request, 'Invalid customer ID or token')
            return redirect('customer_login')
    return render(request, 'customers/login.html')

def customer_panel(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('customer_login')
    customer = get_object_or_404(Costomers, id=customer_id)
    return render(request, 'customers/panel.html', {'customer': customer})



def customer_logout(request):
    try:
        del request.session['customer_id']
    except KeyError:
        pass
    return redirect('customer_login')




def update_cosomer(request):
    customer_id = request.session.get('customer_id')
    costomer = get_object_or_404(Costomers, pk=customer_id)
    
    if request.method == 'POST':
        form = CostomersForm(request.POST, instance=costomer)
        if form.is_valid():
            form.save()
            return redirect('customer_panel')  # Redirect to client detail page
    else:
        form = CostomersForm(instance=costomer)
    
    return render(request, 'customers/edit.html', {'form': form})


def fetch_bills_list(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        bills = "no biles"
        # Handle the case where customer_id is not in the session
        

    # Fetch all UdsBills objects for the given customer
    bills = UdsBills.objects.filter(customer_id=customer_id).order_by('-created_at')
    
    return render(request, 'customers/bills.html', {'form': bills})



def view_bill(request ,id):

   

    customer_id = request.session.get('customer_id')
    costomer = Costomers.objects.filter(pk=customer_id)


    if not customer_id:
        bills = "no biles"
        # Handle the case where customer_id is not in the session
        

    # Fetch all UdsBills objects for the given customer

    bills = UdsBills.objects.filter(pk=id ,customer_id=customer_id )
    bill_instance = get_object_or_404(UdsBills,pk=id ,customer_id=customer_id)
    user_id = bill_instance.created_by.id
    records = UdsBill_inner.objects.filter(uds_bill= id)



    user = CustomUser.objects.filter(pk =user_id)








      
    return render(request, 'customers/index.html', {'form': bills , 'form_in' :records  , 'costomer':costomer , 'user' : user})





def testt(request):
    return render(request, 'customers/index.html')
