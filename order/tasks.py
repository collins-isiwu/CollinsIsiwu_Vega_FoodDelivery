import logging
from celery import shared_task
from .models import Order

logger = logging.getLogger(__name__)

@shared_task
def engage_restaurant_and_courier(order_id):
    """
    Engage the restaurant and courier for 15 minutes after an order is placed.
    """
    try:
        order = Order.objects.get(id=order_id)
        restaurant = order.restaurant

        order.restaurant_engaged = True
        order.courier_engaged = True
        order.save()

        restaurant.is_available = False
        restaurant.save()

        schedule_restaurant_availability.apply_async(args=[order_id], countdown=15 * 60)
        return f"Order {order_id} processed, restaurant and courier engaged"
    except Order.DoesNotExist:
        logger.error(f"Order {order_id} not found")


@shared_task
def schedule_restaurant_availability(order_id):
    """
    After 15 minutes, make the restaurant available again.
    """
    try:
        order = Order.objects.get(id=order_id)
        restaurant = order.restaurant

        restaurant.is_available = True
        restaurant.save()

        order.restaurant_engaged = False
        order.courier_engaged = False
        order.status = 'Delivered'
        order.save()

        return f"{restaurant.name} and courier are now available for new order"
    except Order.DoesNotExist:
        logger.error(f"Order {order_id} not found")
