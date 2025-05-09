from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
import os
import requests
from docx import Document
from io import BytesIO

def home(request): 
    # Get filter parameters from the request
    selected_category = request.GET.get('category', None)
    selected_type = request.GET.get('type', None)

    # Base queryset for all emails (unfiltered)
    email_list = EmailDetail.objects.all().order_by('-id')

    # Filter based on category if selected
    if selected_category and selected_type:
        # Filter for both category and type when both are selected
        email_list = email_list.filter(email_category=selected_category, email_type=selected_type).order_by('-id')
    elif selected_category:
        # Filter only by category if only category is selected
        email_list = email_list.filter(email_category=selected_category).order_by('-id')
    elif selected_type:
        # Filter only by type if only type is selected
        email_list = email_list.filter(email_type=selected_type).order_by('-id')

    # Get the distinct categories and types for the filter buttons
    categories = EmailDetail.objects.values_list('email_category', flat=True).distinct()
    types = EmailDetail.objects.values_list('email_type', flat=True).distinct()

    # Paginator
    paginator = Paginator(email_list, 20)  # 20 items per page
    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)

    # Pass page_obj, categories, and types to the template for rendering
    return render(request, 'home/home.html', {
        'page_obj': page_obj,
        'selected_category': selected_category,
        'selected_type': selected_type,
        'categories': categories,
        'types': types
    })

def brand(request):
    selected_type = request.GET.get('type', None)

    # Get the distinct categories and types for the filter buttons
    brand_type = BrandDetail.objects.values_list('brand_type', flat=True).distinct()

    brand_list = BrandDetail.objects.filter(brand_type=selected_type).order_by('-id') if selected_type else BrandDetail.objects.all().order_by('-id') # fetch all emails

    # Paginator
    paginator = Paginator(brand_list, 20)  # 20 items per page
    page_number = request.GET.get('page') # Get the current page number
    page_obj = paginator.get_page(page_number)

    # Pass page_obj to the template for rendering
    return render(request, 'brand/brand.html', {'brand_list': brand_list, 'brand_type': brand_type, 'selected_type': selected_type, 'page_obj': page_obj})

def templates(request):
    templates_list = TemplatesDetail.objects.all().order_by('-id') # fetch all emails

    # Paginator
    paginator = Paginator(templates_list, 20)  # 20 items per page

    page_number = request.GET.get('page') # Get the current page number
    page_obj = paginator.get_page(page_number)

    # Pass page_obj to the template for rendering
    return render(request, 'templates/templates.html', {'templates_list': templates_list, 'page_obj': page_obj})

def email_detail(request, id):
    email = get_object_or_404(EmailDetail, id = id)

    return render(request, "email_detail/email_detail.html", {"email": email})

def brand_detail(request, id):
    brand = get_object_or_404(BrandDetail, id = id)
    email_list = EmailDetail.objects.all().filter(connected_brand = id)

    return render(request, 'brand_detail/brand_detail.html', {'brand': brand, 'email_list': email_list})
