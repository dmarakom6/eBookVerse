from store.models import Cart

def cart(request):
  try:
    cart_id = request.session['cart_id']
    cart = Cart.objects.get(id=cart_id)
    return { 'cart': cart }
  except:
    return { 'cart': Cart() }
