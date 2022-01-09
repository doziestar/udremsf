"""
! Core Base Abstract Model

1. TimeStamp
2. General Model

inherited by all models in core package

! general model

1. News
2. Event
3. Article
4. Video
5. Gallery
6. Report
"""
import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse


class GeneralManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class NewsAndEventsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True, is_active=True)


class GeneralModelManager(models.Model):
    """
    Abstract Model
    """

    objects = models.Manager()
    manager = GeneralManager()

    class Meta:
        abstract = True


class NewsAndBlogModelManager(models.Model):
    """
    Abstract Model
    """

    objects = models.Manager()
    manager = NewsAndEventsManager()

    class Meta:
        abstract = True


class TimeStamp(models.Model):
    """
    ! TimeStamp Model
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class General(models.Model):
    """
    ! General Model
    """

    title = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    category = models.ManyToManyField("Category")
    image = models.ForeignKey("Image", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tags")

    def __str__(self):
        return self.title

    def slug(self):
        return self.title.replace(" ", "-")

    def excerpt(self):
        return self.description[:100]

    class Meta:
        abstract = True
        verbose_name_plural = "General"


# image models for adding multiple images to a model
class Image(models.Model):
    """
    ! Image Model
    """

    image = models.ImageField(upload_to="images/")
    image_name = models.CharField(max_length=255)
    image_caption = models.CharField(max_length=255)

    def __str__(self):
        return self.image_name

    class Meta:
        # abstract = True
        verbose_name_plural = "Images"


class Tags(TimeStamp):
    """
    ! Tags Model
    """

    tag = models.CharField(max_length=255)

    def __str__(self):
        return self.tag

    class Meta:
        # abstract = True
        verbose_name_plural = "Tags"


class Category(TimeStamp):
    """
    ! Category Model
    """

    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category

    class Meta:
        # abstract = True
        verbose_name_plural = "Categories"


class News(TimeStamp, General):
    """
    ! News Model
    """

    is_published = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("core:news-detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = "News"


class Event(TimeStamp, General, NewsAndBlogModelManager):
    """
    ! Event Model
    """

    is_published = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("core:event-detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = "Events"


class Article(TimeStamp, General, GeneralModelManager):
    """
    ! Article Model
    """

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("core:article-detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = "Articles"


class Video(TimeStamp, General):
    """
    ! Video Model
    """

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("core:video-detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = "Videos"


class Gallery(TimeStamp, General, GeneralModelManager):
    """
    ! Gallery Model
    """

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("core:gallery-detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = "Galleries"


class Report(TimeStamp, General, GeneralModelManager):
    """
    ! Report Model
    """

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("core:report-detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = "Reports"
