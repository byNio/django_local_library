from django.shortcuts import render

#imports the model classes to access data in all our views.
from .models import Book, Author, BookInstance, Genre, Language

def index(request):
	"""
	View function for homepage
	"""
	#Generate count of some of the main objects
	num_books = Book.objects.all().count()#.all() is implemented by default
	num_instances = BookInstance.objects.all().count()

	#Available books (status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()
	num_authors = Author.objects.count() #all() is implied by default
	
	#use session to track browser
	#session is available in request parameter in every view
	num_visits = request.session.get('num_visits', 0) #session.get('a',b) will get 'a' value if 'a' exist if not create 'a' with def value b
	request.session['num_visits'] = num_visits + 1
	
	#Render the HTML template index.html with data in variable above
	return render(
		request,
		'index.html',
		context = {
			'num_books': num_books,
			'num_instances': num_instances,
			'num_instances_available': num_instances_available,
			'num_authors': num_authors,
			'the_title': "Local Library Homepage",
			'num_visits': num_visits,
		},
	)
	
from django.views import generic
'''
#using generic in django.views there are some defaults provided by django:
1. the file.html by default must be located in catalog/templates/catalog/model_name_list.html
2. the html file get varible called object and model_name(book in this case) which provides same data
'''
class BookListView(generic.ListView):
	model = Book #django give book_list in book_list.html to get array of book
	#django will run template based on model = Book + type of generic view *list*
	#so the template must be named book_list.html
	#in the book_list.html file you can access variable named object_list or book_list(from *the_model_name*_list)
	paginate_by = 2
	#Django has in-built pagination in the generic.ListView
	#just add the paginate_by = 2 in the class
	#this will give html template is_paginated = True, page_obj that provides 
	#information about the current page, previous pages, how many pages there are, etc. 
	
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class BookDetailView(generic.DetailView):
	model = Book #django give book in book_detail.html that will get book data
	#django will run template based on model = Book + type of generic view *detail*
	#so the template must be named book_detail.html
	#in the book_detail.html file you can access variable named object or book(from *the_model_name*)
	'''
	because Book is foreign key in BookInstance then Book can call BookInstance
	by book.bookinstance_set.all in html template
	see book_detail.html
	'''
	
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(BookDetailView, self).dispatch(*args, **kwargs)
	
class AuthorListView(generic.ListView):
	model = Author #expect author_list.html in template that will get author_list data
	paginate_by = 2
	
class AuthorDetailView(generic.DetailView):
	model = Author #expect author_detail.html in template that will get author data
	'''
	because Author is foreign key in Book then Author can call Book
	by author.book_set.all in html template
	see author_detail.html
	'''
	
	
#a mixin that ensure login is required to see the view related
from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
	'''
	Generic class-based view listing books on loan to current user
	'''
	model = BookInstance #django give bookinstance_list in bookinstance_list_borrowed_user.html to get array of BookInstance
	#django will run template based on model = BookInstance + type of generic view *list*
	#so the template must be named bookinstance_list.html
	#in the bookinstance_list.html file you can access variable named object_list or bookinstnace_list(from *the_model_name*)
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	#override the default template_name(bookinstance_list.html) and location(catalog/)
	paginate_by = 10
	#Django has in-built pagination in the generic.ListView
	#just add the paginate_by = 2 in the class
	#this will give html template is_paginated = True, page_obj that provides 
	#information about the current page, previous pages, how many pages there are, etc. 

	# override the  get_queryset() method to change the list of records returned
	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


#working with forms using extend Form class
#check permission to run the def
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
#from django.http import HttpResponseRedirect
#from django.core.urlresolvers import reverse
import datetime
from .forms import RenewBookForm

#the permission is located in models.py
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):#create view using function view called in urls.py also get pk value in urls.py
	'''
	View function for renewing a specific BookInstance
	'''
	
	book_inst = get_object_or_404(BookInstance, pk = pk)
	#Calls get() to get data in model with pk(primary key)
	#https://docs.djangoproject.com/en/1.10/topics/http/shortcuts/#get-object-or-404
	
	if request.method == 'POST':
	#if this is a POST request then process the Form data
		form = RenewBookForm(request.POST)
		#create form obj and populate with data from request(binding data)
		
		#check if form valid
		if form.is_valid():
			#use the data as required
			book_inst.due_back = form.cleaned_data['renewal_date']#change the due_back date in model
			book_inst.save()#save BookInstance model
			
			#redirect to url named index defined in urls.py
			return redirect('index')
	
	#if this is a GET request (or any other method) then create default form to fill
	else:
		#get date 3 weeks from today and passed it to renewal_date default value
		proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
		#create form obj
		form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})
	
	return render(request, 'catalog/book_renew_librarian.html', {'form':form, 'bookinst':book_inst})
	#render the html file using template book_renew_librarian.html
	#also passing values called form and bookinst accesible using {{form}} and {{bookinst}}

#Generic editing views
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author

class AuthorCreate(CreateView):#extends CreateView
	model = Author
	#expect to use template called author_form.html *model_name_form.html in template/catalog
	#template name can be changed by specifying template_name_suffix = '_other_suffix'
	fields = '__all__' #specify the fields to display in the form
	initial = {'date_of_death':'12/10/2016',}
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(AuthorCreate, self).dispatch(*args, **kwargs)

class AuthorUpdate(UpdateView):#extends UpdateView
	model = Author #expect to find template called author_form.html
	fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death',]

class AuthorDelete(DeleteView):#extends DeleteView
	model = Author #expect to find template called author_confirm_delete.html
	#specify an alternative redirect url location
	success_url = reverse_lazy('authors') #redirect to our author url in urls.py
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(AuthorDelete, self).dispatch(*args, **kwargs)
