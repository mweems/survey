from django.shortcuts import render
from .models import Question, Choice
from random import randint


def index(request):
	question_list = Question.objects.all()
	for question in question_list:
		question.has_voted_on = False
		question.save()
	context = get_random_question(question_list)
	if not context:
		return render(request, 'finished.html')
	return render(request, 'detail.html', context)

def detail(request, question_id):
	question = Question.objects.get(pk=question_id)
	choices = Choice.objects.filter(question=question)
	context = {'question': question, 'choices': choices}
	return render(request, 'detail.html', context)

def vote(request, question_id):
	question = Question.objects.get(pk=question_id)
	choice = question.choice_set.get(pk=request.POST['choice'])
	choice.votes += 1
	choice.save()
	question.has_voted_on = True
	question.save()
	question_list = Question.objects.all().exclude(has_voted_on=True)
	context = get_random_question(question_list)
	if not context:
		return render(request, 'finished.html')
	return render(request, 'detail.html', context)

def adminPage(request):
	question_list = Question.objects.all()
	choices = Choice.objects.all()
	context = {'questions': question_list, 'choices': choices}
	return render(request, 'adminPage.html', context)


def get_random_question(question_list):
	if not question_list:
		return None
	question = question_list[randint(0, question_list.count() - 1)]
	choices = Choice.objects.filter(question=question)
	return {'question': question, 'choices': choices}


