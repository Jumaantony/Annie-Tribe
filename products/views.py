from django.shortcuts import render, get_object_or_404
from .models import Category, Product


# Create your views here.
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    contxt = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(request, 'product_list.html', contxt)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id,
                                slug=slug)
    return render(request, 'product_detail.html',
                  {'product': product, })