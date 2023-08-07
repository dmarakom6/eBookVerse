from django.shortcuts import render

from store.models import *

# Create your views here.

def index(request):
    return render(request, 'index.html')

def browse(request):
    return render(request, 'browse.html')

def product(request, book_id):
    book = Book.objects.get(id=book_id)
    book.price_cents = '{:,.2f}'.format(book.price_cents/100) #convert to euro
    return render(request, 'product.html', {'book': book})

def author(request, author_id):
    return render(request, 'contributor.html')

def editor(request, editor_id):
    return render(request, 'editor.html')