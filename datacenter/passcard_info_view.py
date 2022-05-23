from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render


def is_visit_long(visit_to_check, minutes=60):
    time_to_check = minutes*60
    visit_duration = visit_to_check.get_visit_duration().total_seconds()
    return visit_duration > time_to_check

def passcard_info_view(request, passcode):
    passcard = Passcard.objects.filter(passcode=passcode)[0]

    this_passcard_visits = [
        {
            'entered_at': visit.entered_at,
            'duration': visit.format_duration(),
            'is_strange': is_visit_long(visit)
        }
        for visit in Visit.objects.filter(passcard=passcard.pk)
    ]

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
