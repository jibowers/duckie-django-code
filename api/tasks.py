## here is where I'm going to put all the schedules


from datetime import timedelta
from django.utils import timezone
from django_q.tasks import async, schedule
from django_q.models import Schedule
from .models import Duckling, Quack
import arrow

def add_and_notify(duckling):
    ## add new approved quack to duckling's quack list
    previous_id = duckling.quack_list.order_by('-id')[:1].id
    new_quack = Quack.objects.get(is_approved=True).filter(id__gt=previous_id).order_by('id')[:1]

    ducking.quack_list.add(new_quack)

    ## send push notification with this quack (if push enabled)
    

#all schedules will be of scheudle type minute (more flexible)
# but if they choose "daily" on the app, then they can specify a time of day in String HHMM
def update_or_add_schedule(duckling):
    if duckling.notification_schedule is not None:
	# update
	duckling.notification_schedule.minutes = duckling.minute_frequency
    else:
	#create and add schedule
	my_schedule = schedule('add_and_notify',
            duckling,
            schedule_type=Schedule.MINUTES,
            minutes=duckling.minute_frequency,
            repeats=-1)
	duckling.notification_schedule = my_schedule
    if len(duckling.preferred_time) == 4:
	duckling.notification_schedule.next_run=arrow.utcnow().replace(hour=int(time_of_day[:2]), minute=int(time_of_day[2:]))
    else:
	duckling.notification_schedule.next_run= timezone.now() + timedelta(minutes=duckling.minute_frequency)
    duckling.save()
