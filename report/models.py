from django.db import models

from django.db import models


"""
reporter : 신고자
report_type : 신고 유형 (PROFANITY:욕설, ADVERTISEMENT:광고, SPAM:스팸 및 도배)
report_at : 신고 시간
report_content : 신고 내용 (채팅방에서 불러오기) - ForeignKey로 연결 할지 or TextField로 저장 할지
"""


class Report(models.Model):
    class ReportTypeChoices(models.TextChoices):
        PROFANITY = "profanity", "Profanity"
        ADVERTISEMENT = "advertisement", "Advertisement"
        SPAM = "spam", "Spam"

    reporter = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        related_name="reporter",
    )
    report_type = models.CharField(
        choices=ReportTypeChoices.choices,
        max_length=30,
        blank=False,
    )
    report_at = models.DateTimeField(
        auto_now_add=True,
        ordering=["-report_at"],
    )
    report_content = models.TextField()

    def __str__(self):
        return self.report_type

    class Meta:
        verbose_name_plural = "Report"