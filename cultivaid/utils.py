import stripe
from cultivaid import app

def create_stripe_checkout_session(service_name, amount, booking_id):
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': amount,
                    'product_data': {
                        'name': service_name,
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{request.host_url}payment/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{request.host_url}payment/cancel",
            metadata={
                'booking_id': booking_id
            }
        )
        return checkout_session
    except Exception as e:
        app.logger.error(f'Stripe session creation error: {str(e)}')
        raise