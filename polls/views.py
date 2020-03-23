from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Choice, Question
from .forms import QuestionForm, ChoiceFormSet


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

def new_question(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = QuestionForm(request.POST)
        choice_formset = ChoiceFormSet(
            request.POST, prefix='choice'
        )
        # check whether it's valid:
        if form.is_valid() and choice_formset.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            question = Question(**form.cleaned_data)

            question.save()

            choice_formset.instance = question

            choice_formset.save()
            return redirect(reverse('polls:detail', args=(question.id,)))

    # if a GET (or any other method) we'll create a blank form
    else:

        choice_formset = ChoiceFormSet(prefix="choice")
        form = QuestionForm()

    return render(
        request, 'polls/new.html',
        {
            'form': form,
            'choice_formset': choice_formset,
        }
    )

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
