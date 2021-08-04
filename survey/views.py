from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from survey.models import Question, Answer, QuestionLike
from django.db.models import Q
from django.urls import reverse_lazy


class QuestionListView(ListView):
    model = Question
    def get_queryset(self):
        return super().get_queryset()[:20]


class QuestionCreateView(CreateView):
    model = Question
    fields = ["title", "description"]
    redirect_url = ""
    success_url = reverse_lazy('survey:question-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        # add message of create and validation
        return super().form_valid(form)


class QuestionUpdateView(UpdateView):
    model = Question
    fields = ["title", "description"]
    template_name = "survey/question_form.html"
    success_url = reverse_lazy('survey:question-list')


def answer_question(request):
    answer_pk = request.POST.get("answer_pk")
    value = request.POST.get("value")
    if answer_pk is None or value is None:
        return JsonResponse({"ok": False})
    try:
        answer = Answer.objects.get(pk=answer_pk)
    except Exception:
        return JsonResponse({"ok": False})
    answer.value = value
    answer.save()
    return JsonResponse({"ok": True})


def like_dislike_question(request):
    question_pk = request.POST.get("question_pk")
    value = request.POST.get("value")
    if question_pk is None or value is None:
        return JsonResponse({"ok": False})
    try:
        question = Question.objects.get(pk=question_pk)
    except Exception:
        return JsonResponse({"message": "Question no exists"})

    # makes value True or False
    like = True if value == "like" else False
    try:
        question_like = QuestionLike.objects.get(
            Q(author=request.user) & Q(question=question)
        )
        question_like.like = like
    except Exception:
        question_like = QuestionLike(author=request.user, question=question, like=like)
    question_like.save()
    return JsonResponse({"ok": True})
