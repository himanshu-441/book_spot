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

    def safe_year(value):
            try:
                value = value.strip()
                if value.isdigit() and len(value) == 4:
                    return int(value)
            except Exception:
                pass
            return 2000 



    def handle(self, *args, **options):
        csv_path = options['csv']
        books_buffer = []
        created = 0

        with open(csv_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)


            for idx, row in enumerate(reader, start=1):
                title = row.get("Book-Title")
                author = row.get("Book-Author")
                year = Command.safe_year(row.get("Year-Of-Publication"))
                isbn = row.get("ISBN")
                language = "en"
                image = row.get("Image-URL-M")
                self.stdout.write(f"{title} rows processed")
                if not title or not author:
                    continue

                books_buffer.append(
                    Book(
                        name=title[:200],
                        author=author[:150],
                        arrival=year,
                        isbn=isbn,
                        language=language[:20],
                        image=image,
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

        
