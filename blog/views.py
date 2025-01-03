from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from .forms import CreateUser,Postform,Loginform,CommentsForm
from .models import CustomUser,Post,Likes,Friends,Comments,Follow_Requests
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            phoneNumber = form.cleaned_data.get('phoneNumber')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                phoneNumber=phoneNumber
            )
            auth_login(request, user)
            return redirect(login)
        else:
            print("form is not valid")
    else:
        form = CreateUser()
    return render(request,'subtemplate/register.html',{'form':form})


def login(request):
    if request.method == 'POST':
        form = Loginform(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('viewblog') 
            else:
                form.add_error(None, 'Invalid username or password')
        else:
            print("Form is not valid")
    else:
        form = Loginform()
    return render(request, 'subtemplate/login.html', {'form': form})



@login_required(login_url="login")
def blogcreate(request):
    if request.method == 'POST':
        form = Postform(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # Create a Post instance but don't save it yet
            post.author = request.user  # Set the author to the currently logged-in user
            post.save()  # Save the Post instance to the database
            return redirect(blogcreate)
    else:
        form = Postform()
        
    return render(request,'subtemplate/blogcreate.html',{'form':form,'nbar': 'create blog'})


@login_required(login_url="login")
def viewblog(request):
    all_user = CustomUser.objects.all()
    post_type = {key: value for key, value in Post.POST_Categories}
    
    # Get the posts created by the currently logged-in user
    user_posts = Post.objects.filter(author=request.user)
    posts = Post.objects.all()
    
    # Count likes for each post
    likes_count = {post.id: Likes.objects.filter(post=post).count() for post in posts}
    
    # Get the current user's friends
    friend_list = Friends.objects.filter(user_id=request.user.id)
    friend_ids = [friend.friend_id for friend in friend_list]  # Assuming friend_id is the field holding the friend's user ID
    
    current_user = request.user.id
    user_list = CustomUser.objects.all()

    # Pass the necessary context to the template
    return render(request, 'subtemplate/viewblog.html', {
        'posts': user_posts,
        'post': posts,
        'likes_count': likes_count,
        'post_type': post_type,
        'nbar': 'Home',
        'user_list': user_list,
        'friend_ids': friend_ids,  # Pass the list of friend ID
        'current_user': current_user,
    })




def world_post(request):
    posts = Post.objects.all()
    post_type = {}
    for key,value in Post.POST_Categories:
        post_type[key]=value


    likes_count = {post.id: Likes.objects.filter(post=post).count() for post in posts}
    comments_data = Comments.objects.all()
    if request.method == "POST":
        form = CommentsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("worldpost")
    else:
        form = CommentsForm()
    return render(request,'subtemplate/worldpost.html',{'posts':posts,'likes_count': likes_count,"form":form,"comments_data":comments_data,"post_type":post_type,'nbar':'World'})

def post_detail(request, post_id):

    # Get the post object by its ID or return 404 if not found
    post = get_object_or_404(Post, id=post_id)
    
    # Get the total number of likes for this post
    likes_count = Likes.objects.filter(post=post).count()
    
    # Check if the user has already liked this post
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = Likes.objects.filter(post=post, user=request.user).exists()

    user_id = request.user.id
    # Pass the post, likes count, and user like status to the template
    context = {
        'post': post,
        'likes_count': likes_count,
        'user_has_liked': user_has_liked,
        "user_id":user_id
    }
    

    return render(request, 'subtemplate/post_detail.html', context,)

@login_required
def likes(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    if not Likes.objects.filter(user=user, post=post).exists():
        Likes.objects.create(user=user, post=post)
    else:
        like_id = get_object_or_404(Likes,user=user,post_id= post)
        like_id.delete()

    return redirect(f"post_detail",post_id)


def comments(request,comn_id):
    comment_data = Comments.objects.filter(post = comn_id)
    
    if request.method == "POST":
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            post = get_object_or_404(Post,id = comn_id)
            comment.post = post
            form.save()
            return redirect("post_detail",comn_id)
    else:
        form = CommentsForm()
    return render(request,"subtemplate/comment.html",{"form":form,"comments":comment_data})



def search(request):
    posts = Post.objects.all()
    post_type = {}
    for key,value in Post.POST_Categories:
        post_type[key]=value

    query = request.GET.get('query')
    results = []
    likes_count = {}
    if query:
        posts = Post.objects.all()
        results = Post.objects.filter(title__icontains = query )
        likes_count = {post.id: Likes.objects.filter(post=post).count() for post in posts}
    return render(request,"subtemplate/search.html",{"results":results,"likes":likes_count,"post_type":post_type})

def blog_type(request,blog_type_id):
    posts = Post.objects.filter(type=blog_type_id)
    post_type = {}
    for key,value in Post.POST_Categories:
        post_type[key]=value


    return render(request,"subtemplate/blog_type.html",{"post":posts,"post_type":post_type})


def delete_post(requset,delete_id):
    delete = get_object_or_404(Post,id = delete_id)
    delete.delete()
    return redirect("worldpost")

def delete_comment(request,delete_id):
    delete = get_object_or_404(Comments,id=delete_id)
    delete.delete()
    return redirect("worldpost")

def update_post(request,update_id):
    update = get_object_or_404(Post,id = update_id)
   
    if request.method == 'POST':
        form = Postform(request.POST,request.FILES,instance = update) # showing data to user py instance
        if form.is_valid():
            post = form.save(commit=False)  # Create a Post instance but don't save it yet
            post.author = request.user  # Set the author to the currently logged-in user
            post.save()
            return redirect(post_detail,update_id)
    else:
        form = Postform(instance = update)
    return render(request,"subtemplate/update_post.html",{"form":form,"update":update})


def generate_request(request,request_id):
    request_user = get_object_or_404(CustomUser,pk= request_id)
    print(request_user.id)
    
     

    Follow_Requests.objects.create(user = request_user ,request_name = str(request.user) ,request_id = request.user.id )
    return redirect(viewblog)

def remove_request(request,remove_id):
    request_user = get_object_or_404(Follow_Requests,pk = remove_id)
    request_user.delete()
    return render(request,"subtemplate/follow_request.html")
    

def request(request):
    request_list = Follow_Requests.objects.filter(user = request.user)
    return render(request,"subtemplate/follow_request.html",{"request_list":request_list})


def friend(request,friend_id):
    print(friend_id)
    users = get_object_or_404(CustomUser,pk = friend_id)
    request_id = get_object_or_404(Follow_Requests,request_id = friend_id)
    request_id.delete()

    Friends.objects.create(user_id = request.user.id,friend_id = users.id, name = users)
    return render(request,"subtemplate/follow_request.html")

def friend_post(request):
    post = Post.objects.all()
    friend_post = Friends.objects.filter(user = request.user)
    friend_list = {}
    for friend in friend_post:
        friend_list[friend.name] = friend.friend_id

    print(friend_list)
    
    return render(request,"subtemplate/friend_post.html",{
        "nbar":'friend',
        "friend_list":friend_list,
        'posts':post
        })


def logout_view(request):
    logout(request)
    return redirect(world_post) 

