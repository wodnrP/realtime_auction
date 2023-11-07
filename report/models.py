from django.db import models

"""
reporter : 신고자
report_criminal : 신고 당한 사람 (피의자)
report_type : 신고 유형 (PROFANITY:욕설, ADVERTISEMENT:광고, SPAM:스팸 및 도배)
report_at : 신고 시간
report_content : 신고 내용 (채팅방에서 불러오기)
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
        null=True,
    )

    report_criminal = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        related_name="report_criminal",
        null=True,
    )

    report_chatting_room = models.ForeignKey(
        "chat.Chatting",
        on_delete=models.CASCADE,
        related_name="report_chatting_room",
        null=True,
        blank=True,
    )

    report_type = models.CharField(
        choices=ReportTypeChoices.choices,
        max_length=30,
        blank=False,
    )

    report_at = models.DateTimeField(
        auto_now_add=True,
    )

    report_content = models.TextField()

    def __str__(self):
        return self.report_type

    class Meta:
        verbose_name_plural = "Report"
        ordering = ["-report_at"]
