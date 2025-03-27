from django.shortcuts import redirect, render,get_object_or_404

from orders.models import OrderProduct
from store.forms import ReviewForm
from .models import  Product, ReviewRating
from category.models import Category
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

from django.contrib import messages



def store(request,category_slug=None):

    categories =None
    products =None

    if category_slug != None:
        categories =get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=categories,is_available=True).order_by('id')

        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        product_count=products.count()
    else:
        products = Product.objects.all().filter(is_available=True)

        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        product_count = products.count()

    context ={
        'products':paged_products,
        'product_count':product_count
    }
    return render(request,'store/store.html',context)




def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)

    # Get approved reviews for this product
    reviews = ReviewRating.objects.filter(product=product, status=True)

    context = {
        'product': product,
        'reviews': reviews
    }
    return render(request, 'store/product_detail.html', context)




def search(request):
    keyword = request.GET.get('keyword', '').strip()
    products = Product.objects.none()  # Default: No products
    product_count = 0

    if keyword:
        products = Product.objects.filter(name__icontains=keyword)  
        product_count = products.count()

    # Fix the review query: Get reviews for all found products
    reviews = ReviewRating.objects.filter(product__in=products, status=True)

    context = {
        'products': products,  
        'keyword': keyword,
        'product_count': product_count,
        'reviews': reviews,
    }
    return render(request, 'store/store.html', context)



def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER', '/')  # Get the referring URL or home page
    
    if request.method == "POST":
        try:
            # Check if a review already exists
            reviews = ReviewRating.objects.get(user=request.user, product_id=product_id)
            form = ReviewForm(request.POST, instance=reviews)  # Update the review
            form.save()
            messages.success(request,'Thank you!Your new review has been updated!')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            # Create a new review if it doesn't exist
            form = ReviewForm(request.POST)
        
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product_id = product_id
            review.ip = request.META.get('REMOTE_ADDR')  # ✅ Fixed IP extraction
            review.save()
            
            messages.success(request, "Thank you! Your review has been submitted.")
        else:
            print("Form Errors:", form.errors)  # Debugging
            messages.error(request, "Something went wrong. Please try again.")

        return redirect(url)  # ✅ Ensure we always return a response

    return redirect(url)  # ✅ Handle non-POST requests

    