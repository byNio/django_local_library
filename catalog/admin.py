from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, Language

admin.site.register(Genre)
admin.site.register(Language)
#admin.site.register(BookInstance)
#admin.site.register(Book)
#admin.site.register(Author)

#adding book data inline author
class BookInline(admin.StackedInline):
	model = Book
	extra = 0
#use modelAdmin to setup admin display for Book, Author, and BookInstance
# 1. define admin class
class AuthorAdmin(admin.ModelAdmin):
	#setup how you want to display Author in admin page
	list_display = ('first_name', 'last_name', 'date_of_birth', "date_of_death")
	#change what fields to display in admin page
	fields = ['first_name', "last_name", ("date_of_birth", 'date_of_death')]
	#optional: adding Book inside author
	inlines = [BookInline]
# 2. Register the modelAdmin class with model to use
admin.site.register(Author, AuthorAdmin)

#add inline associated record
class BookInstanceInline(admin.TabularInline):
	model = BookInstance
	extra = 0
#register the modelAdmin class with Book and BookInstance using @decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	#setup how you want to display Author in admin page
	list_display = ('title', 'author', 'display_genre')
	#add BookInstance inline in Book admin page
	inlines = [BookInstanceInline]
	pass

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
	#setup how you want to display BookInstance in admin page
	list_display = ('id', 'book', 'status', "due_back", 'borrower')

	#setup how you want to filter in admin page
	list_filter = ('status','due_back')
	
	#add section in admin page
	fieldsets = (
		(None, {"fields": ('book', "imprint", "id")}),
		("availability", {'fields': ('status','borrower', 'due_back',)})
	)
	
	

