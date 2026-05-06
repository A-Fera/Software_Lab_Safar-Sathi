from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Itinerary, ItineraryItem
from .forms import ItineraryForm, ItineraryItemForm

@login_required
def itinerary_list_view(request):
    itineraries = Itinerary.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'itinerary/itinerary_list.html', {'itineraries': itineraries})

@login_required
def itinerary_detail_view(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk, user=request.user)
    return render(request, 'itinerary/itinerary_detail.html', {'itinerary': itinerary})

@login_required
def itinerary_create_view(request):
    if request.method == 'POST':
        form = ItineraryForm(request.POST)
        if form.is_valid():
            itin = form.save(commit=False)
            itin.user = request.user
            itin.save()
            messages.success(request, 'Itinerary created!')
            return redirect('itinerary:itinerary_detail', pk=itin.pk)
    else:
        form = ItineraryForm()
    return render(request, 'itinerary/itinerary_form.html', {'form': form})

@login_required
def itinerary_update_view(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ItineraryForm(request.POST, instance=itinerary)
        if form.is_valid():
            form.save()
            messages.success(request, 'Itinerary updated!')
            return redirect('itinerary:itinerary_detail', pk=itinerary.pk)
    else:
        form = ItineraryForm(instance=itinerary)
    return render(request, 'itinerary/itinerary_form.html', {'form': form, 'itinerary': itinerary})

@login_required
def itinerary_delete_view(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk, user=request.user)
    if request.method == 'POST':
        itinerary.delete()
        messages.success(request, 'Itinerary deleted.')
        return redirect('itinerary:itinerary_list')
    return render(request, 'itinerary/itinerary_confirm_delete.html', {'itinerary': itinerary})

@login_required
def item_create_view(request, itinerary_pk):
    itinerary = get_object_or_404(Itinerary, pk=itinerary_pk, user=request.user)
    if request.method == 'POST':
        form = ItineraryItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.itinerary = itinerary
            item.save()
            messages.success(request, 'Activity added!')
            return redirect('itinerary:itinerary_detail', pk=itinerary.pk)
    else:
        form = ItineraryItemForm()
    return render(request, 'itinerary/item_form.html', {'form': form, 'itinerary_pk': itinerary_pk})

@login_required
def item_update_view(request, itinerary_pk, item_pk):
    itinerary = get_object_or_404(Itinerary, pk=itinerary_pk, user=request.user)
    item = get_object_or_404(ItineraryItem, pk=item_pk, itinerary=itinerary)
    if request.method == 'POST':
        form = ItineraryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Activity updated!')
            return redirect('itinerary:itinerary_detail', pk=itinerary.pk)
    else:
        form = ItineraryItemForm(instance=item)
    return render(request, 'itinerary/item_form.html', {'form': form, 'item': item, 'itinerary_pk': itinerary_pk})

@login_required
def item_delete_view(request, itinerary_pk, item_pk):
    itinerary = get_object_or_404(Itinerary, pk=itinerary_pk, user=request.user)
    item = get_object_or_404(ItineraryItem, pk=item_pk, itinerary=itinerary)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Activity removed.')
        return redirect('itinerary:itinerary_detail', pk=itinerary.pk)
    return render(request, 'itinerary/item_confirm_delete.html', {'item': item, 'itinerary': itinerary})
