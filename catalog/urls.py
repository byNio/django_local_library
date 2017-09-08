from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	#for views created from classes we need to call .as_view(). see views.py
	url(r'^books/$', views.BookListView.as_view(), name='books'),
	url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
	#What this regex does is match against any URL that starts with book/, 
	#followed by one or more digits (\d+) before the end of line ($).
	#While performing the matching, it "captures" the digits, 
	#and passes them to the view function as a parameter named pk (?P<pk>).
	
	url(r'^authors/$', views.AuthorListView.as_view(), name='authors'),#list all authors
	url(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
	
	url(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
	url(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book'),
	#(?P<pk>[-\w]+) is used to capture URL [-\w]+ and accessible as 'pk' in views class
]

#urls for generic editing views. see views.py
urlpatterns += [
	url(r'^author/create/$', views.AuthorCreate.as_view(), name="auhtor-create"),
	url(r'^author/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author-update'),
	url(r'^author/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author-delete'),
]