from django.shortcuts import redirect, render
from urllib3 import request
from .models import OfferProduct,Category,Product,SubCategory,Review
from .forms import ReviewForm
from django.db.models import Count,Prefetch,Avg
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import hmac
import hashlib
import uuid
import base64
from cart.cart import Cart
# Create your views here.
def home(request):

    offer=OfferProduct.objects.filter(is_active=True)
    category=Category.objects.annotate(subcategory_count=Count('subcategory')).prefetch_related(
        Prefetch('subcategory_set', queryset=SubCategory.objects.annotate(product_count=Count('product')))
    )
    subcateid=request.GET.get('subcategory')
    min=request.GET.get('min')
    max=request.GET.get('max')

    if subcateid and min and max:
        product=Product.objects.filter(subcategory=subcateid, price__range=(min, max))
    elif subcateid:
        product=Product.objects.filter(subcategory=subcateid)

    else:
        product=Product.objects.all()

    paginator=Paginator(product, 3)
    num_p=request.GET.get('page')
    data=paginator.get_page(num_p)
    total=paginator.num_pages
    
    context={
        'offer':offer,
        'category':category,
        'product':product,
        'data':data,
        'num':[i+1 for i in range(total)]
    }
    return render(request, 'core/index.html', context)

def detail(request, id):
    product=get_object_or_404(Product, id=id)
    review=product.reviews.all()
    review_count=product.reviews.all().count()
    review_avg=review.aggregate(Avg('rating'))['rating__avg']
    form=ReviewForm()
    if request.method=='POST':
        form=ReviewForm(data=request.POST)
        if form.is_valid():
            review=form.save(commit=False)
            review.user=request.user
            review.product=product
            review.save()
            return redirect('product_details', id=product.id)
    context={
        'product':product,
        'form':form,
        'review':review,
        'range':range(1, 6),
        'review_count':review_count,
        'review_avg':round(review_avg) if review_count else 0
    }
    return render(request, 'core/product_detail.html', context)







'''. cart ko laagi'''

@login_required(login_url="login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")
def generate_signature(data, secret):
    # signed_field_names must be included in the payload
    signed_fields = data["signed_field_names"].split(",")
    # Create message string in exact order
    message = ",".join([f"{field}={data[field]}" for field in signed_fields])
    signature = hmac.new(
    secret.encode("utf-8"),
    message.encode("utf-8"),
    hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode("utf-8")

@login_required(login_url="login")
def cart_detail(request):
    cart=request.session.get('cart')
    amount=0
    for item in cart.values():
        amount+=item['quantity']*float(item['price'])
        amount=round(amount, 2)
        tax_amount=round((amount*0.13), 2)
        total_amount=round(amount+tax_amount, 2)
        product_code="EPAYTEST"
        secret_key="8gBm/:&EnhH.1/q"
        data = {
            "amount": amount,
            "tax_amount": tax_amount,
            "total_amount": total_amount,
            "transaction_uuid": str(uuid.uuid4()),
            "product_code": product_code,
            "product_service_charge": 0,
            "product_delivery_charge": 0,
            "success_url": "http://127.0.0.1:8000/payments/success_url/",
            "failure_url": "http://127.0.0.1:8000/payments/failure_url/",
            "signed_field_names": "total_amount,transaction_uuid,product_code"
            }
        data['signature'] = generate_signature(data, secret_key)
    return render(request, 'core/cart.html', data)