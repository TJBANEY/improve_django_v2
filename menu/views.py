from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils import timezone
from operator import attrgetter
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *


def menu_list(request):
    all_menus = Menu.objects.prefetch_related('items').filter(
        expiration_date__gte=timezone.now()).order_by('expiration_date')

    return render(request, 'menu/list_all_current_menus.html', {'menus': all_menus})

def menu_detail(request, pk):
    menu = get_object_or_404(Menu, pk=pk)

    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)

    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_date = timezone.now()
            menu.save()
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm()
    return render(request, 'menu/menu_edit.html', {'form': form})


def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)

    items = Item.objects.all()

    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save()

    return render(request, 'menu/change_menu.html', {
        'menu': menu,
        'items': items,
    })