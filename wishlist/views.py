from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import WishlistSerializer
from .models import Wishlist
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import get_authorization_header
from rest_framework.permissions import IsAuthenticated

class WishlistView(APIView):
    # 로그인 여부 확인
    permission_classes = [IsAuthenticated]
    """
    1 page 최대 items 수 = 10
    page 기본 값 = 1
    """
    def get(self, request):
        page = request.GET.get('page', None)
        items = request.GET.get('items', None)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        
        if page is None:
            page = 1
        if items is not None:
            paginator.page_size = int(items)
        page = int(page)

        wishlist = Wishlist.objects.filter()
        result = paginator.paginate_queryset(wishlist, request)
        try:
            serializer = WishlistSerializer(result, many = True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Wishlist.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

    """
    1. 사용자 로그인 확인
    2. 로그인 된 사용자라면 
        product_id를 request로 받고, 
        2-1
            product_id가 Products DB 테이블에 존재할 때 
            whishlist_active 값을 True로 하는 wishlist 객체 생성
        2-2
            product_id가 Products DB에 존재하지 않을 때
            Error : Product Does not exist
    3. 로그인 된 사용자가 아니라면 
        Message : 권한이 없습니다.
    """
    def post(self, request):
        pass

    """
    1. 사용자 로그인 확인
    2. 로그인 된 사용자라면
        wishlist DB에 해당 사용자가 해당 프로덕트를 저장했을 경우
        wishlist_active가 True이면 
        wishlist 객체 삭제
        Message : success
    """
    def delete(self, request):
        pass