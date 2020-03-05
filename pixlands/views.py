from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404

from pixlands.models import Topic, Image, ProfilePic, Comment, Like
from pixlands.forms import TopicForm, ImageForm, EditImageForm, \
                           ProfilePicForm, CommentForm
import os


def index(request):
    """Домашняя страница приложения Pixland."""
    topics = Topic.objects.filter(public=True).order_by('-date_added').all()
    image_list = ''
    for topic in topics:
        topic_images = topic.image_set.all()
        if not image_list:
            image_list = topic_images
        else:
            image_list = image_list | topic_images

    if image_list:
        image_list = image_list.order_by('-date_added')

    paginator = Paginator(image_list, 24)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)

    context = {'topics': topics, 'images': images}
    return render(request, 'pixlands/index.html', context)


def topics(request):
    """Выводит список публичных тем."""
    unformatted_topics = Topic.objects.filter(
        public=True
    ).order_by('date_added').reverse()

    def get_topic(t):
        t.images = t.image_set.order_by('-date_added')[:4]
        return t

    topic_list = map(get_topic, unformatted_topics)

    paginator = Paginator(list(topic_list), 10)
    page = request.GET.get('page')

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)

    context = {'topics': topics}
    return render(request, 'pixlands/topics.html', context)


def topic(request, topic_id):
    """Выводит одну тему и все ее изображения."""
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.public or topic.owner == request.user:
        image_list = topic.image_set.order_by('-date_added')

        paginator = Paginator(image_list, 5)
        page = request.GET.get('page')
        try:
            images = paginator.page(page)
        except PageNotAnInteger:
            images = paginator.page(1)
        except EmptyPage:
            images = paginator.page(paginator.num_pages)

        for image in images:
            try:
                image.profilepic = ProfilePic.objects.filter(
                    owner=image.owner
                ).get()
            except ObjectDoesNotExist:
                None
            image.likes = len(Like.objects.filter(image=image))
            image.comments = len(Comment.objects.filter(image_id=image))
    else:
        raise Http404

    context = {
        'topic': topic,
        'images': images,
    }
    return render(request, 'pixlands/topic.html', context)


@login_required
def profile(request):
    """Страница пользователя, выводит список созданных им тем."""
    unformatted_topics = Topic.objects.filter(
        owner=request.user
    ).order_by('date_added').reverse()
    try:
        profilepic = ProfilePic.objects.filter(owner=request.user).get()
    except ObjectDoesNotExist:
        profilepic = None

    def get_topic(t):
        t.images = t.image_set.order_by('-date_added')[:4]
        return t

    topic_list = map(get_topic, unformatted_topics)

    paginator = Paginator(list(topic_list), 10)
    page = request.GET.get('page')

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)

    context = {'topics': topics, 'profilepic': profilepic}
    return render(request, 'pixlands/profile.html', context)


def image(request, image_id):
    """Выводит одно изображение и комментарии под ним."""
    image = get_object_or_404(Image, id=image_id)
    if image.topic.public is not True and image.owner != request.user:
        raise Http404
    image.comments = Comment.objects.filter(image_id=image)
    comments_count = len(image.comments)
    form = CommentForm()
    image.number_of_likes = image.like_set.all().count()

    try:
        profilepic = ProfilePic.objects.filter(owner=image.owner).get()
    except ObjectDoesNotExist:
        profilepic = None

    for comment in image.comments:
        try:
            comment.profilepic = ProfilePic.objects.filter(
                owner=comment.owner
            ).get()
        except ObjectDoesNotExist:
            None

    context = {
        'image': image,
        'form': form,
        'comments_count': comments_count,
        'profilepic': profilepic,
    }
    return render(request, 'pixlands/image.html', context)


@login_required
def new_topic(request):
    """Добавляет новую тему."""
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма
        form = TopicForm()
    else:
        # Отправлены данные POST; обработать данные
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            if new_topic.public == True:
                return HttpResponseRedirect(reverse('pixlands:topics'))
            else:
                return HttpResponseRedirect(reverse('pixlands:profile'))

    context = {'form': form}
    return render(request, 'pixlands/new_topic.html', context)


@login_required
def add_image(request, topic_id):
    """Добавление нового изображения в конкретную тему."""
    error_msg = None
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.owner != request.user and topic.public == False:
        raise Http404
    elif request.method != 'POST':
        # Данные не отправлялись; создается пустая форма
        form = ImageForm()
    else:
        # Отправленны данные POST; обработать данные
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            if 'image' in request.FILES:
                form.image = request.FILES['image']
            new_image = form.save(commit=False)
            new_image.owner = request.user
            new_image.topic = topic
            new_image.save()
            return HttpResponseRedirect(reverse(
                'pixlands:topic',
                args=[topic_id]
            ))
        else:
            error_msg = 'You need to add an image!'

    context = {'topic': topic, 'form': form, 'error_msg': error_msg}
    return render(request, 'pixlands/add_image.html', context)


