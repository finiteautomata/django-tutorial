from .models import Question, Choice
from django import forms
from django.forms import inlineformset_factory, formset_factory

class QuestionForm(forms.Form):
    question_text = forms.CharField(label='Question', max_length=100)

ChoiceFormSet = inlineformset_factory(
    Question, Choice, fields=["choice_text"], extra=2,
)
