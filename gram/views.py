from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
# import cloudinary
# import cloudinary.uploader
# import cloudinary.api


# Create your views here.

#View for homepage that returns all posted images
@login_required(login_url='/accounts/login/')
def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})

# profile page
@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    # get images for the current logged in user
    posts = Post.objects.filter(user_id=current_user.id)
    # get the profile of the current logged in user
    profile = Profile.objects.filter(user_id=current_user.id).first()
    return render(request, 'profile.html', {"posts": posts, "profile": profile})

# save image  with image name,image caption and upload image to cloudinary
@login_required(login_url='/accounts/login/')
def new_post(request):
    if request.method == 'POST':
        image_name = request.POST['image_name']
        image_caption = request.POST['image_caption']
        image_file = request.FILES['image_file']
        # image_file = cloudinary.uploader.upload(image_file)
        # image_url = image_file['url']
        # image_public_id = image_file['public_id']
        image = Post(image_name=image_name, image_caption=image_caption, image=image_file,
                      profile_id=request.POST['user_id'], user_id=request.POST['user_id'])
        image.save_image()
        return redirect('/profile', {'success': 'Image Uploaded Successfully'})
    else:
        return render(request, 'profile.html', {'danger': 'Image Upload Failed'})

# update profile with first name,last name,username,email and upload profile image to cloudinary
@login_required(login_url='/accounts/login/')
def update_profile(request):
    if request.method == 'POST':

        current_user = request.user

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']

        bio = request.POST['bio']

        profile_image = request.FILES['profile_pic']
        # profile_image = cloudinary.uploader.upload(profile_image)
        # profile_url = profile_image['url']

        user = User.objects.get(id=current_user.id)

        # check if user exists in profile table and if not create a new profile
        if Profile.objects.filter(user_id=current_user.id).exists():

            profile = Profile.objects.get(user_id=current_user.id)
            profile.profile_photo = profile_image
            profile.bio = bio
            profile.save()
        else:
            profile = Profile(user_id=current_user.id,
                              profile_photo=profile_image, bio=bio)
            profile.save_profile()

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        user.save()

        return redirect('/profile', {'success': 'Profile Updated Successfully'})

       
    else:
        return render(request, 'profile.html', {'danger': 'Profile Update Failed'})


# like image
@login_required(login_url='/accounts/login/')
def like_image(request, id):
    likes = Like.objects.filter(image_id=id).first()
    # check if the user has already liked the image
    if Like.objects.filter(image_id=id, user_id=request.user.id).exists():
        # unlike the image
        likes.delete()
        # reduce the number of likes by 1 for the image
        post = Post.objects.get(id=id)
        # check if the image like_count is equal to 0
        if post.likes == 0:
            post.likes = 0
            post.save()
        else:
            post.likes -= 1
            post.save()
        return redirect('/')
    else:
        likes = Like(image_id=id, user_id=request.user.id)
        likes.save()
        # increase the number of likes by 1 for the image
        post = Post.objects.get(id=id)
        post.likes = post.likes + 1
        post.save()
        return redirect('/')


# single image page with comments
@login_required(login_url='/accounts/login/')
def view_post(request, id):
    post = Post.objects.get(id=id)
    # get related images to the image that is being viewed by the user and order them by the date they were created
    related_posts = Post.objects.filter(
        user_id=post.user_id)
    title = post.image_name
    # check if image exists
    if Post.objects.filter(id=id).exists():
        # get all the comments for the image
        comments = Comment.objects.filter(post_id=id)
        return render(request, 'picture.html', {'post': post, 'comments': comments, 'posts': related_posts, 'title': title})
    else:
        return redirect('/')


# save comment
@login_required(login_url='/accounts/login/')
def add_comment(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        post_id = request.POST['post_id']
        post = Post.objects.get(id=post_id)
        user = request.user
        comment = Comment(comment=comment, post_id=post_id, user_id=user.id)
        comment.save_comment()
        # increase the number of comments by 1 for the image
        post.comments = post.comments + 1
        post.save()
        return redirect('/picture/' + str(post_id))
    else:
        return redirect('/')


# user profile page with images
@login_required(login_url='/accounts/login/')
def user_profile(request, id):
    # check if user exists
    if User.objects.filter(id=id).exists():
        # get the user
        user = User.objects.get(id=id)
        # get all the images for the user
        posts = Post.objects.filter(user_id=id)
        # get the profile of the user
        profile = Profile.objects.filter(user_id=id).first()
        return render(request, 'user-profile.html', {'posts': posts, 'profile': profile, 'user': user})
    else:
        return redirect('/')


# search for images
@login_required(login_url='/accounts/login/')
def search_posts(request):
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get('search').lower()
        posts = Post.search_by_image_name(search_term)
        message = f'{search_term}'
        title = message

        return render(request, 'search.html', {'success': message, 'posts': posts})
    else:
        message = 'You havent searched for any term'
        return render(request, 'search.html', {'danger': message})
