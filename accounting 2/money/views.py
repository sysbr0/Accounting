from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import MoneySource , GeneralPayment
from .forms import MoneySourceForm

# List View
def money_source_list(request):
    moneysources = MoneySource.objects.all()
    return render(request, 'money/list.html', {'moneysources': moneysources})

# Create View
def money_source_create(request):
    if request.method == 'POST':
        form = MoneySourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('moneysource_list'))
    else:
        form = MoneySourceForm()
    return render(request, 'money/add.html', {'form': form})

# Update View
def money_source_update(request, pk):
    moneysource = get_object_or_404(MoneySource, pk=pk)
    if request.method == 'POST':
        form = MoneySourceForm(request.POST, instance=moneysource)
        if form.is_valid():
            form.save()
            return redirect(reverse('moneysource_list'))
    else:
        form = MoneySourceForm(instance=moneysource)
    return render(request, 'money/edit.html', {'form': form})

# Delete View
def money_source_delete(request, pk):
    moneysource = get_object_or_404(MoneySource, pk=pk)
    if request.method == 'POST':
        moneysource.delete()
        return redirect(reverse('moneysource_list'))
    return render(request, 'money/delete.html', {'object': moneysource})



def genaral_pyment_list(request):
    GeneralPayments = GeneralPayment.objects.all()
    return render(request, 'pyment/list.html', {'GeneralPayment': GeneralPayments})