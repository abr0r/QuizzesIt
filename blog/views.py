from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from .models import Post, Tag, Category
from .forms import PostForm, CommentForm
from .utils import searchPosts
from users.utils import paginateObjects
from users.models import Profile


get_tags_categories = lambda posts: (Tag.objects.filter(post__in=posts).distinct(), Category.objects.filter(post__in=posts).distinct())


class CreatePostView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile
        form = PostForm()
        context = {'form': form}
        return render(request, "blog/post_form.html", context)

    def post(self, request):
        profile = request.user.profile
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            post.owner = profile
            post.save()
            return redirect("blog:my-blog")
        context = {'form': form}
        return render(request, "blog/post_form.html", context)


class UpdatePostView(LoginRequiredMixin, View):
    def get(self, request, pk):
        profile = request.user.profile
        post = profile.post_set.get(id=pk)
        form = PostForm(instance=post)
        context = {'form': form, 'post': post}
        return render(request, "blog/post_form.html", context)

    def post(self, request, pk):
        profile = request.user.profile
        post = profile.post_set.get(id=pk)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect("blog:my-blog")
        context = {'form': form, 'post': post}
        return render(request, "blog/post_form.html", context)


class DeletePostView(LoginRequiredMixin, View):
    def get(self, request, pk):
        profile = request.user.profile
        post = profile.post_set.get(id=pk)
        context = {'object': post}
        return render(request, "blog/delete_template.html", context)

    def post(self, request, pk):
        profile = request.user.profile
        post = profile.post_set.get(id=pk)
        post.delete()
        return redirect("blog:my-blog")


class UserBlogView(LoginRequiredMixin, View):
    def get(self, request, username):
        profile = Profile.objects.get(username=username)
        posts = profile.post_set.all()
        tags, categories = get_tags_categories(posts)
        custom_range, posts = paginateObjects(request, posts, 3)
        context = {'profile': profile, 'posts': posts,
                    'tags': tags, 'categories': categories,
                    'custom_range': custom_range}
        return render(request, "blog/user-blog.html", context)


class PostView(LoginRequiredMixin, View):
    def get(self, request, post_slug):
        post = Post.objects.get(slug=post_slug)
        profile = request.user.profile
        comments = post.comments.filter(approved=True)
        form = CommentForm()
        context = {'post': post, 'profile': profile, 
        'comments': comments, 'form': form}
        return render(request, 'blog/single-post.html', context)

    def post(self, request, post_slug):
        post = Post.objects.get(slug=post_slug)
        profile = request.user.profile
        comments = post.comments.filter(approved=True)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.owner = request.user.profile
            comment.save()
            messages.success(request, 'Your comment will appear after moderation')
            return redirect('blog:post', post_slug=post.slug)    
        context = {'post': post, 'profile': profile, 
        'comments': comments, 'form': form}
        return render(request, 'blog/single-post.html', context)


class MyBlogView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile
        posts = profile.post_set.all()
        tags, categories = get_tags_categories(posts)
        custom_range, posts = paginateObjects(request, posts, 3)
        context = {'profile': profile, 'posts': posts,
                    'tags': tags, 'categories': categories,
                    'custom_range': custom_range}
        return render(request, "blog/my-blog.html", context)


class FriendsView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile
        posts = Post.objects.filter(
            owner__in=profile.follows.all()
        )
        tags, categories = get_tags_categories(posts)
        posts, search_query = searchPosts(request)
        custom_range, posts = paginateObjects(request, posts, 3)
        context = {'profile': profile, 'posts': posts,
                    'search_query': search_query,
                    'custom_range': custom_range,
                    'tags': tags, 'categories': categories}
        return render(request, "blog/post_list.html", context)


class PostsByCategoryView(LoginRequiredMixin, View):
    def get(self, request, category_slug):
        profile = request.user.profile
        category = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.filter(category__slug__contains=category_slug)
        tags, categories = get_tags_categories(posts)
        custom_range, posts = paginateObjects(request, posts, 3)
        context = {'profile': profile, 'posts': posts,
                    'custom_range': custom_range,
                    'tags': tags, 'category': category,
                    'categories': categories}
        return render(request, "blog/post_list.html", context)


class PostsByTagView(LoginRequiredMixin, View):
    def get(self, request, tag_slug):
        profile = request.user.profile
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.objects.filter(tags__in=[tag])
        tags, categories = get_tags_categories(posts)
        custom_range, posts = paginateObjects(request, posts, 3)
        context = {'profile': profile, 'posts': posts,
                    'custom_range': custom_range,
                    'tags': tags, 'tag': tag,
                    'categories': categories}
        return render(request, "blog/post_list.html", context)


class LikePostView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if not post.likes.filter(id=request.user.id).exists():
            post.likes.add(request.user)
            post.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            post.likes.remove(request.user)
            post.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class BookmarkPostView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if not post.bookmarks.filter(id=request.user.id).exists():
            post.bookmarks.add(request.user)
            post.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            post.bookmarks.remove(request.user)
            post.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class UserBookmarksView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile
        user = request.user
        posts = Post.objects.filter(bookmarks__in=[user])
        tags, categories = get_tags_categories(posts)
        custom_range, posts = paginateObjects(request, posts, 3)
        context = {'profile': profile, 'posts': posts,
                    'custom_range': custom_range,
                    'tags': tags, 'categories': categories}
        return render(request, "blog/post_list.html", context)