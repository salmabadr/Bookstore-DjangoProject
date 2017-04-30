from django.contrib import admin
from .models import Book,Author,Category,FollowingAuthor,FavouriteCat,UserBookRel

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(FollowingAuthor)
admin.site.register(FavouriteCat)
admin.site.register(UserBookRel)
# admin.site.register(User)