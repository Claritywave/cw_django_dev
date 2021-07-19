from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Question(models.Model):
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
        through="QuestionVoting",
        blank=False,
        related_name="company_users",
    )

    def get_absolute_url(self):
        return reverse("survey:question-edit", args=[self.pk])

    def __str__(self) -> str:
        return self.title


class Answer(models.Model):
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


class QuestionVoting(models.Model):
    """
    QuestionVoting model
    """

    author = models.ForeignKey(
        to=get_user_model(),
        related_name="voting_user",
        verbose_name="User",
        on_delete=models.CASCADE,
    )
    quetion = models.ForeignKey(
        to="Question",
        related_name="question_vote",
        verbose_name="Question",
        on_delete=models.CASCADE,
    )

    like = models.BooleanField(null=False, blank=False)

    def __str__(self) -> str:
        return f"{ self.question } - { self.author } - { self.vote }"
