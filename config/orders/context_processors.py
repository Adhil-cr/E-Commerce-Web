from orders.models import Order, OrderedItem

def cart_item_count(request):
    if request.user.is_authenticated:
        customer = request.user.customer_profile

        order = Order.objects.filter(owner=customer, order_status=0).first()

        if order:
            return {'cart_count': OrderedItem.objects.filter(owner=order).count()}
    
    return {'cart_count': 0}
