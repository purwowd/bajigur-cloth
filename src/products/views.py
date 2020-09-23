from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime
import time

from .models import Product, Review, Cluster
from .forms import ReviewForm
from .suggestions import update_clusters


def product_list(request):
    products = Product.objects.order_by('-name')
    context = {'products': products}

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = ReviewForm()
    return render(request, 'products/product_details.html', {'product': product, 'form': form})


def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list': latest_review_list}
    return render(request, 'products/reviews.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'products/review_details.html', {'review': review})


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = Review()
        review.product = product
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        update_clusters()
        print(update_clusters)

        return HttpResponseRedirect(reverse('product-detail', args=(product.id, )))
    return render(request, 'products/product_details.html', {'product': product, 'form': form})


def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list': latest_review_list, 'username': username}
    return render(request, 'products/reviews_by_user.html', context)


@login_required
def user_recommendation_list(request):
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('product')
    # user_reviews_product_ids = set(map(lambda x: x.product.id, user_reviews))

    try:
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name
    except Exception:
        update_clusters()
        time.sleep(1)
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name

    user_cluster_other_members = \
        Cluster.objects.get(name=user_cluster_name).users \
        .exclude(username=request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    other_users_reviews = \
        Review.objects.filter(user_name__in=other_members_usernames) \
        .exclude(product__id__in=user_reviews)

    other_users_reviews_product_ids = set(map(lambda x: x.product.id, other_users_reviews))

    product_list = sorted(
        list(Product.objects.filter(id__in=other_users_reviews_product_ids)),
        key=lambda x: x.average_rating(),
        reverse=True
    )

    return render(
        request, 'products/recommendations.html',
        {'username': request.user.username, 'products': product_list}
    )
