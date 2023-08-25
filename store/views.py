from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from math import ceil

from store.models import *

# Create your views here.

BOOKS_PER_PAGE = 8

def index(request):
    return render(request, 'index.html')

def browse(request):
    query = Book.objects.all()
    if 'q' in request.GET:
        query = query.filter(
            Q(title__icontains=request.GET['q']) |
            Q(description__icontains=request.GET['q']) |
            Q(isbn__icontains=request.GET['q']) |
            Q(author__first_name__icontains=request.GET['q']) |
            Q(author__last_name__icontains=request.GET['q']))

    if 'topic_id' in request.GET:
        query = query.filter(topics__id=request.GET['topic_id'])


    paginator = Paginator(query, BOOKS_PER_PAGE)

    try:
        current_page = int(request.GET.get('page', 1))
        if current_page > paginator.num_pages:
            return redirect(f'/books?page={paginator.num_pages}')
        elif current_page < 1:
            return redirect(f'/books')
    except ValueError:
        current_page = 1

    books = paginator.get_page(current_page)

    return render(request, 'browse.html', {
        'books': books,
        'topics': Topic.objects.all(),
    })

def product(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'product.html', {'book': book})

def author(request, author_id):
    author = Author.objects.get(id=author_id)
    return render(request, 'contributor.html', {'author': author})

def editor(request, editor_id):
    return render(request, 'editor.html')

def add_to_cart(request):
    book_id = int(request.POST.get('book_id'))
    book = get_object_or_404(Book, id=book_id)

    cart_id = request.session.get('cart_id', None)
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id

    cart.items.add(book)
    messages.success(request, f'Successfully added "{book.title}" to your cart!', extra_tags="ItemAdded")
    return redirect('product', book_id=book_id)

def remove_from_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    cart_id = request.session.get('cart_id', None)
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        cart.items.remove(book)

    messages.success(request, f'Successfully removed "{book.title}" from your cart!', extra_tags="ItemRemoved")
    referrer = request.META.get('HTTP_REFERER', '/')
    return redirect(referrer)

def delete_cart(request):
    cart_id = request.session.get('cart_id', None)
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        cart.delete()
        del request.session['cart_id']

    referrer = request.META.get('HTTP_REFERER', '/')
    return redirect(referrer)

def checkout(request):
    try:
        cart_id = request.session.get('cart_id')
        cart = Cart.objects.get(id=cart_id)
        if cart.isempty():
            raise Exception("Cart is empty")
    except:
        return redirect('index')

    if request.method == "GET":
        return render(request, 'checkout.html')
    elif request.method == "POST":
        order = Order.objects.create(
            name=request.POST.get('name'),
            price_cents=cart.price_cents()
        )
        order.items.set(cart.items.all())
        cart.delete()
        del request.session['cart_id']
        return redirect('order', order_id=order.id)

def order(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order.html', {'order': order})
