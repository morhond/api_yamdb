from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, validate_slug


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLE_CHOICES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
    ]

    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(
        'Информация о пользователе',
        help_text='Введите краткую информацию о себе',
        blank=True,
        null=True,
    )
    role = models.CharField(max_length=9, choices=ROLE_CHOICES, default=USER)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        self.is_active = True
        if self.role == self.ADMIN:
            self.is_staff = True
        super(User, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Категория',
                            unique=True,
                            validators=[MaxLengthValidator(limit_value=256)]
                            )
    slug = models.SlugField(unique=True,
                            max_length=50,
                            validators=[validate_slug,
                                        MaxLengthValidator(limit_value=50)
                                        ]
                            )

    class Meta:
        verbose_name = 'Категория'
        ordering = ['-id']

    def __str__(self):
        return f'{self.name} {self.slug}'


class Genre(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Жанр',
                            unique=True,
                            validators=[MaxLengthValidator(limit_value=256)]
                            )
    slug = models.SlugField(unique=True,
                            max_length=50,
                            validators=[validate_slug,
                                        MaxLengthValidator(limit_value=50)
                                        ]
                            )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['-id']

    def __str__(self):
        return f'{self.name} {self.slug}'


class Title(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название',
                            unique=True,
                            validators=[MaxLengthValidator(limit_value=256)]
                            )
    year = models.IntegerField(blank=True,
                               null=True,
                               verbose_name='Год выпуска')

    # TBA by another contributor (field type: ForeignKey)
    # ---------------------------------------------------
    rating = models.FloatField(blank=True,
                               null=True)
    # ---------------------------------------------------

    description = models.CharField(max_length=200,
                                   verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['-id']

    def __str__(self):
        return f'{self.name} {self.slug}'


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, db_column='genre_id', on_delete=models.CASCADE)
    title = models.ForeignKey(Title, db_column='title_id', on_delete=models.CASCADE)
