from django.test import TestCase
from django.contrib.auth import get_user_model
from product.models import Products, Categories
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import pytest

pytestmark = pytest.mark.django_db
User = get_user_model()


class TestProductsModel:
    def test_str_method(self, products_factory):
        x = products_factory(product_name="test")
        assert x.__str__() == "test"

    def test_set_auction_active_method(
        self, user_factory, categories_factory, products_factory
    ):
        current_datetime = timezone.now()
        past_datetime = current_datetime - timezone.timedelta(days=5)

        category = categories_factory(category_name="TestCategory")
        product = products_factory(
            seller_id=user_factory(
                username="testuser",
                phone_number="01012341234",
                nickname="user_name",
                address="address",
                profile_image="asdasd.jpg",
                password="password",
            ),
            product_name="TestProduct",
            product_price="100",
            product_content="Test content",
            auction_start_at=current_datetime,
            auction_end_at=past_datetime,
            category=category,
        )
        assert not product.auction_active

    # # set_auction_active 메서드를 직접 호출하여 auction_active가 False로 설정되었는지 확인
    #     product.set_auction_active()
    #     product.refresh_from_db()
    #     self.assertFalse(product.auction_active)

    #     # auction_end_at를 미래로 설정하고 set_auction_active 메서드를 호출하여 auction_active가 True로 설정되었는지 확인
    #     future_datetime = timezone.now() + timezone.timedelta(days=5)
    #     product.auction_end_at = future_datetime
    #     product.set_auction_active()  # save 메서드 호출 제거
    #     product.refresh_from_db()
    #     self.assertTrue(product.auction_active)
