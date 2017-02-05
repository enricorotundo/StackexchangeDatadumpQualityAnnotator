from django.http import HttpResponse
from random import choice
from django.template import loader
from django.shortcuts import redirect
from .models import *


def get_shared_questions():
    """
    databases = ['cooking', 'travel', 'webapps']
    shared_questions = {}
    random.seed(a=42)
    for db_name in databases:
        shared_questions_db = []
        # get all questions
        all_questions_ids = Posts.objects \
            .using(db_name) \
            .filter(posttypeid=1) \
            .values_list('id', flat=True)
        while len(shared_questions_db) < 33:
            question_id = random.choice(all_questions_ids)
            question_obj = Posts.objects.using(db_name).get(pk=question_id)
            answers_count = Posts.objects.using(db_name).filter(parentid=question_id).count()
            if answers_count > 0:
                shared_questions_db.append(question_id)
        shared_questions[db_name] = shared_questions_db
    """
    shared_questions = {
        'webapps': [87766L, 26903L, 62617L,
            35474L, 41781L, 22823L,
            21256L, 22647L, 54023L,
            89446L, 35777L, 18961L,
            8300L, 4636L, 9933L,
            79077L, 6114L, 33351L,
            48644L, 95441L, 86540L,
            965L, 70948L, 49595L,
            23029L, 60268L, 10071L,
            39636L, 41275L, 93269L,
            87742L, 22719L, 45530L
        ],
        'travel': [31336L, 46022L, 50155L,
            67830L, 47607L, 57198L,
            3677L, 19143L, 23420L,
            6258L, 7733L, 22628L,
            51218L, 30406L, 30744L,
            17830L, 21846L, 73300L,
            49599L, 13845L, 13279L,
            31394L, 77483L, 51459L,
            46329L, 55678L, 66741L,
            61532L, 19214L, 2589L,
            25204L, 21901L, 17942L
        ],
        'cooking': [45214L, 1927L, 19040L,
            15970L, 54327L, 47570L,
            65309L, 6837L, 28760L,
            2425L, 15681L, 35629L,
            2079L, 14364L, 38188L,
            15794L, 42120L, 58902L,
            403L, 58713L, 49975L,
            22725L, 11411L, 69203L,
            22513L, 7227L, 7491L,
            62409L, 43000L, 58797L,
            53908L, 37637L, 71194L
        ]
    }
    return shared_questions


def index(request):
    template = loader.get_template('index.html')
    shared_questions = get_shared_questions()
    data = dict()

    data["shared_count_enrico"] = 0
    data["shared_count_marit"] = 0
    data["shared_count_christine"] = 0
    data["shared_count_henrik"] = 0
    data["count_enrico"] = 0
    data["count_marit"] = 0
    data["count_christine"] = 0
    data["count_henrik"] = 0

    # retrieve shared questions counting
    for db_name in shared_questions:
        data["shared_count_enrico"] += Posts.objects.using(db_name).filter(pk__in=shared_questions[db_name]).exclude(annotatedqualityenrico__isnull=True).count()
        data["shared_count_marit"] += Posts.objects.using(db_name).filter(pk__in=shared_questions[db_name]).exclude(annotatedqualitymarit__isnull=True).count()
        data["shared_count_christine"] += Posts.objects.using(db_name).filter(pk__in=shared_questions[db_name]).exclude(annotatedqualitychristine__isnull=True).count()
        data["shared_count_henrik"] += Posts.objects.using(db_name).filter(pk__in=shared_questions[db_name]).exclude(annotatedqualityhenrik__isnull=True).count()

        data["count_enrico"] += Annotationscount.objects.using(db_name).get(id=0).enrico
        data["count_marit"] += Annotationscount.objects.using(db_name).get(id=0).marit
        data["count_christine"] += Annotationscount.objects.using(db_name).get(id=0).christine
        data["count_henrik"] += Annotationscount.objects.using(db_name).get(id=0).henrik

    context = {
        'data' : data
    }

    return HttpResponse(template.render(context, request))

def shared_list(request, annotator_name=None):
    template = loader.get_template('shared_questions.html')
    shared_questions = get_shared_questions()
    counter = 1

    # flatten and randomize the list with fixed seed
    questions_list = []
    for db_name in shared_questions:
        for id in shared_questions[db_name]:
            #retrieve status
            question_obj = Posts.objects.using(db_name).get(pk=id)

            if annotator_name == 'enrico':
                annotation = question_obj.annotatedqualityenrico
            if annotator_name == 'marit':
                annotation = question_obj.annotatedqualitymarit
            if annotator_name == 'christine':
                annotation = question_obj.annotatedqualitychristine
            if annotator_name == 'henrik':
                annotation = question_obj.annotatedqualityhenrik

            if annotation is not None:
                status = "Done"
            else:
                status = "Todo"

            questions_list.append((db_name, id, status, counter))
            counter += 1

    context = {
        'questions_list': questions_list,
        'annotator_name': annotator_name
    }

    return HttpResponse(template.render(context, request))



