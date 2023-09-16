from django.urls import path
from django.conf import settings
from .views import WishlistView

urlpatterns = [
    path('', WishlistView.as_view(), name="get_wishlist"),
    path('<int:product_id>', WishlistView.as_view(), name="post_delete_wishlist")    
]