from django.shortcuts import render,redirect , get_object_or_404
from .models import Product
from .forms import ProductForm
from django.contrib import messages


# List available products.
def product_list(request):
    products = Product.objects.filter(delete_status=1).order_by('-priority','-created_date')
    return render(request,'products/product_list.html',{'products':products})

# Shows the details about a product.
def product_detail(request,id):
    product = get_object_or_404(Product,id=id, delete_status=1)
    return render(request,'products/product_detail.html',{'product':product})

# Add new products to site(Admin feature)
def product_add(request):
    
    # Verification is loged user has staff access
    if not request.user.is_staff :
        messages.error(request,"Permission Denied.")
        return redirect('home')
    
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request,"Product added successfully.")
            return redirect('product_add')
        
    else :
        form = ProductForm()
    
    return render(request,'products/product_add.html',{'form':form})



# Edit product details(Admin feature)
def product_edit(request,id):
    # Verification is loged user has staff access
    if not request.user.is_staff:
        messages.error(request,"Permission Denied")
        return redirect('home')
    
    product = get_object_or_404(Product,id=id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request,"Product updated successfully!")
            return redirect('product_detail',id=product.id)
        
    else:
        form = ProductForm(instance=product)

    return render(request,'products/product_edit.html',{
    'form': form,
    'product': product
})


# Delete product 
def product_delete(request,id):
    #Verification is logged user has staff access
    if not request.user.is_staff:
        messages.error(request,"Permission Denied")
        return redirect('home')
    
    product = get_object_or_404(Product,id=id)
    product.delete_status = 0
    product.save()
    messages.success(request,"Product deleted successfully!")
    return redirect('product_list')
