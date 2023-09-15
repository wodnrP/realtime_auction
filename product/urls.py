from django.urls import path
from product import views

urlpatterns = [
    path("all-products", views.ProductsView.as_view(), name="all-products"),
    path("new-product", views.NewProductView.as_view(), name="all-products"),
]