def entry_point(request, annotator_name=None):
    print "Entrypoint for " + annotator_name

    # randomly choose the database
    databases = ['cooking', 'travel', 'webapps']
    choosen_db = choice(databases)

    # get all questions
    # assumes: if a question's annotated, then all the answers have been annotated al well
    all_questions_ids = Posts.objects\
        .using(choosen_db)\
        .filter(posttypeid=1) \
        .values_list('id', flat=True)

    # retrieve a random question
    question_id = choice(all_questions_ids)


    print "Redirecting " + choosen_db + "(" + str(question_id) + ")"

    # select one question
    question_id = str(choice(all_questions_ids))

    return redirect('/'+ annotator_name + '/' + choosen_db + '/' + question_id)



"""
Given annotator_name, db_name, question_id,
it loads the question with all the answers and renders the page.
"""
def annotation(request, annotator_name, db_name, question_id, shared=None):
    print "Annotation for " + annotator_name + " " + db_name + "(" + str(question_id) + ")"
    template = loader.get_template('annotation.html')


    # retrieve the given question
    question_obj = Posts.objects.using(db_name).get(pk=question_id)

    # retrieve its answers, sorted by date
    all_answers_objs = Posts.objects \
        .using(db_name)\
        .filter(parentid=question_id)\
        .order_by('creationdate')

    # if retrieved question has not answers get a new one
    # hint: use .count() if wanna use a min amount of answers
    if not all_answers_objs.exists():
        return redirect('/' + annotator_name + '/')


    # load all the answers
    all_answers_data = list()
    for answer_obj in all_answers_objs:
        answer_data = dict()
        answer_data['answer_id'] = answer_obj.id
        answer_data['answer_body'] = answer_obj.body

        # get possibly previous annotations
        if annotator_name == 'enrico':
            answer_data['answer_quality'] = answer_obj.annotatedqualityenrico
        if annotator_name == 'marit':
            answer_data['answer_quality'] = answer_obj.annotatedqualitymarit
        if annotator_name == 'christine':
            answer_data['answer_quality'] = answer_obj.annotatedqualitychristine
        if annotator_name == 'henrik':
            answer_data['answer_quality'] = answer_obj.annotatedqualityhenrik

        all_answers_data.append(answer_data)

    # fill in the context
    data = dict()
    data['db_name'] = db_name
    data['question_id'] = question_id
    data['question_title'] = question_obj.title
    data['question_body'] = question_obj.body
    if annotator_name == 'enrico':
        data['question_quality'] = question_obj.annotatedqualityenrico
    if annotator_name == 'marit':
        data['question_quality'] = question_obj.annotatedqualitymarit
    if annotator_name == 'christine':
        data['question_quality'] = question_obj.annotatedqualitychristine
    if annotator_name == 'henrik':
        data['question_quality'] = question_obj.annotatedqualityhenrik

    print "data['question_quality']:" + str(data['question_quality'])

    data['answers_list'] = all_answers_data
    data['annotator_name'] = annotator_name

    #default redirect behaviour
    data['submit_redirect'] = '/'
    if shared != '':
        data['submit_redirect'] = '/shared'

    context = {
        'data' : data
    }

    return HttpResponse(template.render(context, request))




def submit(request, annotator_name=None):
    print "submit method called"

    if request.method == 'POST':
        response = str(request.body)

        annotator_name = request.POST['annotator_name']
        db_name = request.POST['db_name']
        submit_redirect = request.POST['submit_redirect']

        if submit_redirect == '/':
            count_obj = Annotationscount.objects.using(db_name).get(id=0)

            if annotator_name == 'enrico':
                count_obj.enrico += 1

            if annotator_name == 'marit':
                count_obj.marit += 1

            if annotator_name == 'christine':
                count_obj.christine += 1

            if annotator_name == 'henrik':
                count_obj.henrik += 1

            count_obj.save()


        # retrieve the available annotations
        annotations = dict()
        for field in response.split('&'):
            if '_quality' in field:
                key = field.split('_')[0]
                value = field.split('=')[1]
                annotations[key] = int(value)
        print annotations

        # update each post
        for post_id in annotations.keys():
            post = Posts.objects.using(db_name).get(pk=post_id)

            if annotator_name == 'enrico':
                post.annotatedqualityenrico = annotations[post_id]
            if annotator_name == 'marit':
                post.annotatedqualitymarit = annotations[post_id]
            if annotator_name == 'christine':
                post.annotatedqualitychristine = annotations[post_id]
            if annotator_name == 'henrik':
                post.annotatedqualityhenrik = annotations[post_id]

            post.save()
    else:
        print "WARNING: submit called without any POST!"

    return redirect('/' + annotator_name + submit_redirect)