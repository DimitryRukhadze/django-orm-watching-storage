from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render


def storage_information_view(request):
    # Программируем здесь
    curr_visits = Visit.objects.filter(leaved_at=None)
    opened_visits = [
        {
            'who_entered': visit.passcard.owner_name,
            'entered_at': visit.entered_at,
            'duration': visit.format_duration
        }
        for visit in curr_visits
    ]

    context = {
        'non_closed_visits': opened_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
