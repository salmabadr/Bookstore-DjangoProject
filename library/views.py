from django.db.models import Max, Avg
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm,SignupForm
from django.contrib import messages
from .models import Book, Author, FollowingAuthor, FavouriteCat, UserBookRel,Category
from django.contrib.auth.hashers import check_password

def reg_into(request):
    form=SignupForm()
    return render(request, 'library/register.html',{'form': form})

def reg_check(request):
    flag=False
    users = User.objects.all()
    uname=request.POST['username']
    passwd=request.POST['password']
    for user in users:
        if uname==user.username:
            if check_password(passwd, user.password):
                flag=True
    if flag==True:
        messages.error(request, 'this user already exists')
        return redirect('/library/reg')
    else:
        user = User.objects.create_user(request.POST['username'],request.POST['email'],request.POST['password'])
        user.first_name = request.POST['fname']
        user.last_name = request.POST['lname']
        user.save()
        form = LoginForm()
        form.fields["username"].initial=uname
        return render(request,'library/loginagain.html',{'form': form})

def log_into(request):
    form = LoginForm()
    return render(request, 'library/login.html',{'form': form})

def log_check(request):
    uname = request.POST['username']
    pwd = request.POST['password']
    user = authenticate(username=uname, password=pwd)
    if user is not None:
        login(request,user)
        request.session['user_id'] = user.id
        return redirect('/library/homepage')

    else:
        messages.error(request,'wrong username or password')
        return redirect('/library/login')

def go_to_homepage(request):
    userid=request.session['user_id']
    currentuser=User.objects.get(pk=userid)
    favcat = FavouriteCat.objects.filter(userid=userid)
    booklist_cat = []
    for c in favcat:
        book = Book.objects.filter(category_id=c.categoryid).aggregate(max_id=Max('pk'))
        bookid=book.get('max_id')
        if bookid != None:
            book=Book.objects.get(pk=bookid)
            booklist_cat.append(book)

    followauthor = FollowingAuthor.objects.filter(userid=userid)
    booklist_auth = []
    for a in followauthor:
        book = Book.objects.filter(writer_id=a.authorid).aggregate(max_id=Max('pk'))
        bookid = book.get('max_id')
        if bookid != None:
            book = Book.objects.get(pk=bookid)
            booklist_auth.append(book)


    return render(request, 'library/home.html', context={"username": currentuser.username, "cat_books": booklist_cat, "auth_books": booklist_auth})

def show_books(request):
    books = UserBookRel.objects.filter(userid=request.session['user_id'])
    list=[]
    for b in books:
        list.append(b.bookid_id)
    booklist=Book.objects.filter(pk__in=list)
    return render(request, 'library/books.html',context={"booklist": booklist})

def get_book_info(request,id):
    book = Book.objects.get(pk=id)
    currbook=UserBookRel.objects.get(bookid=id, userid=request.session['user_id'])
    b = UserBookRel.objects.filter(bookid=id).aggregate(Avg('rating'))
    book.avgrating = b['rating__avg']
    if currbook:
            book.status = currbook.status
            book.rating=currbook.rating
    else:
            book.status=""
            book.rating=0

    return render(request, 'library/bookinfo.html',context={"book": book})

def save_bookinfo(request,id):
    book = UserBookRel.objects.get(bookid=id)
    book.status=request.POST['sel']
    book.rating=request.POST['in']
    book.save()
    return redirect('/library/showbooks')

def listauthors(request):
    authors=Author.objects.all()
    followids=[]
    following=[]
    notfollowing=[]
    auths=FollowingAuthor.objects.filter(userid_id=request.session['user_id'])
    for a in auths:
        followids.append(a.authorid_id)
    for a in authors:
        if a.id in followids:
            following.append(a)
        else:
            notfollowing.append(a)

    return render(request, 'library/authors.html', context={"following": following, "notfollowing":notfollowing})

def getbook(request,id):
    pass

def view_categories(request):
    categories=Category.objects.all()
    cats=FavouriteCat.objects.filter(userid=request.session['user_id'])
    favids=[]
    favcat=[]
    notfavcat=[]
    for i in cats:
        favids.append(i.categoryid_id)
    for c in categories:
        if c.id in favids:
            favcat.append(c)
        else:
            notfavcat.append(c)
    return render(request, 'library/categories.html', context={"favcat": favcat,"notfavcat": notfavcat})

def addtofav(request,id):
    category = FavouriteCat(userid_id=request.session['user_id'], categoryid_id=id)
    category.save()
    return redirect('/library/categories')

def removefav(request,id):
    FavouriteCat.objects.filter(categoryid_id=id,userid_id=request.session['user_id']).delete()
    return redirect('/library/categories')

def showcatbooks(request,id):
    category=Category.objects.get(pk=id)
    books=Book.objects.filter(category_id=id)
    return render(request, 'library/categorybooks.html', context={"category": category,"books":books})

def showauthbooks(request,id):
    author=Author.objects.get(pk=id)
    books= Book.objects.filter(writer_id=id)
    return render(request, 'library/authorinfo.html', context={"author": author, "books": books})
    pass

def follow(request,id):
    author = FollowingAuthor(userid_id=request.session['user_id'], authorid_id=id)
    author.save()
    return redirect('/library/authors')

def unfollow(request,id):
    FollowingAuthor.objects.filter(authorid_id=id,userid_id=request.session['user_id']).delete()
    return redirect('/library/authors')
# def get_secondhomepage(request):
#     if request.user.is_authenticated():
#         if 'user_id' in request.session and request.session['user_id']:
#
#         else:
#             pass
# def home_view(request):
#     if request.user.is_authenticated():
#         return render(request, 'library/home.html')
#     else:
#         pass