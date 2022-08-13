from django.contrib import admin
from .models import Category, Product, Banner


# Register your models here.
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['img1', 'img2', 'img3']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'photo', ]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'photo',
                    'photo1', 'photo2', 'photo3', 'price',
                    'available', 'created', 'updated', ]
    list_filter = ['available', 'created', 'updated', ]
    list_editable = ['price', 'available', ]
    prepopulated_fields = {'slug': ('name',)}
