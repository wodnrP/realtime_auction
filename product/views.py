from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Products, ProductImages
from rest_framework.response import Response
from .serializers import ProductsSerializer, ImageSerializer
from rest_framework import status
from django.utils import timezone
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .filters import ProductsFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser

now = timezone.now()


class ProductsView(APIView):
    def get(self, request):
        filter_set = ProductsFilter(
            request.GET,
            queryset=Products.objects.filter(auction_end_at__gt=now).order_by(
                "auction_end_at"
            ),
        )
        # 페이지네이션
        paginator = PageNumberPagination()
        paginator.page_size = 2
        queryset = paginator.paginate_queryset(filter_set.qs, request)
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


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        products_id = self.kwargs.get("products_id")
        images = ProductImages.objects.filter(products_id=products_id)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)
