from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import *

from django.contrib import messages
# Create your views here.

#Products
def index(request):
    return render(request, 'index.html')

def categories(request):
    categories_data = Category.objects.all()
    return render(request, 'categories.html',context={'categories':categories_data})


def products(request,category):
    products_data = Product.objects.filter(prod_category=category).all()
    title = Category.objects.get(id=category).title
    return render(request, 'products.html',context={'products':products_data,'title':title})
#--------------------------------------------------------------------------------------------------------------------------------
#Cart Functions
@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    user = request.user

    # Get the product and the user's cart
    product = get_object_or_404(Product, prod_id=product_id)

    # Check if the product has enough stock
    if product.prod_stock < 1:
        messages.error(request, f"{product.prod_title} is out of stock.".title())
        return redirect(f'/products/{product.prod_category.id}')  # Replace 'your_product_list_url' with the actual URL of your product list view

    cart, created = Cart.objects.get_or_create(user=user)

    # Check if the product is already in the cart, update quantity if exists, otherwise create a new item
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        # Check if updating quantity will exceed available stock
        if product.prod_stock > 0:
            cart_item.quantity += 1
            product.prod_stock -= 1
            product.save()
            cart_item.save()
            messages.success(request, f"{product.prod_title} quantity updated in your cart.".title())
        else:
            messages.error(request, f"{product.prod_title} does not have enough stock.".title())
    else:
        product.prod_stock -= 1
        product.save()
        messages.success(request, f"{product.prod_title} added to your cart.".title())

    return redirect(f'/products/{product.prod_category.id}')  # Replace 'your_product_list_url' with the actual URL of your product list view


@login_required(login_url='/login/')
def cart(request):
    user = request.user

    # Fetch the user's cart and related cart items
    try:
        cart_items = user.cart.cartitem_set.all()
    except Cart.DoesNotExist:
        cart_items = []

    # Create a list of dictionaries with product and quantity information
    products_in_cart = [{'product': cart_item.product, 'quantity': cart_item.quantity} for cart_item in cart_items]
    total = [cart_item.product.prod_price*cart_item.quantity for cart_item in cart_items]
    print(total)
    print(products_in_cart)
    return render(request, 'cart.html', {'products_in_cart': products_in_cart,'total': sum(total)})

@login_required(login_url='/login/')
def remove_from_cart(request,product_id,action=None):
    user = request.user
    product = get_object_or_404(Product, prod_id=product_id)
    cart, created = Cart.objects.get_or_create(user=user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if action == 'Remove':
        product.prod_stock += cart_item.quantity
        product.save()
        cart_item.delete()
        messages.success(request, f"{product.prod_title} deleted from your cart.".title())
        return redirect('cart')
    elif action == 'Add':
        if product.prod_stock > 0:
            cart_item.quantity += 1
            product.prod_stock -= 1
            product.save()
            cart_item.save()
            messages.success(request, f"{product.prod_title} quantity updated in your cart.".title())
        else:
            messages.error(request, f"{product.prod_title} does not have enough stock.".title())
    else:
        cart_item.quantity -= 1
        product.prod_stock += 1
        product.save()
        cart_item.save()
        if cart_item.quantity < 1:
            cart_item.delete()
            messages.error(request, f"{product.prod_title} deleted from your cart.".title())
        else:
            messages.success(request, f"{product.prod_title} quantity updated in your cart.".title())
    return redirect('cart')

#--------------------------------------------------------------------------------------------------------------------------------
#Wishlist
@login_required(login_url='/login/')
def add_to_wishlist(request, product_id):
    user = request.user


    product = get_object_or_404(Product, prod_id=product_id)

    wishlist, created = Wishlist.objects.get_or_create(user=user)


    wishlist_item, item_created = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
    if not item_created:
        wishlist_item.delete()
        messages.error(request, f"{product.prod_title} removed from your wishlist.".title())
        return redirect('wishlist')
    else:
        messages.success(request, f"{product.prod_title} added to your wishlist.".title())

    return redirect(f'/products/{product.prod_category.id}')

@login_required(login_url='/login/')
def wishlist(request):
    user = request.user

    # Fetch the user's wishlist and related wishlist items
    try:
        wishlist_items = user.wishlist.wishlistitem_set.all()
    except Wishlist.DoesNotExist:
        wishlist_items = []

    # Create a list of dictionaries with product and quantity information
    products_in_wishlist = [{'product': wishlist_item.product} for wishlist_item in wishlist_items]
    
    print(products_in_wishlist)
    return render(request, 'wishlist.html', {'products_in_wishlist': products_in_wishlist})




#--------------------------------------------------------------------------------------------------------------------------------
#Authentication Functions
def loginUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('categories')
        else:
            return redirect('login-page')
    else:
        return render(request, 'Auth/login.html')
    
def logoutUser(request):
    logout(request)
    return redirect('index')

def signUpUser(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        if User.objects.filter(email=email).exists():
            return redirect('signup-page')
        if password != re_password:
            return redirect('signup-page')
        user = User(full_name=full_name, email=email, password=password,username=email)
        user.save()
        return redirect('login-page')
    else:
        return render(request,'Auth/signup.html')
    

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        if User.objects.filter(email=email).exists():
            try:
                user = User.objects.get(email=email)
                user.set_password(re_password)
                user.save()
                return redirect('login-page')
            except:
                return redirect('forgot_password')
        return redirect('forgot_password')
    else:
        return render(request, 'Auth/forgot_password.html')
        
 #--------------------------------------------------------------------------------------------------------------------------------
#Static Pages   
def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        feed = request.POST.get('feedback')
        Feedback.objects.create(name=name, email=email,feedback=feed)
        messages.success(request, f"Feedback Recieved.".title())
        return redirect('feedback')
    return render(request,'feedback.html')

@login_required(login_url='/staff_login/')
def list_feedback(request):
    if request.user.role == "Staff":
        feedbacks = Feedback.objects.all()
        return render(request, 'list_feedback.html',context={'feedbacks':feedbacks})
    else:
        return redirect('index')
#--------------------------------------------------------------------------------------------------------------------------------
#Staff Side

@login_required(login_url='/staff_login/')
def inventory(request):
    if request.user.role == "Staff":
        products = Product.objects.all()
        return render(request,'inventory.html',context={'products':products})
    else:
        return redirect('index')

def update_inventory(request,prod_id,action=None):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        product = get_object_or_404(Product, prod_id=prod_id)
        product.prod_stock = int(quantity)
        product.save()
        messages.success(request, f"{product.prod_title} stock updated. {product.prod_stock} Available".title())
        return redirect("inventory")
    else:
        if action == 'Add':
            product = get_object_or_404(Product, prod_id=prod_id)
            product.prod_stock += 1
            product.save()
            messages.success(request, f"{product.prod_title} stock updated. {product.prod_stock} Available".title())
            return redirect('inventory')
        elif action == 'Minus':
            product = get_object_or_404(Product, prod_id=prod_id)
            product.prod_stock -= 1
            product.save()
            messages.success(request, f"{product.prod_title} stock updated. {product.prod_stock} Available".title())
            return redirect('inventory')
        else:
            return render(request, 'update_inventory.html')
        
def staff_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None and user.role == 'Staff':
            login(request, user)
            return redirect('inventory')
        else:
            messages.success(request, "Invalid username or password")
            return redirect('staff_login')
    return render(request, 'staff_login.html')
