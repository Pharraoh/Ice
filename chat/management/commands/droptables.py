from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Drops chat-related tables manually'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            self.stdout.write("Dropping tables...")
            cursor.execute("DROP TABLE IF EXISTS chat_chatroom CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS chat_chatmessage CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS chat_status CASCADE;")
            self.stdout.write(self.style.SUCCESS("Tables dropped successfully."))
