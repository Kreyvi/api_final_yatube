from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок',
        help_text='Введите название группы',
        unique=True
    )
    slug = models.SlugField(
        max_length=50,
        # unique=True,
        blank=True,
        null=False,

    )
    description = models.TextField(
        max_length=400,
        blank=True,
        verbose_name='Описание',
        help_text='Введите описание группы',
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Group, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name='Группа',
        help_text='Группа записи'
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField()
    created = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True,
        db_index=True
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        db_table = 'Follow'
        constraints = [
            models.UniqueConstraint(
                fields=['following', 'user'],
                name='unique_follow'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='not_following'
            )
        ]
