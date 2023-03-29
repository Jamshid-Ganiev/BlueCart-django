from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from store.models import Product, Variation
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def _cart_id(request):
    """return the cart from the user's session key"""
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# Create your views here.
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        total_after_tax = 0

        if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (0.4 * total) //100
        total_after_tax = total - tax
    except:
        pass
    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "total_after_tax": total_after_tax,
    }

    return render(request, 'store/cart.html', context)



def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)

    # if user is authenticated
    if current_user.is_authenticated:
        product_variation = []


        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)

            exis_var_list = []
            id =  []
            for item in cart_item:
                existing_variation = item.variations.all()
                exis_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in exis_var_list:
                # increase the cart item quantity
                index = exis_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity = 1,
                user = current_user,
            )

            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        
        return redirect('carts:cart')

    # if user is authenticated
    else:
        product_variation = []


        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # existing variations -> database
            # current variation -> product_variation
            # item id - database

            exis_var_list = []
            id =  []
            for item in cart_item:
                existing_variation = item.variations.all()
                exis_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in exis_var_list:
                # increase the cart item quantity
                index = exis_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity = 1,
                cart = cart
            )

            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        
        return redirect('carts:cart')


def remove_cart(request, product_id, cart_item_id):
    
    product = get_object_or_404(Product, id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    
    return redirect("carts:cart")

def remove_cart_item(request, product_id, cart_item_id):
    
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    
    return redirect('carts:cart')


@login_required(login_url='accounts:login')
def checkout(request, total=0, quantity=0, cart_items=None):

    if not request.user.is_authenticated:
        return redirect(f'{reverse("accounts:login")}?next={reverse("carts:checkout")}')
    try:
        tax = 0
        total_after_tax = 0
        
        if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (0.4 * total) //100
        total_after_tax = total - tax
    except:
        pass

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "total_after_tax": total_after_tax,
    }
    
    return render(request, 'store/checkout.html', context)