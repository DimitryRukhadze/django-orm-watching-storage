from datetime import timedelta

from django.db import models
from django import utils


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

    def get_visit_duration(self):
        if not self.leaved_at:
            curr_time = utils.timezone.localtime()
            delta = curr_time - self.entered_at
            return delta
        delta = self.leaved_at - self.entered_at
        return delta

    def format_duration(self):
        duration_in_seconds = self.get_visit_duration().total_seconds()
        hours = int(duration_in_seconds // 3600)
        minutes = int((duration_in_seconds % 3600) // 60)
        return f'{hours}:{minutes}:00'

    def is_visit_long(self, minutes=60):
        time_to_check = minutes * 60
        visit_duration = self.get_visit_duration().total_seconds()
        return visit_duration > time_to_check