from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Products
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProductsSerializer
from rest_framework import status


class ProductsView(APIView):
    def get(self, request):
        # 목록을 가져오는 GET 요청 처리 로직
        queryset = Products.objects.all()
        serializer = ProductsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
