from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from math import ceil

from store.models import *

# Create your views here.

BOOKS_PER_PAGE = 8

def index(request):
    return render(request, 'index.html')

def browse(request):
    # total_pages = ceil(Book.objects.count() / BOOKS_PER_PAGE)

    paginator = Paginator(Book.objects.all(), BOOKS_PER_PAGE)

    try:
        current_page = int(request.GET.get('page', 1))
        if current_page > paginator.num_pages:
            return redirect(f'/books?page={paginator.num_pages}')
        elif current_page < 1:
            return redirect(f'/books')
    except ValueError:
        current_page = 1

    books = paginator.get_page(current_page)

    return render(request, 'browse.html', {'books': books})

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
    return redirect('product', book_id=book_id)

def remove_from_cart(request):
    book_id = int(request.POST.get('book_id'))
    book = get_object_or_404(Book, id=book_id)

    cart_id = request.session.get('cart_id', None)
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        cart.items.remove(book)

    referrer = request.META.get('HTTP_REFERER', '/')
    return redirect(referrer)