@login_required
def add_profile_pic(request):
    """Добавление аватара пользователя."""
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма
        form = ProfilePicForm()
    else:
        # Отправленны данные POST; обработать данные
        form = ProfilePicForm(request.POST, request.FILES)
        if form.is_valid():
            if 'image' in request.FILES:
                form.image = request.FILES['image']
            new_image = form.save(commit=False)
            new_image.owner = request.user
            try:
                old_profilepic = ProfilePic.objects.filter(
                    owner=request.user
                ).get()
                path = 'C:\\python_work\\pixland\\media\\' \
                       'user_pics\\user_{0}\\{1}'
                os.remove(
                    path.format(request.user.id, os.path.basename(
                        old_profilepic.image_url
                    ))
                )
                old_profilepic.delete()
            except ObjectDoesNotExist:
                None
            new_image.save()
            return HttpResponseRedirect(reverse('pixlands:profile'))

    context = {'form': form}
    return render(request, 'pixlands/add_profile_pic.html', context)


@login_required
def add_comment(request, image_id):
    """Добавление комментария под изображение."""
    image = get_object_or_404(Image, id=image_id)
    if image.topic.public is not True and image.owner != request.user:
        raise Http404
    else:
        # Отправка данных POST; обработать данные
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.owner = request.user
            new_comment.image_id = image
            new_comment.save()
            return HttpResponseRedirect(reverse(
                'pixlands:image',
                args=[image.id]
            ))


@login_required
def edit_topic(request, topic_id):
    """Редактирует существующую тему."""
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.owner == request.user:
        if request.method != 'POST':
            # Исходный запрос; форма заполняется данными текущей записи
            form = TopicForm(instance=topic)
        else:
            # Отправка данных POST; обработать данные
            form = TopicForm(instance=topic, data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse(
                    'pixlands:topic',
                    args=[topic.id]
                ))
    else:
        raise Http404

    context = {'topic': topic, 'form': form}
    return render(request, 'pixlands/edit_topic.html', context)


@login_required
def edit_image(request, image_id):
    """Редактирует существующий текст изображения."""
    image = get_object_or_404(Image, id=image_id)
    if image.owner == request.user:
        if request.method != 'POST':
            # Исходный запрос; форма заполняется данными текущей записи
            form = EditImageForm(instance=image)
        else:
            # Отправка данных POST; обработать данные
            form = EditImageForm(instance=image, data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse(
                    'pixlands:image',
                    args=[image.id]
                ))
    else:
        raise Http404

    context = {'image': image, 'form': form}
    return render(request, 'pixlands/edit_image.html', context)


@login_required
def delete_topic(request, topic_id):
    """Удаляет тему."""
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.owner == request.user:
        topic.delete()
    else:
        raise Http404
    if topic.public == True:
        return HttpResponseRedirect(reverse('pixlands:topics'))
    else:
        return HttpResponseRedirect(reverse('pixlands:profile'))


@login_required
def delete_image(request, image_id):
    """Удаляет изображение."""
    image = get_object_or_404(Image, id=image_id)
    date = image.date_added
    topic = image.topic
    if image.owner == request.user:
        path = 'C:\\python_work\\pixland\\media\\photos\\{0}\\{1}\\{2}\\{3}'
        os.remove(
            path.format(date.year, f"{date.month:02d}", f"{date.day:02d}",
                        os.path.basename(image.image_url)))
        image.delete()
    else:
        raise Http404
    return HttpResponseRedirect(reverse('pixlands:topic', args=[topic.id]))


@login_required
def delete_comment(request, comment_id):
    """Удаляет комментарий."""
    comment = get_object_or_404(Comment, id=comment_id)
    image = comment.image_id
    if comment.owner == request.user:
        comment.delete()
    else:
        raise Http404
    return HttpResponseRedirect(reverse('pixlands:image', args=[image.id]))


def like(request, image_id):
    new_like, created = Like.objects.get_or_create(
        owner=request.user,
        image_id=image_id
    )
    if not created:
        new_like.delete()


@login_required
def like_on_image(request, image_id):
    """Ставит лайк на странице изображения."""
    like(request, image_id)
    return HttpResponseRedirect(reverse('pixlands:image', args=[image_id]))


@login_required
def like_on_topic(request, image_id):
    """Ставит лайк на странице темы."""
    image = get_object_or_404(Image, id=image_id)
    like(request, image_id)
    return HttpResponseRedirect(reverse(
        'pixlands:topic',
        args=[image.topic.id]
    ))


@login_required
def like_on_search(request, image_id):
    """Ставит лайк на странице поиска."""
    query = request.GET.get('q')
    like(request, image_id)
    return HttpResponseRedirect(reverse('pixlands:search') + '?q=' + query)


def search(request):
    """Поиск по описанию изображений."""
    data = request.GET.get('q')
    if not data:
        data = ""
    if request.user.is_authenticated:
        topics = Topic.objects.filter(
            Q(owner=request.user) | Q(public=True)
        ).order_by('-date_added').all()
    else:
        topics = Topic.objects.filter(public=True).order_by(
            '-date_added'
        ).all()

    image_list = ''
    for topic in topics:
        topic_images = topic.image_set.filter(text__icontains=data).all()
        if not image_list:
            image_list = topic_images
        else:
            image_list = image_list | topic_images

    if image_list:
        image_list = image_list.order_by('-date_added')

    paginator = Paginator(image_list, 10)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)

    for image in images:
        try:
            image.profilepic = ProfilePic.objects.filter(
                owner=image.owner
            ).get()
        except ObjectDoesNotExist:
            None
        image.likes = len(Like.objects.filter(image=image))
        image.comments = len(Comment.objects.filter(image_id=image))

    context = {
        'images': images,
        'data': data
    }
    return render(request, 'pixlands/search.html', context)
