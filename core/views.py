import random
from itertools import chain
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.http import HttpResponse


@login_required(login_url="signin")
def index(request):

    user_object = User.objects.get(username = request.user)
    user_profile =  Profile.objects.get(user = user_object)

    user_following_list = []
    feed = []
    
    user_following = FollowersCount.objects.filter(follower = request.user.username)
    print(user_following)
    for users in user_following:
        user_following_list.append(users.user)
    print(user_following_list)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user= usernames)
        feed.append(feed_lists)
    
    feed_lists = list(chain(*feed))
    print(feed)
    print(feed_lists)
    

    #mostrar las publicaciones de los usuarios a los que estoy siguiendo
    #posts = Post.objects.all() #ESto .order_by('-created_ad') o reversed en el bucle de template
    #print(posts)
    ################USER SUGESTION STARTS####################################
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    #crea una lista random todas las veces
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []
    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_lists = list(chain(*username_profile_list))

    print(suggestions_username_profile_lists)

    return render(request, "index.html", 
                  {"user_profile":user_profile, 
                   "posts":feed_lists,
                   "suggestions_username_profile_lists":suggestions_username_profile_lists[:4],
                   })


@login_required(login_url="signin")
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    print(post_id)
    post = Post.objects.get(id = post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    print(f"like filter es {like_filter}")

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect('/')


@login_required(login_url="signin")
def upload(request):

    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(
            user=user,
            image=image,
            caption=caption,
        )
        new_post.save()

        return redirect('/')
    else:
        return redirect("/")
    return HttpResponse('<h1>Upload View</h1>')


@login_required(login_url="signin")
def search(request):
    user_object = User.objects.get(username=request.user.username)
    print(user_object)
    user_profile = Profile.objects.get(user=user_object)
    print(user_profile)

    if request.method == "POST":
        username = request.POST['username']
        print(username)
        username_object = User.objects.filter(username__icontains=username)
        print(username_object)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)
        print(username_profile)
        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        print(username_profile_list)
        username_profile_list = list(chain(*username_profile_list))
        print(username_profile_list)

    return render(request, "search.html", {"user_profile":user_profile, "username_profile_list":username_profile_list})


@login_required(login_url="signin")
def profile(request, username):
    print(username)
    user_object = User.objects.get(username=username)
    print(user_object)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=username)
    user_post_length = len(user_posts)

    follower = request.user.username
    #user = username
    print(follower)

    if FollowersCount.objects.filter(follower=follower, user=username).first():
        button_text = "Unfollow"
    else:
        button_text = "Follow"

    user_follower = len(FollowersCount.objects.filter(user=username))
    user_following = len(FollowersCount.objects.filter(follower=username))

    return render(request, "profile.html", 
    {
        "user_profile":user_profile, 
        "user_object":user_object,
        "user_posts":user_posts,
        "user_post_length":user_post_length,
        "button_text":button_text,
        "user_follower":user_follower,
        "user_following":user_following,
    })

@login_required(login_url="signin")
def follow(request):
    if request.method == "POST":
        follower = request.POST['follower']
        user = request.POST['user']
        print(follower)
        print(user)

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()

            return redirect("profile",user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()

            return redirect("profile",user)
    else:
        return redirect('/')
    


@login_required(login_url="signin")
def settings(request):
    print("hola settings")
    user_profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        print(request.FILES.get('image'))
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        else: # if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect("settings")

    return render(request, "setting.html", {"user_profile":user_profile})


def signup(request):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken (Ya cogido)")
                return redirect("signup")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken (Ya cogido)")
                return redirect("signup")
            else:
                user = User.objects.create_user(
                    username=username, 
                    email=email, 
                    password=password
                )
                user.save() #ya tenemos el usuario creado
                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #ahora que tenemos creado un usuario, queremos crear un profile para el nuevo usuario "POR DEFECTO"
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()

                #redirigir al usuario a la pagina de inicio de sesion, pero todavia no la tenemos
                return redirect("settings")

        else:
            messages.info(request, "Password NOT Matching")
            return redirect('signup')
    else:

        return render(request, 'signup.html')


def signin(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        print(user)

        if user is not None: #es lo mismo que (user != None)
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Credentials Invalid")
            return redirect("signin")

    else:
        return render(request, "signin.html")


@login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect("signin")