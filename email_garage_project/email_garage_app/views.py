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

    # Fetch all emails
    email_list = EmailDetail.objects.all().order_by('id')

    # Filter based on category if selected
    if selected_category:
        email_list = email_list.filter(email_category=selected_category)

    # Filter based on type if selected
    if selected_type:
        email_list = email_list.filter(email_type=selected_type)

    # Get the distinct categories and types for the filter buttons
    categories = email_list.values_list('email_category', flat=True).distinct()
    types = email_list.values_list('email_type', flat=True).distinct()

    # Paginator
    paginator = Paginator(email_list, 20)  # 20 items per page
    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)

    # Pass page_obj, categories, and types to the template for rendering
    return render(request, 'home/home.html', {'page_obj': page_obj, 'selected_category': selected_category, 'selected_type': selected_type, 'categories': categories, 'types': types})

def brand(request):
    brand_list = BrandDetail.objects.all().order_by('id') # fetch all emails

    # Paginator
    paginator = Paginator(brand_list, 20)  # 20 items per page

    page_number = request.GET.get('page') # Get the current page number
    page_obj = paginator.get_page(page_number)

    # Pass page_obj to the template for rendering
    return render(request, 'brand/brand.html', {'brand_list': brand_list, 'page_obj': page_obj})

def templates(request):
    templates_list = TemplatesDetail.objects.all().order_by('id') # fetch all emails

    # Paginator
    paginator = Paginator(templates_list, 20)  # 20 items per page

    page_number = request.GET.get('page') # Get the current page number
    page_obj = paginator.get_page(page_number)

    # Pass page_obj to the template for rendering
    return render(request, 'templates/templates.html', {'templates_list': templates_list, 'page_obj': page_obj})

def blogs(request):
    blogs_list = BlogDetail.objects.all().order_by('id') # fetch all emails

    # Paginator
    paginator = Paginator(blogs_list, 20)  # 20 items per page

    page_number = request.GET.get('page') # Get the current page number
    page_obj = paginator.get_page(page_number)

    # Pass page_obj to the template for rendering
    return render(request, 'blogs/blogs.html', {'blogs_list': blogs_list, 'page_obj': page_obj})

def email_detail(request, id):
    email = get_object_or_404(EmailDetail, id = id)

    return render(request, "email_detail/email_detail.html", {"email": email})

def blog_detail(request, id):
    blog = get_object_or_404(BlogDetail, id = id)
    
    blog_content = ""
    docx_url = blog.blog_body.url  # Get Cloudinary file path
    
    # try:
    #     response = requests.get(docx_url)
    #     response.raise_for_status()

    #     docx_file = BytesIO(response.content)
    #     doc = Document(docx_file)

    #     # Extract text content from the docx file
    #     blog_content = "\n".join([para.text for para in doc.paragraphs])

    # except Exception as e:
    #     print(f"Error fetching or reading DOCX file: {e}")
    #     blog_content = "Unable to load blog content."

    return render(request, 'blog_detail/blog_detail.html', {'docx_url': docx_url})

def brand_detail(request, id):
    brand = get_object_or_404(BrandDetail, id = id)
    email_list = EmailDetail.objects.all().filter(connected_brand = id)

    return render(request, 'brand_detail/brand_detail.html', {'brand': brand, 'email_list': email_list})
