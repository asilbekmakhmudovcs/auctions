from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max



from .models import User, Product, Bids, Comments
from .forms import ProductForm


def index(request):
    products = Product.objects.filter(on_market=True).exclude(owner=request.user.id)
    context = {"products": products}
    
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='login')
def new_product(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.on_market = True
            product.save()
            return HttpResponseRedirect(reverse('watchlist'))
        else:
            return render(request, "auctions/new_product.html", {"form": form})
    else:
        form = ProductForm()
        return render(request, "auctions/new_product.html", {"form": form})
    
    


'''@login_required
def bid(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    highest_bid = Bids.objects.filter(product_id=product_id).aggregate(max_bid=Max('bid_amount'))

    if request.method == 'POST':
        bid_amount = request.POST['bid_amount']
        # Validate bid amount (e.g., check if it's higher than the current highest bid)
        highest_bid = Bids.objects.filter(product_id=product_id).aggregate(max_bid=Max('bid_amount'))

        if int(request.POST["bid_amount"]) <= int(highest_bid) or int(request.POST["bid_amount"]) < int(product.highest_bid):
            return HttpResponse("Bid should be higher try again.")
        # Perform necessary validation and business logic here...
        # For example, you can use Django's form validation or custom logic.

        # Assuming the bid_amount is validated, create a new bid
        new_bid = Bids.objects.create(bidder=request.user, bid_amount=bid_amount)
        product.bids.add(new_bid)
        product.save()
        return HttpResponseRedirect(reverse('index'))
    
    return render(request, 'auctions/bid.html', {'product': product, 'highest_bid': highest_bid})

'''


def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments = Comments.objects.filter(product=product).order_by('-created_at')
    comment_count = 2

    if request.method == "POST": # if request.POST.get("form_type") == bid, else
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        
        # CHECKING IF IT IS FOR COMMENT OR BID
        if request.POST.get("form_type") == 'bid':

            bid_amount = request.POST.get("bid_amount")
            bidder = request.user
            highest_bid = product.get_highest_bid_amount()
            if int(bid_amount) <= int(highest_bid) or int(bid_amount) < product.starting_bid:
                return HttpResponse("Your bid should be higher than current/initial bid.")
            
            if bidder == product.owner:
                return HttpResponse("You can't bid on your own product.")

            try:
                bid = Bids.objects.create(bidder=request.user, bid_amount=bid_amount)
                product.highest_bid = bid
                product.save()
            except Exception as e:
                return HttpResponse(f"Something went wrong!")
                            
            
        elif request.POST.get("form_type") == 'comment':
            
            comment_text = request.POST.get("comment_text")
            try:
                comment = Comments.objects.create(
                    product=product, commenter=request.user,
                    comment_text=comment_text
                )
                comment.save()
            except Exception:
                return HttpResponse("Error")


    context = {'product': product, "comments": comments, "comment_count": comment_count}
    return render(request, 'auctions/bidding.html', context)


@login_required(login_url='login')
def watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    # Fetch products auctioned by the current user and order by time_added in descending order
    user_auctioned_products = Product.objects.filter(owner=request.user, on_market=True).order_by('-time_added')

    return render(request, 'auctions/watchlist.html', {'listings': user_auctioned_products})

@login_required(login_url='login')
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)

#    if len(product) != 1:
#        return HttpResponseRedirect(reverse('index'))
    
    if request.method == "POST":
        product = Product.objects.get(id=pk)
        status = request.POST.get('status')
        if status == '1':
            product.delete()
            return HttpResponseRedirect("watchlist")


    return render(request, 'auctions/delete_product.html', {'product': product})

@login_required(login_url='login')
def sell_product(request, pk):

    product = get_object_or_404(Product, id=pk)

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if request.method == "POST":
        if request.user == product.owner:
            # DONE change currnet product's owner to product.highest_bid.bidder....
            # DONE AttributeError -> when there is no bidder
            try:
                product.owner=product.highest_bid.bidder
                product.on_market = False
                product.save()
            except AttributeError:
                return HttpResponse("Noone bid yet.")
                
        else:
            return HttpResponse("u dont own this shit. Forbidden")
            # redirect to page with explanation message                                                               
    return render(request, 'auctions/selling.html', {'product': product})



@login_required(login_url='login')
def owned_products(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    products = Product.objects.filter(owner=request.user).exclude(on_market=True)

    return render(request, 'auctions/owning.html', {'products': products})

@login_required(login_url='login')
def re_auction(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.user != product.owner:
        return HttpResponse("you cant reaution a prouct you dont own")
    
    form = ProductForm(instance=product)
    return render(request, 'auctions/re_auction.html', {'products': product, "form": form})


