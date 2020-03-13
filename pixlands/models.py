from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


class Topic(models.Model):
    """Тема, которую изучает пользователь."""
    text = models.CharField(max_length=50)
    public = models.BooleanField(False)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Возвращает строковое представление модели."""
        return self.text


class Image(models.Model):
    """Изображение, которое выложил пользователь."""

    def validate_image(fieldfile_obj):
        w, h = get_image_dimensions(fieldfile_obj)
        if w < 600:
            raise ValidationError(
                "The image is %i pixel wide. It supposed to be 600px" % w
            )

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='photos/%Y/%m/%d',
        validators=[validate_image],
        blank=False,
        null=False
    )
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return '/static' + self.image.url

    def __str__(self):
        """Возвращает строковое представление модели."""
        return self.text


class ProfilePic(models.Model):
    """Изображение профиля."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def user_directory_path(instance, filename):
        # file will be uploaded to media/user_<id>/<filename>
        return 'user_pics/user_{0}/{1}'.format(instance.owner.id, filename)
    image = models.ImageField(upload_to=user_directory_path, blank=True)

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return '/static' + self.image.url


class Comment(models.Model):
    """Комментарий под изображением."""
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Возвращает строковое представление модели."""
        return self.comment


class Like(models.Model):
    """Лайк под изображением."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

