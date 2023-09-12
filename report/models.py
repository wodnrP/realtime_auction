from djongo import models

"""
reporter : 신고자
report_type : 신고 유형 (PROFANITY:욕설, ADVERTISEMENT:광고, SPAM:스팸 및 도배)
report_at : 신고 시간
report_chatting_room : 신고된 채팅방 / 경매 채팅방(auction) 참조
report_suspect : 신고 대상자 (신고당한 사람)
report_content : 신고 내용 (채팅방에서 불러오기)
"""


class Report(models.Model):
    class ReportTypeChoices(models.TextChoices):
        PROFANITY = "profanity", "욕설"
        ADVERTISEMENT = "advertisement", "광고"
        SPAM = "spam", "스팸 및 도배"

    reporter = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        related_name="reporter",
        null=True,
    )
    report_type = models.CharField(
        choices=ReportTypeChoices.choices,
        max_length=30,
        blank=False,
    )
    report_at = models.DateTimeField(
        auto_now_add=True,
    )
    report_chatting_room = models.ForeignKey(
        "auction.Auction",
        on_delete=models.SET_NULL,
        null=True,
        default=None,
    )
    report_suspect = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="suspects",
    )
    report_content = models.TextField()

    def __str__(self):
        return self.report_type

    class Meta:
        verbose_name_plural = "Reports"
        ordering = ["-report_at"]