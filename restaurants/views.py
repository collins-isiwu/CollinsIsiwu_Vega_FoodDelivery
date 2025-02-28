from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Restaurant
from .serializers import RestaurantSerializer
from users.permissions import IsAdmin  

class RestaurantListCreateView(generics.ListCreateAPIView):
    """
    API view to list and create restaurants. Only admins can create restaurants.
    """
    queryset = Restaurant.objects.all().order_by('id')
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        """
        Override the list method to return all restaurants.
        """
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'success': True,
                'status': status.HTTP_200_OK,
                'error': None,
                'message': 'Restaurants fetched successfully.',
                'data': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'status': status.HTTP_200_OK,
            'error': None,
            'message': 'Restaurants fetched successfully.',
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        """
        Override the create method to add a new restaurant by an admin.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'status': status.HTTP_201_CREATED,
                'error': None,
                'message': 'Restaurant created successfully.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'error': serializer.errors,
            'message': 'Failed to create restaurant.',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific restaurant by ID. Only admins can perform updates or deletes.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific restaurant.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'status': status.HTTP_200_OK,
            'error': None,
            'message': 'Restaurant details fetched successfully.',
            'data': serializer.data
        })

    def update(self, request, *args, **kwargs):
        """
        Update a specific restaurant by ID.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'status': status.HTTP_200_OK,
                'error': None,
                'message': 'Restaurant updated successfully.',
                'data': serializer.data
            })
        return Response({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'error': serializer.errors,
            'message': 'Failed to update restaurant.',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific restaurant by ID.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'status': status.HTTP_204_NO_CONTENT,
            'error': None,
            'message': 'Restaurant deleted successfully.',
            'data': None
        }, status=status.HTTP_204_NO_CONTENT)

