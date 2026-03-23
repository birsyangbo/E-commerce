from django.http import HttpResponse
from django.shortcuts import render
from .models import *
import json
import hmac
import hashlib
import base64
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def success_esawa(request):
    encoded_data = request.GET.get("data")
    if not encoded_data:
        return HttpResponse("Invalid response", status=400)
    # Step 1: Decode Base64 → JSON
    try:
        decoded_json = base64.b64decode(encoded_data).decode("utf-8")
        payload = json.loads(decoded_json)
    except Exception:
        return HttpResponse("Invalid data", status=400)
    # Step 2: Verify Signature
    try:
        signed_fields = payload["signed_field_names"].split(",")
        # Build message in the order of signed_fields excluding 'signed_field_names'
        message = ",".join([f"{field}={payload[field]}" for field in signed_fields])
        # Use Test Secret Key
        secret_key = "8gBm/:&EnhH.1/q" # Test mode key
        expected_signature = base64.b64encode(
        hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
        ).decode()
        # Compare signature (strip '=' padding for safety)
        if expected_signature.rstrip('=') != payload["signature"].rstrip('='):
    # Debugging: show mismatch
            print("Message to sign:", message)
            print("Expected signature:", expected_signature)
            print("Payload signature:", payload["signature"])
            return HttpResponse("Invalid signature", status=400)
    except KeyError as e:
        return HttpResponse(f"Missing field: {e}"
    , status=400)
    print("check data",payload)
    txn,created=Transaction.objects.get_or_create(transaction_uuid=payload['transaction_uuid'],
    transaction_code=payload['transaction_code'],product_code=payload['product_code'],total_amount=payload['total_amount'],user=request.user,status=payload['status'])

    order,created=Order.objects.get_or_create(transaction_code=payload['transaction_code'],user=request.user,status=payload['status'])
    cart=request.session.get('cart')
    for item in cart.values():
        Order_item.objects.get_or_create(order=order,product_id=item['product_id'],price=item['price'],quantity=item['quantity'])

    request.session['cart']={}
    return render(request, 'success_esewa.html',{'txn':txn})

def failure_payment(request):
    return render(request, 'failure_esewa.html')