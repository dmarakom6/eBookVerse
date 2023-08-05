from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def browse(request):
    return render(request, 'browse.html')

def product(request, book_id):
    # Go to the database and get the book with the given id
    # Pass the book to the template
    # If book doesn't exist, return a 404
    return render(request, 'product.html')
