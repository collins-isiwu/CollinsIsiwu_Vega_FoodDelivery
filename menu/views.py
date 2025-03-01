from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Food
from .serializers import FoodSerializer, FoodDetailSerializer
from users.permissions import IsAdmin 

class FoodListView(generics.ListAPIView):
    """
    API view for listing and filtering food items.
    Users and admins can filter based on availability, price, and name.
    """
    queryset = Food.objects.all().order_by('id')
    serializer_class = FoodDetailSerializer 
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'price', 'is_available']

    def list(self, request, *args, **kwargs):
        """
        Override the list method to paginate and filter the food items.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'success': True,
                'status': status.HTTP_200_OK,
                'message': 'Food items fetched successfully.',
                'data': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Food items fetched successfully.',
            'data': serializer.data
        })


class FoodDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific food item.
    Only admins can update or delete food items.
    """
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve details of a food item.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Food details fetched successfully.',
            'data': serializer.data
        })

    def update(self, request, *args, **kwargs):
        """
        Update a food item.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'status': status.HTTP_200_OK,
                'message': 'Food item updated successfully.',
                'data': serializer.data
            })
        return Response({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Failed to update food item.',
            'error': serializer.errors,
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a food item.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'status': status.HTTP_204_NO_CONTENT,
            'message': 'Food item deleted successfully.',
            'data': None
        }, status=status.HTTP_204_NO_CONTENT)


class FoodCreateView(generics.CreateAPIView):
    """
    API view to create food items. Only admins can create food items.
    """
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def create(self, request, *args, **kwargs):
        """
        Override the create method to allow an admin to add new food items.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'status': status.HTTP_201_CREATED,
                'message': 'Food item created successfully.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Failed to create food item.',
            'error': serializer.errors,
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)


class FoodDetailForUsersView(generics.RetrieveAPIView):
    """
    API view for users to view the details of a specific food item.
    Users can only view available food items.
    """
    queryset = Food.objects.filter(is_available=True)
    serializer_class = FoodDetailSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve the details of an available food item.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Food details fetched successfully.',
            'data': serializer.data
        })
