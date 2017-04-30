from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# user = User.objects.create_user('mohamed', 'mohamed@gmail.com', '123')
#
# # USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', User)
# # Update fields and then save again
# user.first_name = 'ahmed'
# user.last_name = 'badr'
# user.save()

class Book(models.Model):
    title = models.CharField(max_length=100)
    publishedAt = models.DateField()
    summary=models.CharField(max_length=300)
    country = models.CharField(max_length=100)
    img=models.ImageField()
    writer = models.ForeignKey('Author', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    usersids = models.ManyToManyField(User, through='UserBookRel')
    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=100)
    bornAt = models.DateField()
    diedAt = models.DateField()
    contact = models.IntegerField()
    bio = models.CharField(max_length=100)
    usersids = models.ManyToManyField(User, through='FollowingAuthor')
    def __str__(self):
        return self.name


class Category(models.Model):
    name=models.CharField(max_length=100)
    desc = models.CharField(max_length=300)
    usersids = models.ManyToManyField(User, through='FavouriteCat')
    def __str__(self):
        return self.name


class UserBookRel(models.Model):
    # statusChoices = ('wishlist', 'read', 'reading')
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    bookid = models.ForeignKey('Book', on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(0)]
    )
    status=models.CharField(max_length=100,
                            choices=(('read', 'read'),('wish', 'add to wishlist'),('reading', 'reading')))


class FollowingAuthor(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    authorid = models.ForeignKey('Author', on_delete=models.CASCADE)


class FavouriteCat(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    categoryid = models.ForeignKey('Category', on_delete=models.CASCADE)

