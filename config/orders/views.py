from django.shortcuts import render , redirect , get_object_or_404
from .models import Order , OrderedItem
from products.models import Product
from django.contrib import messages
from decimal import Decimal
from django.db import transaction

# Fetching logged users Active cart ( )
def cart(request):
    if not request.user.is_authenticated:
        messages.info(request, "Please login to view your cart.")
        return redirect('login')
    
    elif request.user.is_staff:
        messages.error(request, "Admin cannot access cart.")
        return redirect('home')


    customer = request.user.customer_profile

    order, created = Order.objects.get_or_create(
        owner=customer,
        order_status=0  # CART_STAGE
    )

    items = OrderedItem.objects.filter(owner=order).select_related('product')

    total = Decimal('0.00')

    # Add per-item total_price dynamically
    for item in items:
        item.total_price = (item.product.price or Decimal('0')) * item.quantity
        total += item.total_price

    return render(request, 'orders/cart.html', {
        'items': items,
        'total': total
    })

# Adding product to logged users cart
@transaction.atomic
def add_to_cart(request,product_id):
    if not request.user.is_authenticated:
        messages.info(request, "Please login to add items to cart.")
        return redirect('login')
    
    elif request.user.is_staff:
        messages.error(request, "Admin cannot access cart.")
        return redirect('home')
    
    # get the customer and the product
    customer = request.user.customer_profile
    product = get_object_or_404(Product,id=product_id, delete_status=1)

    # get or create an active cart (CART_STAGE
    order, _created = Order.objects.get_or_create(owner=customer,order_status=0)

    # get or create the item;if existing increment quantity
    item,  created = OrderedItem.objects.get_or_create(owner=order, product=product,defaults={'quantity':1})
    if not created :
        item.quantity += 1
        item.save(update_fields=['quantity'])

    messages.success(request, "Item added to cart!")
    return redirect('cart')

# Removing item from the cart 
def remove_from_cart(request,item_id):
    if not request.user.is_authenticated:
        messages.info(request,'Please login')
        return redirect('login')
    
    elif request.user.is_staff:
        messages.error(request, "Admin cannot access cart.")
        return redirect('home')
    
    item = get_object_or_404(OrderedItem,id=item_id)

    # verify the item belongs to the loged-in user's order
    if item.owner.owner != request.user.customer_profile:
        messages.error(request," Permission denied")
        return redirect('cart')
    
    item.delete()
    messages.success(request,"Item remove from the cart")
    return redirect('cart')

# + button in in ( Quantity increment )
def increase_quantity(request,item_id):
    item = get_object_or_404(OrderedItem,id=item_id)

    item.quantity += 1
    item.save()

    messages.success(request,"Quantity updated")
    return redirect('cart')

# - button in in ( Quantity decrement )
def decrease_quantity(request,item_id):
    item = get_object_or_404(OrderedItem,id=item_id)

    if item.quantity == 1:
        item.delete()
        messages.success(request,'Item removed from the cart.')
    else:
        item.quantity -= 1
        item.save()
        messages.error(request,'Quantity updated')

    return redirect('cart')

# cart stage to checkout stage
def checkout(request):
    # Checking the user is logged or not 
    if not request.user.is_authenticated:
        messages.info(request,"Please login to checkout.")
        return redirect('login')
    
    elif request.user.is_staff:
        messages.error(request, "Admin cannot access cart.")
        return redirect('home')
    
    # logged user profile
    customer = request.user.customer_profile

    # logged users active cart
    active_cart = Order.objects.filter(owner=customer,order_status=0).first()

    # Checking the cart is empty 
    if not active_cart:
        messages.error(request,"Your cart is empty.")
        return redirect('cart')
    
    # Gets all the products inside the active cart
    items = OrderedItem.objects.filter(owner=active_cart).select_related('product')


    total = Decimal('0.00')
    for item in items:
        item.total_price = item.product.price * item.quantity
        total += item.total_price

    return render(request,'orders/checkout.html',{
        'active_cart':active_cart,
        'items':items,
        'total':total
    })

# Placing the order 
def place_order(request):
    # Checking the user is logged or not 
    if not request.user.is_authenticated:
        messages.info(request, "Please login.")
        return redirect('login')
    
    elif request.user.is_staff:
        messages.error(request, "Admin cannot access cart.")
        return redirect('home')

    customer = request.user.customer_profile

    order = Order.objects.filter(owner=customer, order_status=0).first()

    if not order:
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    # Change order status
    order.order_status = 1   # ORDER_CONFIRMED
    order.save()

    messages.success(request, "Order placed successfully!")
    return redirect('order_success')

# Redirect to order success full page
def order_success(request):
    return render(request,'orders/order_success.html')


# Fetching logged user orders
def my_orders(request):
    # Checking the user is logged or not 
    if not request.user.is_authenticated:
        messages.info(request,"Please login to view your orders.")
        return redirect('login')
    
    # fetching logged your profile
    customer = request.user.customer_profile

     # fetch only confirmed/processed/delivered orders
    orders = Order.objects.filter(
        owner=customer,
        order_status__gte=1   # 1:confirmed, 2:processed, 3:delivered
    ).order_by('-created_at')

    return render(request,'orders/my_orders.html',{
        'orders':orders
    })

# Order Detail Page ( users can click ordered products details )
def order_detail(request,order_id):
    
    # Authenticating 
    if not request.user.is_authenticated:
        messages.info(request,'Please login to continue.')
        return redirect('login')
    
    # Fetching logged users details
    customer = request.user.customer_profile

    # Fetch the order 
    order = get_object_or_404(Order,id=order_id, owner=customer)

    # Fetch items inside the order
    items = OrderedItem.objects.filter(owner=order).select_related('product')

    # Calculate total price
    total = sum(item.product.price * item.quantity for item in items)

    return render(request,'orders/order_detail.html',{
        'order':order,
        'items':items,
        'total':total
    })


# Admin order list view
def admin_orders(request):
    # Admin Authentication
    if not request.user.is_staff:
        messages.error(request,"Access denied.")
        return redirect('home')
    
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        new_status = int(request.POST.get("status"))
        order = get_object_or_404(Order,id=order_id)
        order.order_status = new_status
        order.save()
        messages.success(request,f"Order {order_id} Updated successfully!")

    
    # Fetch all orders except cart
    orders = Order.objects.filter(order_status__gte=1).order_by('-created_at')

    return render(request,'orders/admin_orders.html',{
        'orders':orders
    })


# # Admin Order status control 
# def admin_update_order(request,order_id):
#     # Admin Authentication
#     if not request.user.is_staff:
#         messages.error(request,"Access denied")
#         return redirect('home')
    
#     # fetching the order detials corresponding id
#     order = get_object_or_404(Order,id=order_id)

#     if request.method == "POST":
#         new_status = int(request.POST.get("status"))
#         order.order_status = new_status
#         order.save()

#         messages.success(request,'Order status updated!')
#         return redirect('admin_orders')
    
#     return render(request,'orders/admin_update_order.html',{
#         'order':order   
#     })

