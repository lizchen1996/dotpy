from django.http import Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
import logging as log
from django.contrib.auth.decorators import login_required
from dotpy.lessons.models import Lesson, Comment, LessonForm
from dotpy.lessons.util import check_lesson_markdown_cache
from dotpy.util import user_context

#
# Note: Remember to use user_context(request) to
# show user login status
#

def home(request):
  lessons = Lesson.objects.all()
  return render_to_response('home.html', {'lessons': lessons},
                            user_context(request))

def show(request, slug):
  if not slug:
    # show lessons home page
    return render_to_response('home.html')

  # load lesson from database
  lesson = get_object_or_404(Lesson, slug=slug)

  # check if the cache file exists for this lesson
  markdown_template = check_lesson_markdown_cache(lesson)
  return render_to_response('lesson.html', \
            {'lesson':lesson, \
             'comments_num': lesson.comment_set.count(), \
             'markdown_template': markdown_template \
            }, user_context(request))

def show_comments(request, slug):
  lesson = get_object_or_404(Lesson, slug=slug)
  comments = lesson.comment_set.all()
  return render_to_response('comment.html',
            {'lesson': lesson, 'comments': comments},
            user_context(request))

@login_required
def edit(request, slug):
  # TODO admin required
  if request.method == 'POST':
    if slug:
      lesson = get_object_or_404(Lesson, slug=slug)
      form = LessonForm(request.POST, instance=lesson)
    else:
      form = LessonForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('/learn/%s' % form.instance.slug)
  else:
    if slug:
      lesson = get_object_or_404(Lesson, slug=slug)
      form = LessonForm(instance=lesson)
    else:
      form = LessonForm()
  return render_to_response('lesson_form.html', {'form': form}, user_context(request))
