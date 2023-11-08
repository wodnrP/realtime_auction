from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Products, ProductImages
from rest_framework.response import Response
from .serializers import ProductsSerializer, ImageSerializer
from rest_framework import status
from django.utils import timezone
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .filters import ProductsFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser

now = timezone.now()


class ProductsView(APIView):
    """
    현재 활성화된 경매 상품의 페이지네이션된 목록을 반환합니다.

    Parameters:
    - request: HTTP GET 요청 객체

    Returns:
    - Response: 페이지네이션된 상품 목록을 포함한 JSON 응답

    Errors:
    - 400 Bad Request: 요청 데이터가 유효하지 않은 경우
    """

    def get(self, request):
        filter_set = ProductsFilter(
            request.GET,
            queryset=Products.objects.filter(auction_end_at__gt=now).order_by(
                "auction_end_at"
            ),
        )
        paginator = PageNumberPagination()
        paginator.page_size = 2
        queryset = paginator.paginate_queryset(filter_set.qs, request)
        serializer = ProductsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class NewProductView(APIView):
    """
    새로운 상품을 생성하는 뷰입니다.

    인증과 권한이 필요합니다.

    Parameters:
    - request: HTTP POST 요청 객체

    Returns:
    - Response: 생성된 상품 정보 또는 오류 메시지를 포함한 JSON 응답

    Errors:
    - 400 Bad Request: 요청 데이터가 유효하지 않은 경우
    - 403 Forbidden : 현재 판매 활동이 불가능 한 경우
    """

    def post(self, request):
        if not request.user.can_sell:
            return Response({"error":"현재 판매 활동이 불가능 합니다."},status=status.HTTP_403_FORBIDDEN)
            
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            current_date = serializer.validated_data["auction_start_at"]
            final_date = current_date + timezone.timedelta(days=3)
            serializer.validated_data["auction_end_at"] = final_date
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class DeleteProductView(APIView):
    """
    상품을 삭제하는 뷰입니다.

    인증과 권한이 필요하며 활성화된 경매만 삭제할 수 있습니다.

    Parameters:
    - request: HTTP DELETE 요청 객체
    - pk: 삭제할 상품의 기본 키

    Returns:
    - Response: 성공 또는 실패 메시지를 포함한 JSON 응답

    Errors:
    - 400 Bad Request: 요청 데이터가 유효하지 않은 경우
    - 403 Forbidden: 상품을 삭제할 권한이 없는 경우
    - 404 Not Found: 삭제하려는 상품이 존재하지 않는 경우
    """

    def delete(self, request, pk):
        product = get_object_or_404(Products, pk=pk, product_active=True)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAuthenticated])
class ImageView(APIView):
    """
    상품 이미지 업로드와 검색을 다루는 뷰입니다.

    인증과 권한이 필요하며 이미지 업로드와 검색을 지원합니다.

    Parameters:
    - request: HTTP POST 또는 GET 요청 객체

    Returns:
    - Response: 업로드된 이미지 정보 또는 검색된 이미지 목록을 포함한 JSON 응답

    Errors:
    - 400 Bad Request: 요청 데이터가 유효하지 않은 경우
    """

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        """
        이미지 업로드를 처리합니다.

        Parameters:
        - request: 이미지 데이터를 포함한 HTTP POST 요청 객체

        Returns:
        - Response: 업로드된 이미지 정보 또는 오류 메시지를 포함한 JSON 응답

        Errors:
        - 400 Bad Request: 요청 데이터가 유효하지 않은 경우
        """
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            product_id = request.data.get("products_id")
            if product_id:
                product = Products.objects.get(pk=product_id)
                serializer.save(products_id=product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"error": "product_id is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """
        상품에 연결된 이미지를 검색합니다.

        Parameters:
        - request: 상품 ID를 포함한 HTTP GET 요청 객체

        Returns:
        - Response: 상품과 연결된 이미지 URL 목록을 포함한 JSON 응답

        Errors:
        - 400 Bad Request: 요청 데이터가 유효하지 않은 경우
        - 404 Not Found: 검색하려는 상품이 존재하지 않는 경우
        """
        products_id = self.kwargs.get("products_id")
        images = ProductImages.objects.filter(products_id=products_id)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)
