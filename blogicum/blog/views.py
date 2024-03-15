from datetime import datetime

from django.shortcuts import render, get_object_or_404

from .models import Post, Category

"""Константа для количества отображаемых постов"""
NUM_POSTS_ON_PAGE = 5


def posts():
    """Получение постов из БД"""
    return Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=datetime.now()
    )


def index(request):
    """Главная страница / Лента записей"""
    return render(request, 'blog/index.html', 
                  ({'posts': get_posts()[:NUM_POSTS_ON_PAGE]}))


def post_detail(request, id):
    """Отображение полного описания выбранной записи"""
    post = get_object_or_404(posts(), id=id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    """Отображение публикаций категории"""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    context = {'category': category,
               'post_list': posts().filter(category=category)}
    return render(request, 'blog/category.html', context)
