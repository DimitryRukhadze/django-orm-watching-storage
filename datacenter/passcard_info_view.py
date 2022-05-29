from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.filter(passcode=passcode)[0]
    passcard_visits = Visit.objects.filter(passcard=passcard.pk)

    passcard_visits_serialized = [
        {
            'entered_at': visit.entered_at,
            'duration': visit.format_duration(),
            'is_strange': visit.is_visit_long()
        }
        for visit in passcard_visits
    ]

    context = {
        'passcard': passcard,
        'this_passcard_visits': passcard_visits_serialized
    }
    return render(request, 'passcard_info.html', context)
