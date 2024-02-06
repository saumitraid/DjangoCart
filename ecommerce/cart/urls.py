from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
	path('', views.product_list, name='product_list'),
	path('home', views.home, name='home'),
	path('cart', views.view_cart, name='view_cart'),
	path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
	path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path("initiate-payment/", views.initiate_payment, name="initiate_payment"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("payment-failed/", views.payment_failed, name="payment_failed"),
]
