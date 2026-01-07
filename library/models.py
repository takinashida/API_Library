from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    surname = models.CharField(max_length=255, verbose_name="Фамилия")
    second_name = models.CharField(max_length=255,verbose_name="Отчество", null=True, blank=True)

    def __str__(self):
        return f"{self.surname} {self.name} {self.second_name if self.second_name else ""}"

    class Meta:
        verbose_name = "автор"
        verbose_name_plural = "авторы"


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    author = models.ForeignKey("library.Author", on_delete=models.CASCADE, verbose_name="Автор")
    genre = models.CharField(max_length=100, verbose_name="Жанр")
    count_available = models.PositiveIntegerField(verbose_name="Осталось")
    all_count = models.PositiveIntegerField(verbose_name="Всего")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "книга"
        verbose_name_plural = "книги"


class Loan(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="Прокатчик")
    book = models.ForeignKey("library.Book", on_delete=models.CASCADE, verbose_name="Книга")
    taken_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата выдачи")
    return_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата возврата")
    is_active = models.BooleanField(verbose_name="Актуальность", default=True)
    is_overdue = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} {self.book} {self.taken_at} {self.is_active}"

    class Meta:
        verbose_name = "прокат"
        verbose_name_plural = "прокат"
