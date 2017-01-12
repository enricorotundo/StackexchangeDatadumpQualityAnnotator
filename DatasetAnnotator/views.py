from django.http import HttpResponse
from django.views import generic
from random import choice
from django.template import loader

from .models import *
from .forms import PostForm

def index(request):

    if request.method == 'POST':
        response = str(request.body)
        annotations = dict()
        target_db = ""

        for field in response.split('&'):
            if '_quality' in field:
                key = field.split('_')[0]
                value = field.split('=')[1]
                annotations[key] = int(value)
            if 'choosen_db' in field:
                target_db = field.split('=')[1]

        print annotations

        for post_id in annotations.keys():
            post = Post.objects.using(target_db).get(pk=post_id)
            post.annotatedquality = annotations[post_id]
            post.save()
            print str(target_db),
            print ": ",
            print str(post.pk),
            print "annotated with",
            print str(annotations[post_id])



    template = loader.get_template('index.html')

    databases = ['cooking', 'travel', 'webapps']
    choosen_db = choice(databases)

    # get all questions not yet annotated
    # assumes: if a question's annotated, then all the answers have been annotated al well
    all_questions_ids = Post.objects\
        .using(choosen_db)\
        .filter(posttypeid=1)\
        .filter(annotatedquality=None)\
        .values_list('id', flat=True)


    # retrieve a random question
    question_id = choice(all_questions_ids)
    question_obj = Post.objects.using(choosen_db).get(pk=question_id)


    # retrieve its answers, sorted by date
    all_answers_objs = Post.objects \
        .using(choosen_db)\
        .filter(parentid=question_id)\
        .order_by('creationdate')

    # load all the answers
    all_answers_data = list()
    for answer_obj in all_answers_objs:
        answer_data = dict()
        answer_data['answer_id'] = answer_obj.id
        answer_data['answer_body'] = answer_obj.body
        all_answers_data.append(answer_data)

    # fill in the context
    data = dict()
    data['choosen_db'] = choosen_db
    data['question_id'] = question_id
    data['question_title'] = question_obj.title
    data['question_body'] = question_obj.body
    data['answers_list'] = all_answers_data

    context = {
        'data' : data
    }


    return HttpResponse(template.render(context, request))

