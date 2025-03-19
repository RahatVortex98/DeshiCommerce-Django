from django.shortcuts import render,get_object_or_404
from .models import  Product
from category.models import Category
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator




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




def product_detail(request,category_slug, product_slug):
    product =get_object_or_404(Product,slug=product_slug, category__slug=category_slug)
    return render(request,'store/product_detail.html',{'product':product})



def search(request):
    keyword = request.GET.get('keyword', '').strip()  # Get the keyword and remove spaces
    products = Product.objects.none()  # Default: No products

    if keyword:
        products = Product.objects.filter(name__icontains=keyword)  # Search by product name
        product_count = products.count()

    context = {
        'products': products,  
        'keyword': keyword,  # Keep the search term in the input field
        'product_count':product_count,
    }
    return render(request, 'store/store.html', context)  # Use store.html to display results