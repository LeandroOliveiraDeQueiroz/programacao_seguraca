from django.db import models

# Create your models here.
class QRCode(models.Model):
    user_id = models.IntegerField()
    url = models.CharField(max_length=200)
    qrcode = models.ImageField()