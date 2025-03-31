import stripe

from config.settings import STRIPE_API_KEY



class StripeTransaction:
    stripe.api_key = STRIPE_API_KEY


    @staticmethod
    def create_checkout_session(success_url, price_id, customer_email):
        session = stripe.checkout.Session.create(
            success_url=success_url,
            line_items=[{"price": price_id, "quantity": 1}],
            mode="payment",
            customer_email=customer_email,
        )
        return session



    @staticmethod
    def create_product(name, description):
        product = stripe.Product.create(name=name, description=description)
        return product


    @staticmethod
    def create_price(product,price):
        price = stripe.Price.create(
              currency="usd",
              unit_amount_decimal=price*100,
              product_data={"name": product},
            )
        return price

