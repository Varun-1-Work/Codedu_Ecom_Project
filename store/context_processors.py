from decimal import Decimal

def cart_count(request):
    cart = request.session.get('cart', {})
    total_items = 0

    for pid, item in cart.items():
        total_items += item.get("quantity", 0)

    return {"cart_count": total_items}
