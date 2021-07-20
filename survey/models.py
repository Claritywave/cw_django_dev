from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import datetime
from .utils import get_current_request
from django.db.models import Q


class TimeStampedModel(models.Model):
    """TimeStampedModel
    TimeStampedModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following attributes:
        + created_at (DateTime): Store the datetime the object was created.
        + modified_on (DateTime): Store the last datetime the object was modified.
    """

    updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    class Meta:
        abstract = True


class Question(TimeStampedModel):
    """
    Question model
    """

    author = models.ForeignKey(
        get_user_model(),
        related_name="user",
        verbose_name="User",
        on_delete=models.PROTECT,
    )
    title = models.CharField("Title", max_length=200)
    description = models.TextField("Description")
    question_voting = models.ManyToManyField(
        to=get_user_model(),
        through="QuestionLike",
        blank=False,
        related_name="company_users",
    )

    def get_absolute_url(self):
        return reverse("survey:question-edit", args=[self.pk])

    def __str__(self) -> str:
        return self.title

    @property
    def ranking(self):
        likes = self.question_like.filter(like=True).count()
        dislike = self.question_like.filter(like=False).count()
        answers = self.question_answers.all().count()
        created_today = 10 if self.created_on.date() < datetime.today().date() else 0
        return (answers * 10) + (likes * 5) - (dislike * 3) + created_today

    @property
    def user_likes(self):
        request = get_current_request()
        if request.user.is_anonymous:
            return None
        try:
            return QuestionLike.objects.get(
                Q(author=request.user) & Q(question__id=self.id)
            ).like
        except Exception:
            return None


class Answer(TimeStampedModel):
    """
    Answer model
    """

    ANSWERS_VALUES = (
        (0, "Sin Responder"),
        (1, "Muy Bajo"),
        (2, "Bajo"),
        (3, "Regular"),
        (4, "Alto"),
        (5, "Muy Alto"),
    )

    question = models.ForeignKey(
        to=Question,
        related_name="question_answers",
        verbose_name="Question",
        on_delete=models.PROTECT,
    )
    author = models.ForeignKey(
        to=get_user_model(),
        related_name="user_answers",
        verbose_name="Autor",
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )
    value = models.PositiveIntegerField(
        verbose_name="Vote", default=0, blank=True, null=True
    )
    comment = models.TextField(verbose_name="Comentario", blank=False, null=False)

    def __str__(self) -> str:
        return f"{ self.question } - { self.author }"


class QuestionLike(TimeStampedModel):
    """
    QuestionLike model
    """

    author = models.ForeignKey(
        to=get_user_model(),
        related_name="user_like",
        verbose_name="User",
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        to="Question",
        related_name="question_like",
        verbose_name="Question",
        on_delete=models.CASCADE,
    )

    like = models.BooleanField(null=False, blank=False)

    def __str__(self) -> str:
        return f"{ self.question } - { self.author } - { self.like }"
