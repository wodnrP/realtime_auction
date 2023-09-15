from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Products
from rest_framework.response import Response
from .serializers import ProductsSerializer
from rest_framework import status
from django.utils import timezone
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

now = timezone.now()


class ProductsView(APIView):
    def get(self, request):
        # 목록을 가져오는 GET 요청 처리 로직
        queryset = Products.objects.filter(auction_end_at__gt=now).order_by(
            "auction_end_at"
        )
        serializer = ProductsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class NewProductView(APIView):
    def post(self, request):
        # POST 요청 처리 로직
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class DeleteProductView(APIView):
    def delete(self, request, pk):
        product = get_object_or_404(Products, pk=pk, auction_active=True)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
