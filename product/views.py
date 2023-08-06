from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Product, Rating, Cart, CartItem, Category, Comment
from django.shortcuts import render, get_object_or_404, redirect
from .form import ContactMsgForm
from django.contrib import messages


def AllView(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        if cart.exists():
            cart = cart[0]
            cartitem = CartItem.objects.filter(cart=cart).count()
        else:
            cartitem = 0
            Cart.objects.create(user=request.user)
        context = {
            'item_len': cartitem,
        }
        return context
    else:
        session_cart = request.session.get('cart', {})
        product = session_cart.get('product', None)
        if product is None:
            request.session['cart'] = {}
            request.session['cart']['product'] = []
            return {'item_len': 0}
        else:
            return {"item_len": len(session_cart['product'])}


def all_obj(request, obj):
    p = Paginator(obj, 12)
    page = request.GET.get('page')
    category = Category.objects.all()
    return p.get_page(page), category


def home(request):
    context = {}
    return render(request, 'home.html', context=context)


def DetailPageView(request, pk):
    obj = get_object_or_404(Product, pk=pk)
    category_obj = Product.objects.filter(category=obj.category)
    comment = Comment.objects.filter(post=obj)
    context = {
        "obj_category": category_obj,
        'obj': obj,
        "comment": comment
    }
    return render(request, 'shop-details.html', context)


def about(request):
    return render(request, 'about.html')


@login_required(login_url='login')
def CommentAddView(request, pk):
    product = get_object_or_404(Product, pk=pk)
    rating = request.GET.get('rating', None)
    Rating.objects.update_or_create(
        user=request.user,
        product=product,
        defaults={"rating": rating}
    )
    Comment.objects.create(
        user=request.user,
        message=request.GET.get("message"),
        post=product
    )
    return redirect('detailpage', pk)


def ShopView(request):
    products = Product.objects.filter(is_active=True)
    products, category = all_obj(request, products)
    context = {
        'product': products,
        'category': category,
    }
    return render(request, 'shop.html', context)


def CategoriesView(request, slug):
    category_obj = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category_obj)
    products, category = all_obj(request, products)
    context = {
        'product': products,
        'category': category,
        'activ': category_obj.id,
    }
    return render(request, 'shop.html', context)


def ProductFilterView(request, minimum=1, maximum=1):
    products = Product.objects.filter(price__gte=minimum, price__lte=maximum)
    category = Category.objects.all()
    context = {
        'product': products,
        'category': category,
        'minimum': minimum,
        'maximum': maximum,
    }
    return render(request, 'shop.html', context)


def SearchView(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        products = Product.objects.filter(title__icontains=search)
        category = Category.objects.all()
        context = {
            'product': products,
            'category': category,
        }
        return render(request, 'shop.html', context)


def CartView(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        context = {'cart': cart}
    else:
        obj = []
        cart_session = request.session.setdefault('cart', {})
        for i in cart_session['product']:
            obj_product = get_object_or_404(Product, pk=i['product'])
            obj_product.total_price = int(obj_product.price) * int(i['quantity'])
            obj_product.quantity = i['quantity']
            obj.append(obj_product)
        context = {
            'cart_session': obj,
        }
    return render(request, 'cart.html', context)


def CartItemAddView(request, pk):
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
        product = get_object_or_404(Product, pk=pk)
        cart_item = CartItem.objects.filter(cart=cart, product=product)
        if cart_item:
            cart_item = cart_item[0]
            cart_item.quantity += 1
            cart_item.total_price = cart_item.quantity * product.price
            cart_item.save()
        else:
            cartitem = CartItem.objects.create(cart=cart, product=product)
            cartitem.total_price = cartitem.quantity * product.price
            cartitem.save()
        return redirect('cart')
    else:
        cart = request.session.setdefault('cart', {})
        product = get_object_or_404(Product, pk=pk)
        if cart['product'] == []:
            cart['product'].append({'product': product.id, 'quantity': 1})
            request.session['cart'] = cart
        else:
            for i in cart['product']:
                if i['product'] == product.id:
                    i['quantity'] += 1
                    request.session['cart'] = cart
                    return redirect('cart')
            cart['product'].append({'product': product.id, 'quantity': 1})
            request.session['cart'] = cart
        return redirect('cart')


def CartItemRemoveView(request, pk):
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
        product = get_object_or_404(Product, pk=pk)
        full_item = CartItem.objects.filter(cart=cart)
        cart_item = full_item.filter(product=product)
        if cart_item:
            cart_item = cart_item[0]
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.total_price = cart_item.quantity * product.price
                cart_item.save()
            else:
                cart_item.delete()
        return redirect('cart')
    else:
        cart = request.session.setdefault('cart', {})
        product = get_object_or_404(Product, pk=pk)
        if cart['product'] == []:
            return redirect('cart')
        else:
            for i in cart['product']:
                if i['product'] == product.id:
                    if i['quantity'] > 1:
                        i['quantity'] -= 1
                        request.session['cart'] = cart
                        return redirect('cart')
                    else:
                        cart['product'].remove(i)
                        request.session['cart'] = cart
                        return redirect('cart')
            return redirect('cart')


def DeleteItemCart(request, pk):
    if request.user.is_authenticated:
        obj = CartItem.objects.get(pk=pk)
        obj.delete()
        return redirect('cart')
    else:
        cart = request.session.setdefault('cart', {})
        product = get_object_or_404(Product, pk=pk)
        if cart['product'] == []:
            return redirect('cart')
        else:
            for i in cart['product']:
                if i['product'] == product.id:
                    cart['product'].remove(i)
                    request.session['cart'] = cart
                    return redirect('cart')
            return redirect('cart')


def ContactView(request):
    if request.method == 'POST':
        form = ContactMsgForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Xabar yuborildi')
            return redirect('contact')
        messages.error(request, "xatolik Xabar yuborilmadi")
        return redirect('contact')
    return render(request, 'contact.html')


def DetailAddCart(request, pk):
    quantity = request.GET.get('quantity', None)
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
        product = get_object_or_404(Product, pk=pk)
        full_item = CartItem.objects.filter(cart=cart)
        single_item = full_item.filter(product=product)
        if single_item:
            single_item = single_item[0]
            if single_item.quantity > 1:
                single_item.quantity = int(single_item.quantity) + int(quantity)
                single_item.total_price = int(single_item.quantity) * int(product.price)
                single_item.save()
                return redirect('cart')
            single_item.quantity = quantity
            single_item.total_price = int(quantity) * int(product.price)
            single_item.save()
            return redirect('cart')
        itm = CartItem.objects.create(
            cart=cart, product=product,
        )
        itm.quantity = quantity
        itm.total_price = int(quantity) * int(product.price)
        itm.save()
        return redirect('cart')
    else:
        cart = request.session.setdefault('cart', {})
        product = get_object_or_404(Product, pk=pk)
        if cart['product'] == []:
            cart['product'].append({"product": product.id, "quantity": quantity})
            request.session['cart'] = cart
            return redirect('cart')
        for i in cart['product']:
            if i['product'] == product.id:
                i['quantity'] = int(quantity) + int(i['quantity'])
                request.session['cart'] = cart
                return redirect('cart')
        cart['product'].append({"product": product.id, "quantity": quantity})
        request.session['cart'] = cart
        return redirect('cart')
