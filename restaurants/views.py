from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
import json
import bcrypt
from .models import User, Category, TransactionType, Location, Restaurant, Review
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from restaurant_proj.settings import API_KEY
import requests

def dashboard(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        rest_list = Restaurant.objects.filter(location_id__in=Location.objects.filter(city__in=Location.objects.filter(id__in=user.favorites.all().values("location_id").distinct()).values("city").distinct(), state__in=Location.objects.filter(id__in=user.favorites.all().values("location_id").distinct()).values("state").distinct())).exclude(favorites=user).order_by('-rating', 'review_count', '-location__city', 'price')
        page = request.GET.get('page', 1)
        paginator = Paginator(rest_list, 50)
        try:
            restaurants = paginator.page(page)
        except PageNotAnInteger:
            restaurants = paginator.page(1)
        except EmptyPage:
            restaurants = paginator.page(paginator.num_pages)
        
        context = {
            'user': user,
            'restaurants': restaurants,
            'states': Location.objects.all().values_list('state', flat=True).distinct(),
        }
        return render(request, 'dashboard.html', context)
    return redirect("/")

def show_restaurant(request, id):
    restaurant = Restaurant.objects.filter(id=id)
    if restaurant:
        restaurant = restaurant[0]
        reviews = restaurant.restaurant_reviews.order_by('-updated_at')
        
        if restaurant:
            rel_rests = related_restaurants(restaurant)
            context = {
                'restaurant' : restaurant,
                'reviews': reviews,
                'stars': range(1, 6),
                'user': User.objects.get(id=request.session['user_id']),
                'related_restaurants': rel_rests,
            }

        return render(request, 'restaurant_profile.html', context)

def category_explore(request):
    user = User.objects.filter(id=request.session['user_id'])
    if user:
        if request.method == "GET":
            context = {}
            city = request.GET.get("city")
            state = request.GET.get("state")
            category = request.GET.get("category")
            context['restaurants'] = None
            context['user'] = user[0]
            context['states'] = Location.objects.all().values_list('state', flat=True).distinct()
            if city and state and category:
                if category.strip() == 'all':
                    restaurants = Restaurant.objects.filter(location_id__in=Location.objects.filter(city=city)).order_by("rating")
                else:
                    restaurants = Restaurant.objects.filter(location_id__in=Location.objects.filter(city=city), categories__in=Category.objects.filter(title=category)).order_by("name")
                context['restaurants'] = restaurants
                return render(request, 'restaurant_explore.html', context)
    return redirect("/dashboard/explore")

def related_restaurants(restaurant):
    categories = restaurant.categories.all()
    if categories:
        rel_rests = Restaurant.objects.filter(location_id__in=(Location.objects.filter(city=restaurant.location.city, state=restaurant.location.state)), categories__in=restaurant.categories.all())
        
    else:
        rel_rests = Restaurant.objects.filter(location_id__in=(Location.objects.filter(city=restaurant.location.city, state=restaurant.location.state)))
    return rel_rests.distinct().order_by('rating', 'review_count', 'price')[:10]

def explore(request):
    if "user_id" in request.session:
        user = User.objects.get(id=request.session['user_id'])
        context = {}
        if user:
            context['restaurants'] = None
            context['user'] = user
            context['states'] = Location.objects.all().values_list('state', flat=True).distinct().order_by('state')
            
            return render(request, 'restaurant_explore.html', context)
    return redirect("/")

def create_review(request, id):
    if "user_id" in request.session:
        if request.method == "POST":
            restaurant = Restaurant.objects.filter(id=id)
            Review.objects.create(creator=User.objects.get(id=request.session['user_id']), title=request.POST['title'], desc=request.POST['desc'], restaurant=restaurant[0], rating=request.POST['rating'])
            return redirect(f"/dashboard/restaurants/show/{id}")
    return redirect("/")

def update_review(request, id):
    if 'user_id' in request.session:
        if request.method == "POST":
            review = Review.objects.filter(id=id)
            if review:
                review = review[0]
                review.title = request.POST['title']
                review.desc = request.POST['desc']
                review.rating = request.POST['rating']
                review.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    return redirect("/")

def delete_review(request, id):
    if request.method == "POST":
        review = Review.objects.filter(id=id)
        if review:
            review[0].delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def favorite(request):
    if request.method == "GET":
        if 'user_id' in request.session:
            restaurant = Restaurant.objects.get(id=request.GET['rest_id'])
            user = User.objects.get(id=request.session['user_id'])
            if request.GET['status'] == "Favorite":
                restaurant.favorites.add(user)
                data = {'status': "Unfavorite"}
            else:
                restaurant.favorites.remove(user)
                data = {'status': "Favorite"}
            restaurant.save()
            return JsonResponse(data)
    return redirect("/")

def show_user(request, id):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        user_prof = User.objects.filter(id=id)
        
        if user:
            context = {
                'user': user,
                'stars': range(1, 6),
                'user_prof': user_prof[0],
                'user_prof_reviews': Review.objects.filter(creator=user_prof[0]).order_by("-updated_at")
            }
            return render(request, 'user_profile.html', context)
    return redirect('/')

def explore_friends(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        friends = user.friends.all()
        user_friends = user.user_friends.all()
        all_friends = friends | user_friends
        all_friends = all_friends.distinct()
        non_friends = User.objects.all().exclude(id__in=all_friends)
        
        context = {
            'user': user,
            'all_friends': all_friends,
            'non_friends': non_friends,
            }
        return render(request, 'explore_friends.html', context)
    return redirect("/")

def add_friend(request, friend_id):
    if request.method == "POST":
        user = User.objects.filter(id=request.session['user_id'])
        friend = User.objects.filter(id=friend_id)
        if user and friend:
            user = user[0]
            friend = friend[0]
            user.friends.add(friend)
            friend.friends.add(user)
            user.save()
            friend.save()
            return redirect(f"/dashboard/friends/explore")
    return redirect("/dashboard")

def remove_friend(request, friend_id):
    if request.method == "POST":
        if 'user_id' in request.session:
            user = User.objects.filter(id=request.session['user_id'])
            friend = User.objects.filter(id=friend_id)
            if user and friend:
                user = user[0]
                friend = friend[0]
                user.friends.remove(friend)
                friend.friends.remove(user)
                friend.save
                user.save()
                return redirect(f"/dashboard/friends/explore")
    return redirect("/dashboard")

def friend(request, friend_id):
    friend = User.objects.filter(id=friend_id)
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        if friend:
            friend = friend[0]
        if friend in user.friends.all() or user.user_friends.all():
            user.friends.remove(friend)
            friend.friends.remove(user)
            user.save()
            friend.save()
            status = 'Add Friend'
        else:
            user.friends.add(friend)
            friend.friends.add(user)
            user.save()
            friend.save()
            status = 'Remove Friend'
        return JsonResponse({'status': status})

def new_loc_search(request):
    user = User.objects.filter(id=request.session['user_id'])
    if user:
        if request.method == "GET":
            context = {}
            search_term = request.GET.get("rest_search_term")
            if search_term == "":
                search_term="food"
            city = request.GET.get("rest_search_loc")
            context['user'] = user[0]
            if city:
                context['states'] = Location.objects.all().values_list('state', flat=True).distinct()
                context['restaurants'] = new_restaurant_query(search_term, city)
                return render(request, 'restaurant_explore.html', context)
                
    return redirect("/dashboard/explore")

def new_restaurant_query(search_term, location):
    api_key = API_KEY
    url='https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'Bearer %s' % api_key}
    # In the dictionary, term can take values like food, cafes or businesses like McDonalds
    params = {'term':search_term,'location':location, 'limit': 50}
    req=requests.get(url, params=params, headers=headers)
    data = json.loads(req.text)
    rests_to_return = []
    if data:
        restaurants = data['businesses']
        for test_rest in restaurants:
            if 'price' not in test_rest:
                test_rest['price'] = '$'
            if test_rest['image_url'] == "":
                test_rest['image_url'] = 'https://s3-media1.fl.yelpcdn.com/bphoto/UaybPI6fcFGFsvftdW54JA/o.jpg'
            is_in_db = Restaurant.objects.filter(name=test_rest['name'], url=test_rest['url'])
            if is_in_db:
                rests_to_return.append(is_in_db[0])
            else:
                new_restaurant = Restaurant.objects.create(creator=User.objects.get(id=1), name=test_rest['name'], alias=test_rest['alias'], is_closed=test_rest['is_closed'], url=test_rest['url'], review_count=test_rest['review_count'], rating=test_rest['rating'], latitude=test_rest['coordinates']['latitude'], longitude=test_rest['coordinates']['longitude'], phone_number=test_rest['display_phone'], price=test_rest['price'])
                new_restaurant.image_url = test_rest['image_url']
                # new_restaurant.get_remote_image()
                loc_data = test_rest['location']
                new_location = Location.objects.create(address1=loc_data['address1'], city=loc_data['city'], zip_code=loc_data['zip_code'], country=loc_data['country'], state=loc_data['state'])
                new_restaurant.location = new_location
                transaction_types = test_rest['transactions']
                for t in transaction_types:
                    t_type = TransactionType.objects.filter(title=t)
                    if not t_type:
                        new_t_type = TransactionType.objects.create(title=t)
                    else:
                        new_t_type = t_type[0]
                    new_restaurant.transaction_types.add(new_t_type)

                category_types = test_rest['categories']
                for c in category_types:
                    c_type = Category.objects.filter(title=c['title'])
                    if not c_type:
                        new_c_type = Category.objects.create(title=c['title'], alias=c['alias'])
                    else:
                        new_c_type = c_type[0]
                    new_restaurant.categories.add(new_c_type)
                new_restaurant.save()
                rests_to_return.append(new_restaurant)
    return rests_to_return

def state_change(request):
    if request.method == "GET":
        data = {
            'cities': list(Location.objects.filter(state=request.GET['state']).values_list('city', flat=True).distinct().order_by('city')),
        }
        return JsonResponse(data)

def city_change(request):
    categories = Category.objects.filter(Category__in=(Restaurant.objects.filter(location_id__in=Location.objects.filter(city=request.GET['city'])))).distinct().order_by('title')
    categories = [c.title for c in categories]
    data = {
        'categories': categories,
    }
    return JsonResponse(data)

def new_loc_autocomplete(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Location.objects.filter(Q(city__contains=q)).values_list('city').distinct()
        results = []
        if search_qs:
            for r in search_qs[0:10]:
                results.append(r[0])
        else:
            results.append("No Existing Location")
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def autocomplete_model(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Restaurant.objects.filter(Q(name__contains=q))
        results = []
        for r in search_qs[0:10]:
            results.append(r.name)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def search(request):
    if request.method == "GET":
        restaurant = Restaurant.objects.filter(name=request.GET['rest_search'])
        if restaurant:
            return redirect(f"/dashboard/restaurants/show/{restaurant[0].id}")
        return redirect("/dashboard/explore")



def edit_profile(request):
    if request.method == "POST":
        if 'user_id' in request.session:
            user = User.objects.get(id=request.session['user_id'])
            errors = User.objects.register_validator(request.POST, edit_profile=True)
            del_username_error, del_email_error = False, False
            for k in errors.keys():
                if k == "username":
                    if user.username == request.POST['username']:
                        del_username_error = True
                        
                if k == 'email':
                    if user.email == request.POST['email']:
                        del_email_error = True
            if del_username_error:    
                del errors['username']
            if del_email_error:
                del errors['email']
            if len(errors) == 0:               
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.username = request.POST['username']
                user.email = request.POST['email']
                user.birthday = request.POST['birthday']
                user.save()
            return JsonResponse(errors)
    return redirect("/dashboard")
        

def change_password(request):
    if request.method == "POST":
        if 'user_id' in request.session:
            errors = User.objects.register_validator(request.POST, change_password=True)
            mydict = {}
            if len(errors) > 0:
                for k, v in errors.items():
                    # messages.error(request, v, extra_tags=k)
                    mydict[k] = v
            else:
                password = request.POST['password']
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                user = User.objects.get(id=request.session['user_id'])
                user.password = pw_hash
                user.save()
            return JsonResponse(errors)
    return redirect("/dashboard")


def test(request):
    context = {'user': User.objects.get(id=request.session['user_id'])}
    return render(request, 'test.html', context)