"""

"""
import urllib2
from django.db.models.fields.files import FieldFile

from resources.models import Topic, Resource

def run():
    with open('resources.txt') as f:
        while True:
            line = f.readline().strip()
            slug, title, description, topic, typ, remote_url, key, reqd = line.split('===')

            topic = Topic.objects.get(slug=topic)

            if Resource.objects.filter(slug=slug[:40]):
                print "SKIPPING %s", title
                continue

            key = bool(int(key))
            reqd = bool(int(reqd))

            if typ == 'Link':
                print title,
                resource = Resource(
                    title=title,
                    description=description,
                    topic=topic,
                    slug=slug[:40],
                    status='published',
                    link=remote_url,
                    key=key,
                    required=reqd,
                )
                print remote_url,
                resource.index_link(remote_url)
                print ".",
                resource.save()
                print "."


            elif typ == 'File':
                print title,

                from django.core.files.base import ContentFile


                web = urllib2.urlopen(remote_url)
                the_file = ContentFile(web.read())
                resource = Resource(
                    title=title,
                    description=description,
                    topic=topic,
                    slug=slug[:40],
                    status='published',
                    key=key,
                    required=reqd,
                )
                if web.headers.subtype == 'pdf':
                    fname = slug + '.pdf'
                elif web.headers.subtype == 'html':
                    fname = slug + '.html'
                else:
                    raise Exception(web.headers.subtype)
                resource.file.save(fname, the_file, save=False)
                print ".",
                resource.index_file(the_file, mimetype=web.headers.type)
                print ".",
                resource.save()
                print "\n\n"
                web.close()

            elif typ == 'Image':

                print title,

                from django.core.files.base import ContentFile
                web=urllib2.urlopen(remote_url)
                the_file=ContentFile(web.read())
                resource = Resource(
                    title=title,
                    description=description,
                    topic=topic,
                    slug=slug[:40],
                    status='published',
                    key=key,
                    required=reqd,
                )
                if web.headers.subtype=='jpeg':
                    fname = slug + '.jpg'
                elif web.headers.subtype=='png':
                    fname = slug + '.png'
                else:
                    raise Exception(web.headers.subtype)
                resource.file.save(fname, the_file, save=False)
                print ".",
                resource.index_file(the_file, mimetype=web.headers.type)
                print ".",
                resource.save()
                web.close()

            else:
                raise Exception("type?")
