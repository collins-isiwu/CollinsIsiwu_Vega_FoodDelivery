from rest_framework import generics, status, filters
from rest_framework.response import Response
from .models import Order
from users.permissions import IsAdmin
from .serializers import OrderCreateSerializer, OrderDetailSerializer, OrderListSerializer

class OrderCreateView(generics.CreateAPIView):
    """
    API view to create a new order and route it to the nearest restaurant.
    """
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer

    def create(self, request, *args, **kwargs):
        """
        Overriding the create method to include custom response handling.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'status': status.HTTP_201_CREATED,
                'error': None,
                'message': 'Order placed successfully and routed to the nearest restaurant.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'error': serializer.errors,
            'message': 'Order creation failed.',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(generics.RetrieveAPIView):
    """
    API view for users to check their order details and status.
    """
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        order_id = kwargs.get('pk')

        try:
            order = Order.objects.get(id=order_id, user=user)
        except Order.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'error': 'Order not found.',
                'message': 'Order not found or you do not have access to this order.',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(order)
        return Response({
            'success': True,
            'status': status.HTTP_200_OK,
            'error': None,
            'message': 'Order details retrieved successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class OrderListView(generics.ListAPIView):
    """
    API view to list and filter orders.
    Admins see all orders; users see only their own orders.
    """
    serializer_class = OrderListSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['restaurant__name', 'status', 'total_price']  

    def get_queryset(self):
        user = self.request.user

        if user.is_admin:
            return Order.objects.all().order_by('id')
        return Order.objects.filter(user=user) 

    def list(self, request, *args, **kwargs):
        """
        Override the list method to paginate and filter the orders.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'success': True,
                'status': status.HTTP_200_OK,
                'message': 'Orders retrieved successfully.',
                'data': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Orders retrieved successfully.',
            'data': serializer.data
        })

