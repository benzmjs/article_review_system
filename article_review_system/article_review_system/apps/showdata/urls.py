from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^showdata/', views.Showdata.as_view()),
    url(r'^update/',views.UpdateData.as_view()),
    url(r'^delete/',views.DeleteData.as_view()),
    url(r'^publish/',views.PublishData.as_view())
]