from django.urls import path
from .views import register, login, blogcreate, viewblog, world_post, likes, comments, search, post_detail,blog_type,delete_post,delete_comment,update_post,friend,friend_post,generate_request,request,remove_request,logout_view

urlpatterns = [
    path('', world_post, name='worldpost'),  
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('blogcreate/', blogcreate, name='blogcreate'),
    path('viewblog/', viewblog, name='viewblog'),
    path('likes/<int:post_id>/', likes, name='likes'),
    path('comment/<int:comn_id>/', comments, name='comment'),   
    path('search/', search, name='search'),
    path('post_detail/<int:post_id>/', post_detail, name='post_detail'),  # Add missing slash
    path('blog_type/<int:blog_type_id>',blog_type , name='blog_type'),
    path('delete_post/<int:delete_id>',delete_post , name='delete_post'),
    path('delete_comment/<int:delete_id>',delete_comment , name='delete_comment'),
    path('update_post/<int:update_id>',update_post , name='update_post'),
    path('generate_request/<int:request_id>',generate_request , name='generate_request'),
    path('remove_request/<int:remove_id>',remove_request , name='remove_request'),

    path('request',request , name='request'),
    
    path("friend/<int:friend_id>//", friend, name="friend"),
    path('friend_post/', friend_post, name='friend_post'),
    path('logout_view/', logout_view, name='logout_view'),
    
]


