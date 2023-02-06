import json
import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from orders.models import OrderItem, Order
from .forms import MpesaPhoneForm
from .models import MpesaPayment

from .mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
import braintree
from requests.auth import HTTPBasicAuth

# Create your views here.
# instantiating braintree payment gateway

gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


@login_required
def payment_options(request):
    order_id = request.session.get('order_id')
    order = Order.objects.get(id=order_id)
    ordered_items = OrderItem.objects.filter(order=order_id)

    return render(request, 'payment_options.html',
                  {'order': order,
                   'ordered_items': ordered_items})


@login_required
def card_payment(request):
    order_id = request.session.get('order_id')
    order = Order.objects.get(id=order_id)
    ordered_items = OrderItem.objects.filter(order=order_id)
    total_cost_after_discount = order.get_total_cost_after_discount()

    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)

        # create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{total_cost_after_discount:.2f}',
            'payment_method_nonce': nonce,
            'options': {'submit_for_settlement': True}
        })

        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store unique transaction id
            order.braintree_id = result.transaction.id
            order.save()

            return redirect('payment:payment_done')
        else:
            return redirect('payment:payment_canceled')
    else:
        # generate token
        client_token = gateway.client_token.generate()

    return render(request, 'card.html',
                  {'order': order,
                   'ordered_items': ordered_items,
                   'total_cost_after_discount': total_cost_after_discount,
                   'client_token': client_token})


@login_required
def get_access_token(request):
    consumer_key = 'E4yc9wFcaAdeoFe2vxYVzSAT7M2nroQU'
    consumer_secret = 'uWsn21FgMbIzhmE3'

    # url for generating mpesa token
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    # initiate http call to mpesa sandbox
    r = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    # parsing the json string from safaricom
    mpesa_access_token = json.loads(r.text)

    # accessing the mpesa token
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)


@login_required
def mpesa_payment(request):
    # retrieve the current order
    order_id = request.session.get('order_id')
    order = Order.objects.get(id=order_id)
    ordered_items = OrderItem.objects.filter(order=order_id)
    total_cost_after_discount = order.get_total_cost_after_discount()

    if request.method == 'POST':
        phone = request.POST.get('phone')

        # converting to float and str to make the objects JSON serializable
        total_cost_after_discount = int(total_cost_after_discount)

        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

        headers = {"Authorization": "Bearer %s" % access_token}

        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,  # paybill or buy goods till number
            "Password": LipanaMpesaPpassword.decode_password,  # password used to encrypt the requests sent
            "Timestamp": LipanaMpesaPpassword.lipa_time,  # transaction timestamp
            "TransactionType": "CustomerPayBillOnline",  # used to identify the type of transaction
            "Amount": float(total_cost_after_discount),  # the amount you intend to pay
            "PartyA": phone,  # phone number sending the money
            "PartyB": LipanaMpesaPpassword.Business_short_code,  # organization receiving the funds can also be
            # BusinesShortCode
            "PhoneNumber": phone,  # number to receive the STK pin Prompt. can be same as PartA
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",  # valid secure url used to receive notifications
            # from mpesa api. it is the endpoint to which the results will be sent by the mpesa api
            "AccountReference": "Annie Tribe",  # the name of the business
            "TransactionDesc": "Testing stk push"
            # additional information that that can be sent along with the sys's req
        }

        response = requests.post(api_url, json=request, headers=headers)

        order.paid = True
        order.save()
        return redirect('payment:payment_done')
    else:
        form = MpesaPhoneForm()
        return render(request, 'mpesa.html',
                      {'order': order,
                       'ordered_items': ordered_items,
                       'total_cost_after_discount': total_cost_after_discount,
                       'form': form})




@csrf_exempt
def register_urls(request):  # use this method to register our confirmation and validation URL with Safaricom.
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Test_c2b_shortcodee,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://0bd7-154-159-237-225.in.ngrok.io/payment/confirmation/",
               "ValidationURL": "https://0bd7-154-159-237-225.in.ngrok.io/payment/validation/"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)


@csrf_exempt
def call_back(request):
    pass


@csrf_exempt
def validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))


@csrf_exempt
def confirmation(request):
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],
    )
    payment.save()
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))


@login_required
def payment_done(request):
    return render(request, 'payment_done.html')


@login_required
def payment_canceled(request):
    return render(request, 'payment_canceled.html')
