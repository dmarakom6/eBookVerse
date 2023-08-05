from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.browse, name='browse'),
    path('books/<int:book_id>', views.product, name='product'),
]
