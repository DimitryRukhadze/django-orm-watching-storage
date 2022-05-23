from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render


def storage_information_view(request):
    curr_visits = Visit.objects.filter(leaved_at=None)
    curr_visits_info = [
        {
            'who_entered': visit.passcard.owner_name,
            'entered_at': visit.entered_at,
            'duration': visit.format_duration
        }
        for visit in curr_visits
    ]

    context = {
        'non_closed_visits': curr_visits_info,
    }
    return render(request, 'storage_information.html', context)
