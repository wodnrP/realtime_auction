from rest_framework.authentication import get_authorization_header
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializer import WishlistSerializer
from product.models import Products
from django.conf import settings
from .models import Wishlist
from user.models import User
import jwt


# 로그인 한 사용자의 id 정보
def user_check(request):
    access_token = get_authorization_header(request).split()[1]
    decode_token = jwt.decode(
        access_token, 
        settings.SECRET_KEY, 
        algorithms=['HS256'], 
        verify=False)
    users_id = decode_token['user_id']
    user = User.objects.get(id=users_id)
    return user

# wishlist에 이미 저장한 항목인이 확인 
def wish_check(request, product_id):
    user = user_check(request)
    product = get_object_or_404(Products, id=product_id)
    wish_check = Wishlist.objects.filter(
        users_id=user,
        product_id=product,
        wishlist_active=True
        ).exists()
    return wish_check


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
    이미 저장한 값인지 확인
    사용자 정보, 프로덕트 정보, active값 True 저장
    Wishlist DoesNotExist 예외처리
    이미 저장한 경우 알림 
    """
    def post(self, request, product_id):
        wishcheck = wish_check(request, product_id)
        user = user_check(request)
        product = get_object_or_404(Products, id=product_id)
        
        if wishcheck is False:
            try:
                wishlist = Wishlist(
                    users_id=user, 
                    product_id=product, 
                    wishlist_active=True
                    )
                if wishlist.product_id.product_name == product.product_name:
                    wishlist.save()
            
            except Wishlist.DoesNotExist:
                wishlist = Wishlist(
                    users_id=user, 
                    product_id=product, 
                    wishlist_active=True
                )
                wishlist.save()
            
            serializer = WishlistSerializer(wishlist, partial=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'Message : already saved'},status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, product_id):
        user = user_check(request)
        wishcheck = wish_check(request, product_id)
        product = Products.objects.get(id=product_id)

        if wishcheck is True:
            wishlist = Wishlist.objects.get(users_id=user, product_id=product)
            wishlist.delete()
            return Response({'Message':'delete success'},status=status.HTTP_200_OK)