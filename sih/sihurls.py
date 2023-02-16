
from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^savefile/',views.Save_File,name='savefile'),
    url(r'^nlpfile/',views.nlpfile,name='nlpfile'),
    url(r'^nlp/',views.nlp,name='nlp'),
    url(r'^classi/',views.classi,name='classi'),
    url(r'^classifile/',views.classifile,name='classifile'),
    url(r'^ts/',views.ts,name='ts'),
    url(r'^tsfile/',views.tsfile,name='tsfile'),
    url(r'^vid/', views.vid, name='vid'),
    url(r'^vidfile/', views.vidfile, name='vidfile'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)