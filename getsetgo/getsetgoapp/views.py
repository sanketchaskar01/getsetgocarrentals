import json
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404   
from .models import VehicleCategory,Vehicle,Booking
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
import razorpay,re
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import JsonResponse,HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ValidationError
# Create your views here.

def home(request):
    return render(request,'home.html')

def signup(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if not re.match("^[a-zA-Z]+$", username):
            error_message = "Username must contain only alphabetic characters."
    
        elif password1 != password2:
            error_message = "Passwords do not match."

        elif User.objects.filter(username=username).exists():
            error_message = "Username already exists."
        
        elif User.objects.filter(email=email).exists():
            error_message = "Email already exists."

        if not error_message:
            try:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                return redirect('login')  
            except ValidationError as e:
                error_message = str(e)
    
    return render(request, 'signup.html', {'error_message': error_message})

def vehicle_list(request):
    vl=Vehicle.objects.all()
    context={'vl':vl}
    return render(request,'rides.html',context)

def bookingform(request):
    return render(request,'booking.html')


def booking(request):
    if request.method == 'POST':
        uid = request.session.get('uid')
        user = User.objects.get(id=uid)

        contact = request.POST.get('contact')
        email = request.POST.get('email')
        vehicle_id = request.POST.get('vehicle_id') 
        trip_date = request.POST.get('trip_date')
        return_date = request.POST.get('return_date')
        vehicle = Vehicle.objects.get(id=vehicle_id)

        if contact and email and vehicle and trip_date and return_date:
            booking = Booking(
                user=user,
                contact=contact,
                email=email,
                vehicle=vehicle,
                trip_date=trip_date,
                return_date=return_date
            )
            booking.save()
            return redirect('payment', booking_id=booking.id)
        else:
            return HttpResponse('All fields are required.', status=400)

    return render(request, 'booking.html')


def login_view(request):
    login_error = None
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Validate Username
        if not username:
            login_error = "Username cannot be empty."
        elif not re.match("^[a-zA-Z]+$", username):
            login_error = "Username must only contain alphabetic characters without numbers."

        # Proceed if there's no error
        if not login_error:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Use login function after authentication
                return redirect('home')
            else:
                login_error = "Invalid credentials. Please try again."
    
    return render(request, 'login.html', {'login_error': login_error})
    

def logout_view(request):
    logout(request)
    return redirect('/')


def booking_form(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    return render(request, 'booking.html', {'vehicle': vehicle})


def vehicle_list(request):
    category_name = request.GET.get('category')
    search_query = request.GET.get('search', '')
    vehicles = Vehicle.objects.all()
    if category_name:
        vehicles = vehicles.filter(v_category__name=category_name)
    if search_query:
        vehicles = vehicles.filter(v_name__icontains=search_query)
    categories = VehicleCategory.objects.all()
    return render(request, 'rides.html', {
        'vl': vehicles,
        'categories': categories
    })


def create_order(request):
    if request.method == 'POST':
        user = request.user  
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        vehicle_id = request.POST.get('vehicle_id')
        trip_date = request.POST.get('trip_date')
        return_date = request.POST.get('return_date')
        vehicle = Vehicle.objects.get(id=vehicle_id)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        order_amount = 300000  
        order_currency = 'INR'
        order_receipt = 'receipt#1'
        order = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt))

        order_id = order['id']

        booking = Booking.objects.create(
            user=user,
            contact=contact,
            email=email,
            vehicle=vehicle,
            trip_date=trip_date,
            return_date=return_date,
            is_paid=False,
            payment_id=order_id 
        )
        return render(request, 'payment.html', {'order_id': order_id, 'amount': order_amount})

    return redirect('booking_form') 



@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        payment_id = data.get('razorpay_payment_id')
        order_id = data.get('razorpay_order_id')
        signature = data.get('razorpay_signature')
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)})

    return render(request, 'payment_success.html')


def payment_callback(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    payment_id = request.POST.get('payment_id') 
    booking.is_paid = True
    booking.payment_id = payment_id
    booking.save()
    return HttpResponseRedirect(reverse('payment_success'))  

def user_rides(request):
    if request.user.is_authenticated:
        user_bookings = Booking.objects.filter(user=request.user)
        return render(request, 'your_rides.html', {'bookings': user_bookings})
    else:
        return redirect('login')
