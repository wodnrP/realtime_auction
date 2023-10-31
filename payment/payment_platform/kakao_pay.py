from django.conf import settings
import requests
from django.shortcuts import redirect
from payment.models import Payments
import datetime

BASE_URL = settings.BASE_URL
FRONT_URL = "http://localhost:5500"

KAKAO_PAY = settings.KAKAO_PAY
KAKAO_PAY_APPROVAL_URL = "/payment_approval.html"  # "/payments/kakao_pay_approval"
KAKAO_PAY_CANCEL_URL = "/payment_cancel.html"
KAKAO_PAY_FAIL_URL = "/payment_fail.html"


class KakaoPay(object):
    def kakao_pay_ready(self, id, user, product_name, total_amount):
        URL = "https://kapi.kakao.com/v1/payment/ready"
        headers = {
            "Authorization": "KakaoAK " + KAKAO_PAY,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        data = {
            "cid": "TC0ONETIME",  # test code
            "partner_order_id": id,
            "partner_user_id": user.phone_number,
            "item_name": product_name.product_name,
            "quantity": 1,
            "total_amount": total_amount.auction_final_price,
            "tax_free_amount": 0,
            "approval_url": FRONT_URL + KAKAO_PAY_APPROVAL_URL,
            "cancel_url": FRONT_URL + KAKAO_PAY_CANCEL_URL,
            "fail_url": FRONT_URL + KAKAO_PAY_CANCEL_URL,
        }

        res = requests.post(URL, headers=headers, params=data)

        """
        세션,쿠키,캐싱등을 사용할 수 있지만 프론트 부재로 일단 tid 및 url등을
        DB에 넣는 방식으로 진행
        """
        payment_try = Payments(
            pk=id,
            buyer=user,
            product_name=product_name,
            total_price=total_amount,
            payment_date=datetime.datetime.now(),
            kakao_pay_url=res.json()["next_redirect_pc_url"],
            kakao_tid=res.json()["tid"],
        )
        payment_try.save()
        payment_try = Payments.objects.get(pk=id)

        next_url = res.json()["next_redirect_pc_url"]
        self.next_url = next_url

        return self.next_url

    def kakao_pay_approval(self, request, id, tid, user):
        URL = "https://kapi.kakao.com/v1/payment/approve"

        headers = {
            "Authorization": "KakaoAK " + KAKAO_PAY,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        print(request)
        data = {
            "cid": "TC0ONETIME",  # test code
            "tid": tid,
            "partner_order_id": id,
            "partner_user_id": user,
            "pg_token": request.data["pg_token"],
        }
        res = requests.post(URL, headers=headers, params=data).json()
        print(res)

        try:
            payment = Payments.objects.get(pk=id, paid=False)
            payment.paid = True
            payment.payment_type = "카카오페이"
            payment.payment_date = res["approved_at"]
            payment.save()
        except:
            print("Kakao pay approval fail")

    def __str__(self):
        return self.next_url
