import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, CartItem

def product_list(request):
	products = Product.objects.all()
	return render(request, 'cart/index.html', {'products': products})

def view_cart(request):
	if request.user.is_authenticated:
		cart_items = CartItem.objects.filter(user=request.user)
		total_price = sum(item.product.price * item.quantity for item in cart_items)
		total_price=int(total_price)
		return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_price': total_price})
	else:
		return redirect('cart:home')

def add_to_cart(request, product_id):
	if request.user.is_authenticated:
		product = Product.objects.get(id=product_id)
		cart_item, created = CartItem.objects.get_or_create(product=product, 
                                                        user=request.user)
		cart_item.quantity += 1
		cart_item.save()
		return redirect('cart:view_cart')
	else:
		return redirect('cart:home')

def remove_from_cart(request, item_id):
	if request.user.is_authenticated:
		cart_item = CartItem.objects.get(id=item_id,user=request.user)
		cart_item.delete()
		return redirect('cart:view_cart')
	else:
		return redirect('cart:home')


def home(request):
	return HttpResponse('Please login yourself')


def initiate_payment(request):
    if request.method == "POST":
        amount = int(request.POST["amount"]) * 100  # Amount in paise

        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        payment_data = {
            "amount": amount,
            "currency": "INR",
            "receipt": "order_receipt",
            "notes": {
                "email": "user_email@example.com",
            },
        }

        order = client.order.create(data=payment_data)
        
        # Include key, name, description, and image in the JSON response
        response_data = {
            "id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "key": settings.RAZORPAY_API_KEY,
            "name": "My Company",
            "description": "Payment for Your Product",
            "image": "https://yourwebsite.com/logo.png",  # Replace with your logo URL
        }
        
        return JsonResponse(response_data)
    return redirect('cart:cart.html')
	


def payment_success(request):
    return render(request, "cart/payment_success.html")

def payment_failed(request):
    return render(request, "cart/payment_failed.html")
