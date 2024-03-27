from typing import Any

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError


class Command(BaseCommand):
    help = "DEscription of the comamand"

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write("this is my simple task")
