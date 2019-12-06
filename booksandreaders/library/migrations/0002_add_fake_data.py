import logging
import random
import sys
from random import randint
from django.db import migrations
from faker import Faker
from faker.providers import isbn
from booksandreaders.library.models import (
    Book,
    Reader,
)


log = logging.getLogger(__name__)


fake = Faker()
Faker.seed(1)
fake.add_provider(isbn)

random.seed(1)

BATCH_SIZE = 5000
READERS_COUNT = 50000
BOOKS_COUNT = 100000

colors = (
    '\033[35m',
    '\033[0m',
)


def chunks(lst, n):
    n = int(n)
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def add_fake_data(apps, schema_editor):
    if 'test' in sys.argv:
        log.debug('Fake data will not be added during tests')
        return
    add_fake_readers()
    add_fake_books()


def add_fake_readers():
    log.debug(f'{colors[0]}Readers: generating {READERS_COUNT} fake readers{colors[1]}')
    fake_readers = [Reader(name=fake.name()) for i in range(0, READERS_COUNT)]
    i = 1
    for batch in chunks(fake_readers, BATCH_SIZE):
        Reader.objects.bulk_create(batch, BATCH_SIZE)
        log.debug(f'Readers: batch #{i:0>2d} completed')
        i += 1


def add_fake_books():
    log.debug(f'{colors[0]}Books: querying all fake readers{colors[1]}')
    fake_readers = list(Reader.objects.all().only('id'))
    log.debug(f'{colors[0]}Books: generating {BOOKS_COUNT} fake books; It may take a minute or two{colors[1]}')
    fake_books = [Book(
        name=fake.text(100).replace('\n', ' '),
        isbn=fake.isbn13(separator='-'),
        reader=fake_readers[randint(0, READERS_COUNT - 1)]
    ) for i in range(0, BOOKS_COUNT)]
    i = 1
    for batch in chunks(fake_books, BATCH_SIZE):
        Book.objects.bulk_create(batch, BATCH_SIZE)
        log.debug(f'Books: batch #{i:0>2d} completed')
        i += 1


class Migration(migrations.Migration):

    initial = False

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_fake_data),
    ]
