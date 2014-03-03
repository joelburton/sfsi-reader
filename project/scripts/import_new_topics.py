"""

"""
from django.utils.text import slugify
from resources.models import Topic


def run():
    with open('subtopics.txt') as f:
        while True:
            line = f.readline().strip()
            title, description, parent = line.split('===')

            print parent
            day = Topic.objects.get(slug=parent).day

            subtopic = Topic(title=title, description=description, day=day,
                             slug=slugify(unicode(title)), status='published'
                             )
            print subtopic
            subtopic.save()
