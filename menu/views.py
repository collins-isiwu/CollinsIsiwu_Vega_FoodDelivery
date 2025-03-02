from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Food, FoodRating, FoodComment
from .serializers import FoodRatingSerializer, FoodCommentSerializer, FoodDetailSerializer, FoodSerializer
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
    ordering_fields = ['price', 'average_rating'] # Allow sorting by price and average rating

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
                'error': None,
                'message': 'Food items fetched successfully.',
                'data': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'status': status.HTTP_200_OK,
            'error': None,
            'message': 'Food items fetched successfully.',
            'data': serializer.data
        })


class FoodDetailAdminView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific food item.
    Only admins can update or delete food items.
    """
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

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
                'error': None,
                'message': 'Food item updated successfully.',
                'data': serializer.data
            })
        return Response({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'error': serializer.errors,
            'message': 'Failed to update food item.',
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
            'error': None,
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
                'error': None,
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


class FoodDetailView(generics.RetrieveAPIView):
    """
    API view for users to view the details of a specific food item.
    Users can only view available food items.
    """
    serializer_class = FoodDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Override the default queryset to ensure only available food items are retrieved.
        """
        return Food.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve the details of an available food item.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                'success': True,
                'status': status.HTTP_200_OK,
                'error': None,
                'message': 'Food details fetched successfully.',
                'data': serializer.data
            })
        except Food.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'error': 'Food item not found or unavailable.',
                'message': 'The requested food item does not exist or is unavailable.',
                'data': None
            })



class FoodRatingCreateView(generics.CreateAPIView):
    """
    API view for users to rate a food item.
    """
    queryset = FoodRating.objects.all()
    serializer_class = FoodRatingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            rating = serializer.save(user=request.user)
            return Response({
                'success': True,
                'status': status.HTTP_201_CREATED,
                'error': None,
                'message': 'Rating submitted successfully.',
                'data': {'food': rating.food.name, 'rating': rating.rating}
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Failed to rate food.',
            'error': serializer.errors,
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)


class FoodCommentCreateView(generics.CreateAPIView):
    """
    API view for users to comment on a food item.
    """
    queryset = FoodComment.objects.all()
    serializer_class = FoodCommentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            comment = serializer.save(user=request.user)
            return Response({
                'success': True,
                'status': status.HTTP_201_CREATED,
                'error': None,
                'message': 'Comment submitted successfully.',
                'data': {'food': comment.food.name, 'comment': comment.comment}
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'error': serializer.errors,
            'message': 'Failed to comment on food.',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)
    