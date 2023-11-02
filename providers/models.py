from django.db import models
import uuid

class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20,decimal_places=2, default=0)
#Provider
class Provider(models.Model):
    id: models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emprendedor_id = models.UUIDField(default=uuid.uuid4)
    cedula = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    email = models.TextField(blank=True)
    phone = models.CharField(max_length=16)
    address = models.CharField(max_length=264)
    articles = models.ManyToManyField(Article)

    def __str__(self):
        return id