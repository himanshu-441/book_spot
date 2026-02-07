import csv
from django.core.management.base import BaseCommand
from books.models import Book

BATCH_SIZE = 1000


class Command(BaseCommand):
    help = "Bulk seed books from Goodreads CSV (FAST, NO APIs)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv',
            type=str,
            required=True,
            help='Path to Goodreads CSV file'
        )

    def handle(self, *args, **options):
        csv_path = options['csv']
        books_buffer = []
        created = 0

        with open(csv_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for idx, row in enumerate(reader, start=1):
                title = row.get("title")
                author = row.get("authors")
                year = row.get("original_publication_year")
                isbn = row.get("isbn")
                language = row.get("language_code") or "en"

                if not title or not author:
                    continue

                books_buffer.append(
                    Book(
                        name=title[:200],
                        author=author[:150],
                        arrival=int(float(year)) if year else 2000,
                        isbn=isbn,
                        language=language[:20],
                    )
                )

                if len(books_buffer) >= BATCH_SIZE:
                    Book.objects.bulk_create(
                        books_buffer,
                        ignore_conflicts=True
                    )
                    created += len(books_buffer)
                    books_buffer.clear()

                if idx % 10000 == 0:
                    self.stdout.write(f"{idx} rows processed")

        if books_buffer:
            Book.objects.bulk_create(
                books_buffer,
                ignore_conflicts=True
            )
            created += len(books_buffer)

        self.stdout.write(
            self.style.SUCCESS(f"CSV seeding complete → {created} books inserted")
        )
