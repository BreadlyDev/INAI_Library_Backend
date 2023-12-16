from django.db import models
from django.utils import timezone
from users.models import User
from books.models import Book

ORDER_STATUS = (
    ("Ожидает проверки", "Ожидает проверки"),
    ("В обработке", "В обработке"),
    ("Выполнен", "Выполнен"),
    ("Отклонено", "Отклонено"),
)


class OrderBook(models.Model):
    order = models.ForeignKey("Order", on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = "orders_books"


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, through=OrderBook)
    status = models.CharField(max_length=50, choices=ORDER_STATUS, default=ORDER_STATUS[0][0])
    comment = models.TextField(default="", blank=True)
    created_time = models.DateTimeField(default=timezone.now)
    due_time = models.DateField()

    class Meta:
        ordering = ["-created_time"]
        db_table = "orders"

    def formatted_created_time(self):
        local_time = timezone.localtime(self.created_time)
        return local_time.strftime("%d-%m-%y %H:%M:%S")

    def __str__(self):
        return f"Order by {self.owner} at {self.formatted_created_time()}"
