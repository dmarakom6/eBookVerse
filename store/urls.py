from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.browse, name='browse'),
    path('books/<int:book_id>', views.product, name='product'),
    path('authors/<int:author_id>', views.author, name='author'),
    path('publishers/<int:editor_id>', views.editor, name='publisher'),
    path('cart', views.add_to_cart, name='add_to_cart'),
    path('cart/delete', views.delete_cart, name='delete_cart'),
    path('cart/<int:book_id>/remove', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout', views.checkout, name='checkout'),
    path('order/<int:order_id>', views.order, name='order'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# RESTful
