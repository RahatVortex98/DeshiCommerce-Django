from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove-from-cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('delete-cart-item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/<str:order_number>/', views.checkout, name='checkout'),

]
