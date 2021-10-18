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
    posts = Post.objects.all().order_by('-image_date')
    return render(request, 'index.html', {'posts': posts})

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
        image_public_id = image_file['public_id']
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


