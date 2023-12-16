from django.db import models
from main.settings import IMAGE_FOLDER, ERROR_404_IMAGE, E_BOOKS_FOLDER

LANGUAGES = (
    ("Кыргызский", "Кыргызский"),
    ("Русский", "Русский"),
    ("Английский", "Английский"),
    ("Немецкий", "Немецкий"),
)


def validate_price(price):
    if not str(price).isdigit():
        raise ValueError("Invalid price value")


def validate_edition_year(year):
    if not str(year).isdigit():
        raise ValueError("Invalid edition year")


class Category(models.Model):
    title = models.CharField(max_length=150)

    class Meta:
        db_table = "categories"

    def __str__(self):
        return f"Category {self.title}"


class Subcategory(models.Model):
    title = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = "subcategories"

    def __str__(self):
        return f"Subcategory {self.title}"


class Book(models.Model):
    author = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    description = models.TextField(default="No description", blank=True)
    image = models.ImageField(default=ERROR_404_IMAGE, upload_to=IMAGE_FOLDER)
    e_book = models.FileField(upload_to=E_BOOKS_FOLDER)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    inventory_number = models.CharField(max_length=150)
    language = models.CharField(choices=LANGUAGES, max_length=150)
    edition_year = models.CharField(max_length=4)
    purchase_price = models.CharField(max_length=10)
    purchase_time = models.DateField()
    quantity = models.IntegerField()
    isPossibleToOrder = models.BooleanField(default=True)
    rating = models.FloatField(default=0)
    orders = models.IntegerField(default=0)
    reviews_quantity = models.IntegerField(default=0)
    absolute_rating = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["reviews_quantity"]
        db_table = "books"

    def __str__(self):
        return f"{self.title} book with id = {self.pk}"

    def save(self, *args, **kwargs):
        if self.purchase_price:
            validate_price(self.purchase_price)
        if self.edition_year:
            validate_edition_year(self.edition_year)
        super().save(*args, **kwargs)
