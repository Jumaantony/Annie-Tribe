from django.db import models
from django.urls import reverse

from account.models import User

from cloudinary.models import CloudinaryField
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class Banner(models.Model):
    img1 = CloudinaryField(blank=False)
    img2 = CloudinaryField(blank=False)
    img3 = CloudinaryField(blank=True)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    photo = CloudinaryField(blank=False)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=250, blank=False)
    slug = models.SlugField(max_length=200)
    category = models.ForeignKey(Category, related_name='products',
                                 on_delete=models.CASCADE, null=True)
    photo = CloudinaryField()
    photo1 = CloudinaryField()
    photo2 = CloudinaryField()
    photo3 = CloudinaryField()
    description = RichTextUploadingField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    users_wishlist = models.ManyToManyField(User, related_name="user_wishlist", blank=True)

    class Meta:
        ordering = ('name',)

    index_together = (('id', 'slug'),)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('products:product_detail',
                       args=[self.id, self.slug])


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Review on {self.product}'

    # return f'Comment by {self.user} on {self.product}'
