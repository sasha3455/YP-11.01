from djS0rrow.models import Clothes


CART_SESSION_ID = 'cart'


class Basket:
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(CART_SESSION_ID)
        if basket is None:
            basket = self.session[CART_SESSION_ID] = {}
        self.basket = basket

    def add(self, clothes, quantity=1, override_quantity=False):
        clothes_id = str(clothes.id)
        if clothes_id not in self.basket:
            self.basket[clothes_id] = 0

        if override_quantity:
            self.basket[clothes_id] = quantity
        else:
            self.basket[clothes_id] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, clothes):
        clothes_id = str(clothes.id)
        if clothes_id in self.basket:
            del self.basket[clothes_id]
            self.save()

    def clear(self):
        self.session[CART_SESSION_ID] = {}
        self.save()

    def __iter__(self):
        clothes_ids = self.basket.keys()
        clothes_map = Clothes.objects.in_bulk(clothes_ids)

        for clothes_id, quantity in self.basket.items():
            clothes = clothes_map.get(int(clothes_id))
            if not clothes:
                continue
            yield {
                'clothes': clothes,
                'quantity': quantity,
                'item_total': clothes.price * quantity,
            }

    def __len__(self):
        return sum(self.basket.values())

    def get_total_price(self):
        return sum(item['item_total'] for item in self)

