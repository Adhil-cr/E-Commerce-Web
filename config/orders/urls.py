from django.urls import path
from . import views

urlpatterns = [
    path('cart/',views.cart,name='cart'),
    path('add/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('remove/<int:item_id>/',views.remove_from_cart,name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/',views.place_order, name='place_order'),
    path('success/', views.order_success, name='order_success'),
    path('my-orders/',views.my_orders,name="my_orders"),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),


    
    # Quantity update routes
    path('increase/<int:item_id>',views.increase_quantity,name='increase_quantity'),
    path('decrease/<int:item_id>',views.decrease_quantity,name='decrease_quantity')

]