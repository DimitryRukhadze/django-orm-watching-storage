from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render


def get_person_visits(person_passcard):
    person = person_passcard
    person_visits = Visit.objects.filter(passcard=person.pk)
    return person_visits

def is_visit_long(visit_to_check, minutes=60):
    time_to_check = minutes*60
    visit_duration = visit_to_check.get_visit_duration().total_seconds()
    if visit_duration > time_to_check:
        return True
    return False

def passcard_info_view(request, passcode):
    passcard = Passcard.objects.filter(passcode=passcode)[0]

    this_passcard_visits = [
        {
            'entered_at': visit.entered_at,
            'duration': visit.format_duration(),
            'is_strange': is_visit_long(visit)
        }
        for visit in get_person_visits(passcard)
    ]

    this_passcard_visits1 = [
        {
            'entered_at': '11-04-2018',
            'duration': '25:03',
            'is_strange': False
        },
    ]
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
