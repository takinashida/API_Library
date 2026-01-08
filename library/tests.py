from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta
from library.models import Book, Author, Loan

User = get_user_model()


class AuthorViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user", email="user@mail.com", password="pass123"
        )

        self.author = Author.objects.create(
            name="Leo",
            surname="Tolstoy",
            second_name="N"
        )

        self.url_list = reverse("library:author-list")
        self.url_detail = lambda pk: reverse("library:author-detail", args=[pk])

    # LIST #######################################################
    def test_author_list_auth_required(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 401)

    def test_author_list_ok(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)

    # CREATE #####################################################
    def test_create_author_ok(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url_list, {
            "name": "Fyodor",
            "surname": "Dostoevsky",
            "second_name": "M"
        })
        self.assertEqual(response.status_code, 201)

    # RETRIEVE ###################################################
    def test_retrieve_author_ok(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url_detail(self.author.id))
        self.assertEqual(response.status_code, 200)

    # UPDATE #####################################################
    def test_update_author_ok(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch(
            self.url_detail(self.author.id),
            {"surname": "Толстой"}
        )
        self.assertEqual(response.status_code, 200)

    # DELETE #####################################################
    def test_delete_author_ok(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.url_detail(self.author.id))
        self.assertEqual(response.status_code, 204)


class BookViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user", email="user@mail.com", password="pass123"
        )

        self.author = Author.objects.create(
            name="Leo",
            surname="Tolstoy",
            second_name="N"
        )

        self.book = Book.objects.create(
            title="War and Peace",
            author=self.author,
            genre="novel",
            all_count=5,
            count_available=5
        )

        self.url_list = reverse("library:book-list")
        self.url_detail = lambda pk: reverse("library:book-detail", args=[pk])

    # LIST #######################################################
    def test_book_list_ok(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)

    def test_book_filter_by_author(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url_list, {"author": self.author.id})
        self.assertEqual(response.status_code, 200)

    # CREATE #####################################################
    def test_create_book_ok(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url_list, {
            "title": "Anna Karenina",
            "author": self.author.id,
            "genre": "novel",
            "all_count": 3,
            "count_available": 3
        })
        self.assertEqual(response.status_code, 201)

    # UPDATE #####################################################
    def test_update_book_ok(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch(
            self.url_detail(self.book.id),
            {"genre": "classic"}
        )
        self.assertEqual(response.status_code, 200)

    # DELETE #####################################################
    def test_delete_book_ok(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.url_detail(self.book.id))
        self.assertEqual(response.status_code, 204)





class LoanViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user", email="user@mail.com", password="pass123"
        )

        self.author = Author.objects.create(
            name="Leo",
            surname="Tolstoy",
            second_name="N"
        )

        self.book = Book.objects.create(
            title="War and Peace",
            author=self.author,
            genre="novel",
            all_count=2,
            count_available=2
        )

        self.url_list = reverse("library:loan-list")
        self.url_detail = lambda pk: reverse("library:loan-detail", args=[pk])

    # CREATE #####################################################
    def test_create_loan_ok(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url_list, {
            "user": self.user.id,
            "book": self.book.id,
            "return_at": (now() + timedelta(days=7)).isoformat(),
            "is_active": True
        })
        self.assertEqual(response.status_code, 201)

    def test_book_count_decreases(self):
        self.client.force_authenticate(self.user)
        self.client.post(self.url_list, {
            "user": self.user.id,
            "book": self.book.id,
            "return_at": (now() + timedelta(days=7)).isoformat(),
            "is_active": True
        })
        self.book.refresh_from_db()
        self.assertEqual(self.book.count_available, 1)

    # LIST #######################################################
    def test_loan_list_ok(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)
