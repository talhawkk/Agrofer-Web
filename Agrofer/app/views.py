# app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings  # Correct import for settings
from .models import Product, BlogPost, ContactSubmission

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html')

def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def process(request):
    return render(request, 'process.html')

def aim(request):
    return render(request, 'aim.html')

def blog(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog.html', {'posts': posts})

def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    # Fetch related posts (same category, excluding current post)
    related_posts = BlogPost.objects.filter(category=post.category).exclude(id=post.id)[:2]
    return render(request, 'blog_detail.html', {'post': post, 'related_posts': related_posts})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Basic validation
        if not name or not email or not message:
            messages.error(request, 'Please fill out all fields.')
            return redirect('contact')

        # Prepare email content
        subject = f"New Contact Form Submission from {name}"
        email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        # print(email_message)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['agrofer.info@gmail.com']  # Tumhara email address

        try:
            # Send email
            send_mail(
                subject,
                email_message,
                from_email,
                recipient_list,
                fail_silently=False,
            )
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
        except Exception as e:
            messages.error(request, f'Error sending message: {str(e)}. Please try again later.')

        return redirect('contact')

    return render(request, 'contact.html')