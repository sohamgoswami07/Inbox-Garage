from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
import os

# Create your views here.
# def user_login(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         if not User.objects.filter(username = username).exists:
#             messages.error(request, "Invalid username!")
#             return redirect('login')
        
#         user = authenticate(username = username, password = password)
#         if user is None:
#             messages.error(request, "Invalid password!")
#             return redirect('login')
            
#         else:
#             login(request, user)
#             return redirect('home')

#     return render(request, 'login/login.html')

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
    email = get_object_or_404(EmailDetail, id=id)

    email_content = ""
    email_image = None

    if email.email_body:
        file_path = email.email_body.path # Get the file path
        file_extension = os.path.splitext(file_path)[1].lower()  # Get file extension

        if file_extension in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"]:
            # If the file is an image, pass its URL to the template
            email_image = email.email_body.url  # URL to be used in frontend
        elif file_extension in [".html", ".htm"]:
            # If the file is an HTML file, read its content
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    email_content = file.read()
            except Exception as e:
                print(f"Error reading file: {e}")

    return render(request, "email_detail/email_detail.html", {"email": email, "email_content": email_content, "email_image": email_image})

def blog_detail(request, id):
    blog = get_object_or_404(BlogDetail, id = id)
    
    blog_content = ""
    file_path  = blog.blog_body.path # Get the file path
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            blog_content = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
    
    return render(request, 'blog_detail/blog_detail.html', {'blog_content': blog_content})

def brand_detail(request, id):
    brand = get_object_or_404(BrandDetail, id = id)
    email_list = EmailDetail.objects.all().filter(connected_brand = id)

    return render(request, 'brand_detail/brand_detail.html', {'brand': brand, 'email_list': email_list})
