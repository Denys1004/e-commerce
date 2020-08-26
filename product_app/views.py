from django.shortcuts import render, redirect
from product_app.models import *
from django.contrib.auth.decorators import login_required
from login_app.models import *
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    return redirect('/login/login')


def store(request):
    if 'user_id' in request.session:
        cur_user = User.objects.get(id = request.session["user_id"]) 
        if len(cur_user.cart.cart_items.all()) > 0:
            num_items_in_cart = cur_user.cart.total_quantity
            products = Product.objects.all()								
            paginator = Paginator(products, 3)									
            page = request.GET.get('page')													
            products = paginator.get_page(page)			
            context = {
                'num_items_in_cart':num_items_in_cart,
                'products' : products
            }
            return render(request, 'store.html', context)
        else:
            num_items_in_cart = cur_user.cart.total_quantity
            products = Product.objects.all()								
            paginator = Paginator(products, 3)									
            page = request.GET.get('page')													
            products = paginator.get_page(page)
            context = {
                'products' : products
            }
            return render(request, 'store.html', context)
    else:
        num_items_in_cart = cur_user.cart.total_quantity
        products = Product.objects.all()								
        paginator = Paginator(products, 3)									
        page = request.GET.get('page')													
        products = paginator.get_page(page)
        context = {
            'products' : products
        }
        return render(request, 'store.html', context)




def cart(request):
    cur_user = User.objects.get(id = request.session['user_id'])
    cart_items = cur_user.cart.cart_items.all()
    for item in cart_items:
        print('PRICE: ', item.item_cost)
    context = {
        'num_items_in_cart':cur_user.cart.total_quantity,
        'cur_user':cur_user
    }
    return render(request, 'cart.html', context)




def checkout(request):
    cur_user = User.objects.get(id = request.session['user_id'])
    context = {
        'num_items_in_cart':cur_user.cart.total_quantity,
        'cur_user':cur_user
    }
    return render(request, 'checkout.html', context)




def item(request, id):
    product=Product.objects.get(id=id)
    cur_rating = product.average
    first_image = product.images.all()[1]
    additional_images = product.images.all().exclude(id=first_image.id)
    cur_user = User.objects.get(id = request.session['user_id'])
    context = {
        'product':product,
        'first_image':first_image,
        'additional_images':additional_images,
        'num_items_in_cart':cur_user.cart.total_quantity,
        'all_reviews':product.reviews.all(),
        'cur_user':cur_user,
        'star_count':range(cur_rating)
    }
    return render(request, 'item.html', context)



def create_new_product(request):
    if request.method == "GET":
        context={
            'catergories':Category.objects.all()
        }
        return render(request, 'create_product.html', context)
    else:
        new_product = Product.objects.create_product(request.POST, request.FILES)
        return redirect('/store')



def all_products(request):
    cur_user = User.objects.get(id = request.session['user_id'])
    context = {
        'all_products':Product.objects.all(),
        'num_items_in_cart':cur_user.cart.total_quantity
    }
    return render(request, 'all_products.html', context)



def add_to_cart(request, id):
    product = Product.objects.get(id = id)
    cart = User.objects.get(id = request.session['user_id']).cart
    found_item = False

    all_cart_items = cart.cart_items.all()
    for item in all_cart_items:
        if item.product.id == product.id:
            found_item = True
            break

    if found_item:
        item.quantity += 1
        item.total_item_cost = item.product.price * item.quantity
        cart.total_cost += item.product.price
        cart.total_quantity+=1
        cart.save()
        item.save()
        return redirect('/store')
    else:
        cart_item = CartItem.objects.create(
            product = product,
            cart = cart,
            item_cost = product.price,
            total_item_cost = product.price
        )
        cart.total_cost += product.price
        cart.total_quantity+=1
        cart.save()
        return redirect('/store')




def edit(request, product_id):
    if request.method == "GET":
        context = {
            'needed_product': Product.objects.get(id = product_id)
        }
        return render(request, 'edit_product.html', context)
    else:
        updated_product = Product.objects.update_product(request.POST, request.FILES, product_id)
        return redirect(f'/edit/{product_id}')


# update quantity
def update_quantity(request, product_id):
    current_item = CartItem.objects.get(id=product_id)
    current_item_old_qty = current_item.quantity
    item_old_total_cost = current_item.total_item_cost

    current_item.quantity = int(request.POST['qty'])

    current_item.total_item_cost  = current_item.quantity * current_item.item_cost
    current_item.save()

    cur_user = User.objects.get(id = request.session['user_id'])
    cart = User.objects.get(id = request.session['user_id']).cart

    cart.total_quantity = (cart.total_quantity - current_item_old_qty) + current_item.quantity
    cart.save()
    cur_user.save()

    cur_user.cart.total_cost = (cur_user.cart.total_cost - item_old_total_cost) + current_item.total_item_cost
    cur_user.cart.save()
    if current_item.quantity == 0:
        current_item.delete()
<<<<<<< HEAD

    return redirect('/cart') 
=======
    
    context = {
        'num_items_in_cart':cur_user.cart.total_quantity,
        'cur_user':cur_user,
        'product':current_item
    }

    return render(request, 'cart_partial.html', context)
>>>>>>> 242fa30ca95a1dd8eaef9c4bf2e835e1330532f8



def review(request, product_id):
    product = Product.objects.get(id = product_id)
    poster = User.objects.get(id = request.session['user_id'])
    if 'rating' in request.POST:
        product.stars = product.stars + int(request.POST['rating'])
        product.count = product.count + 1
        product.average = product.stars / product.count 
        product.save()
        Review.objects.create(review = request.POST['review'], poster=poster, product = product, stars = int(request.POST['rating']))
        return redirect(f'/item/{product.id}')
    else:
        Review.objects.create(review = request.POST['review'], poster=poster, product = product)
        return redirect(f'/item/{product.id}')



def delete_review(request, product_id, review_id):
    review = Review.objects.get(id = review_id)
    if review.stars:
        product = Product.objects.get(id = product_id)
        product.count = product.count - 1
        product.stars = product.stars - review.stars
        product.average = product.stars / product.count
        product.save()
    review.delete()
    return redirect(f'/item/{product_id}')


def delete_photo(request, product_id, image_id):
    product = Product.objects.get(id = product_id)
    image = Image.objects.get(id = image_id)
    image.delete()
    return redirect(f'/edit/{product_id}')


def delete_cart_item(request, cart_item_id):
    cart_item = CartItem.objects.get(id = cart_item_id)
    # print("*" * 30)
    cart = Cart.objects.get(id = request.session['cart_id'])
    cart.total_quantity = cart.total_quantity - cart_item.quantity
    cart.total_cost = cart.total_cost - (cart_item.item_cost*cart_item.quantity)
    cart.save()
    cart_item.delete()
    return redirect('/cart')




def payment(request):
    return redirect('/payment_page')

def payment_page(request):
    context = {
        
    }
    return render(request, 'payment.html', context)


def delete(request, id):
    product = Product.objects.get(id = id)
    product.delete()
    return redirect('/all_products')

# search bar in store
def search_product(request):
    products = Product.objects.all()
  
    search_query = request.GET.get('query')
    if search_query != '' and search_query is not None:
        searched_query = products.filter(name__contains = search_query)
        context = {
            'searched_query': searched_query
        }
    return render(request, 'search_result.html', context)




