from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .forms import ReviewForm
from .models import Category, Product, Banner
from cart.forms import CartAddProductForm
from orders.views import order_create


# Create your views here.
def index(request):
    banner = Banner.objects.all()
    return render(request, 'index.html', {'banner': banner, })


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    paginator = Paginator(products, 32)
    page_num = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    # cart form
    cart_product_form = CartAddProductForm()

    contxt = {
        'category': category,
        'categories': categories,
        'products': products,
        'page_obj': page_obj,
        'cart_product_form': cart_product_form,
    }
    return render(request, 'product_list.html', contxt)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id,
                                slug=slug)
    # cart form
    cart_product_form = CartAddProductForm()

    if user_passes_test(order_create):
        reviews = product.reviews.filter(active=True)
        new_review = None

        if request.method == 'POST':
            review_form = ReviewForm(data=request.POST)

            if review_form.is_valid():
                new_review = review_form.save(commit=False)
                # assign review to the product
                new_review.product = product

                new_review.save()
        else:
            review_form = ReviewForm()

    return render(request, 'product_detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'reviews': reviews,
                   'new_review': new_review,
                   'review_form': review_form})
