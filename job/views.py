from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password , check_password
from .models import *
import razorpay
from django.conf import settings
import razorpay




def index(request):
    return render(request, 'index.html')
# Create your views here.



def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        photo = request.FILES.get("photo")

        # Basic validation
        if not all([first_name, last_name, email, password, photo]):
            messages.error(request, "All fields are required.")
            return render(request, 'register.html')

        if RegisterModel.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'register.html')

        hashed_password = make_password(password)

        # Save user
        RegisterModel.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            photo=photo
        )

        messages.success(request, "Registration successful.")
        return redirect('login')  # or any success page

    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return render(request, 'login.html')

        try:
            user = RegisterModel.objects.get(email=email)
            if check_password(password, user.password):
                # Instead of storing session, render a response directly
                return render(request, 'welcome.html', {
                    'user': user  # pass user data to template
                })
            else:
                messages.error(request, "Incorrect password.")
        except RegisterModel.DoesNotExist:
            messages.error(request, "User does not exist.")

    return render(request, 'login.html')

def logout_view(request):
    
    messages.success(request, "Logged out.")
    return redirect('login')



def welcome(request):
    jobs = Job.objects.order_by('-posted_at')  # Show latest jobs first
    return render(request, 'welcome.html', {'jobs': jobs})


def post_job(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        company = request.POST.get("company")
        location = request.POST.get("location")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        if not all([title, description, company, location]):
            messages.error(request, "Title, description, company, and location are required.")
            return render(request, "post_job.html")

        Job.objects.create(
            title=title,
            description=description,
            company=company,
            location=location,
            email=email,
            phone=phone,
        )

        messages.success(request, "Job posted successfully!")
        return redirect("post_job")

    return render(request, "postjob.html")

def course(request):
    return render(request, 'course.html')


# payment

import json
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@csrf_exempt
def create_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        course = data.get('course')
        
        # Convert $500 USD to INR (example: 1 USD = 82 INR approx)
        amount_in_inr = 500 * 82 * 100  # amount in paise
        
        order = client.order.create({
            "amount": amount_in_inr,
            "currency": "INR",
            "payment_capture": '1'
        })
        return JsonResponse({
            "order_id": order['id'],
            "amount": amount_in_inr,
            "currency": "INR",
            "course": course,
            "key": settings.RAZORPAY_KEY_ID
        })
