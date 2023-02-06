import hashlib
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.postgres.search import SearchVector
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .forms import EmailForm
from .models import Category, Product, Banner
from cart.forms import CartAddProductForm

from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

logger = logging.getLogger(__name__)

mailchimp = Client()
mailchimp.set_config({
    'api_key': settings.MAILCHIMP_API_KEY,
    'server': settings.MAILCHIMP_REGION,
})


# Create your views here.

def mailchimp_ping_view(request):
    response = mailchimp.ping.get()
    return JsonResponse(response)


def subscribe_view(request):
    if request.method == 'POST':
        email = request.POST['subscriber_email']
        try:
            form_email = email

            # member info contains the user information that will be stored in mailchimp
            member_info = {
                'email_address': form_email,
                'status': 'subscribed',
            }
            response = mailchimp.lists.add_list_member(
                settings.MAILCHIMP_MARKETING_AUDIENCE_ID,
                member_info)
            logger.info(f'API call successful: {response}')
            return redirect('products:subscribe_success')

        except ApiClientError as error:
            logger.error(f'An exception occurred: {error.text}')
            return redirect('products:subscribe_fail')


def subscribe_success_view(request):
    return render(request, 'newsletter/message.html', {
        'title': 'Successfully subscribed',
        'message': 'Yay, you have been successfully subscribed to our mailing list.',
        'unsubscribe-link': '<a href "{% "product:unsubscribe" %}"> unsubscribe </a>'
    })


def subscribe_fail_view(request):
    return render(request, 'newsletter/message.html', {
        'title': 'Failed to subscribe',
        'message': 'Oops, something went wrong.',
    })


def unsubscribe_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            try:
                form_email = form.cleaned_data['email']
                # hashing the user's email using md5 to generate a subscriber hash will allow to manipulate the
                # user's data
                form_email_hash = hashlib.md5(form_email.encode('utf-8').lower()).hexdigest()

                # member_update used to change the user data
                member_update = {
                    'status': 'unsubscribed',
                }
                response = mailchimp.lists.update_list_member(
                    settings.MAILCHIMP_MARKETING_AUDIENCE_ID,
                    form_email_hash,
                    member_update,
                )
                logger.info(f'API call successful: {response}')
                return redirect('products:unsubscribe_success')

            except ApiClientError as error:
                logger.error(f'An exception occurred: {error.text}')
                return redirect('products:unsubscribe_fail')

    return render(request, 'newsletter/unsubscribe.html', {
        'form': EmailForm(),
    })


def unsubscribe_success_view(request):
    return render(request, 'newsletter/message.html', {
        'title': 'Successfully unsubscribed',
        'message': 'You have been successfully unsubscribed from our mailing list.',
    })


def unsubscribe_fail_view(request):
    return render(request, 'newsletter/message.html', {
        'title': 'Failed to unsubscribe',
        'message': 'Oops, something went wrong.',
    })


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

    """ordered_items = OrderItem.objects.filter(user=request.user)
    if user_passes_test(lambda order_items: ordered_items.order.order_status):
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
            review_form = ReviewForm()"""

    return render(request, 'product_detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        form_data = {
            'name': name,
            'email': email,
            'message': message,
        }
        message = '''
                From:\n\t\t{}\n
                Message:\n\t\t{}\n
                Email:\n\t\t{}\n
                '''.format(form_data['name'], form_data['message'], form_data['email'], )
        send_mail('You got a mail!', message, '', ['jumaanton98@gmail.com'])
        messages.success(request, 'Your email has been sent successfully. We will reach out to you as soon as possible')
        return render(request, 'contact.html')

    else:
        return render(request, 'contact.html', {})


def search(request):
    if request.method == 'GET':
        query = request.GET['search_query']
        search_results = Product.objects.filter(available=True). annotate(
            search=SearchVector('name', 'description'), ).filter(search=query)
        return render(request, 'search.html', {'query': query,
                                               'search_results': search_results, })
