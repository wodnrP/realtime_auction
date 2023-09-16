from django.urls import path
from product import views

urlpatterns = [
    path("all-products", views.ProductsView.as_view(), name="all_products"),
    path("new-product", views.NewProductView.as_view(), name="new_product"),
    path("<str:pk>/delete", views.DeleteProductView.as_view(), name='delete_product'),
    path('upload-images', views.ImageView.as_view(), name="upload_images"),
    path('images/<str:products_id>', views.ImageView.as_view(), name='get_images'),
]
