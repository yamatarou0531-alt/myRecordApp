from django.db import models

# Create your models here.

class SakeRecord(models.Model):
    title = models.CharField("銘柄名", max_length=200)
    brewery = models.CharField("蔵元", max_length=100, blank=True)
    sake_type = models.CharField("種類（純米・吟醸など）", max_length=50, blank=True)
    rating = models.IntegerField("評価（1〜5）", default=3)
    memo = models.TextField("メモ", blank=True)
    image = models.ImageField("写真", upload_to="sake/", blank=True, null=True)
    recorded_at = models.DateTimeField("記録日", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-recorded_at"]