from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path('create-post/', views.CreatePostView.as_view(), name="create-post"),
    path('update-post/<str:pk>', views.UpdatePostView.as_view(), name="update-post"),
    path('delete-post/<str:pk>', views.DeletePostView.as_view(), name="delete-post"),
    path('blog/<str:username>/', views.UserBlogView.as_view(), name="user-blog"),
    path('post/<slug:post_slug>/', views.PostView.as_view(), name="post"),
    path('myblog/', views.MyBlogView.as_view(), name="my-blog"),
    path('friends/', views.FriendsView.as_view(), name="friends"),
    path('category/<slug:category_slug>/', views.PostsByCategoryView.as_view(), name="by_category"),
    path('tag/<slug:tag_slug>', views.PostsByTagView.as_view(), name="by_tag"),
    path('like/<int:post_id>', views.LikePostView.as_view(), name='like_post'),
    path('bookmark/<int:post_id>', views.BookmarkPostView.as_view(), name='bookmark_post'),
    path('bookmarks/', views.UserBookmarksView.as_view(), name='user_bookmarks'),
]