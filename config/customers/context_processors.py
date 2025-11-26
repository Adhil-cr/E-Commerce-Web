from .models import Customer

def customer_info(request):
    if request.user.is_authenticated:
        try :
            customer = Customer.objects.get(user=request.user)
            return {'customer':customer}
        except Customer.DoesNotExist:
            return {'customer':None}
        
    return {'customer':None}