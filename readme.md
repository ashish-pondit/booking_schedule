# Django-Scheduler

## Models

Here are the major models of Django-Scheduler
1. [Calendar](#1-calendar)
2. [CalendarRelation](#2-calendarrelation)
3. [Event](#3-event)
4. [EventRelation](#4-eventrelation)
5.  [Rule](#5-rule)
6. [Occurrence](#6-occurrence)

### 1. Calendar

```python

from schedule.models import Calendar

# Create a Calendar
calendar = Calendar(name = 'Test Calendar')
calendar.save()
# Get all calendars
all_calendars = Calendar.objects.all()

```
-----

### 2. CalendarRelation

This is for relating data to a Calendar, and possible all of the events for
that calendar, there is also a distinction, so that the same type or kind of
data can be related in different ways.  A good example would be, if you have
calendars that are only visible by certain users, you could create a
relation between calendars and users, with the distinction of 'visibility',
or 'ownership'.  If inheritable is set to true, all the events for this
calendar will inherit this relation.

- calendar: a foreign key relation to a Calendar object.
- content_type: a foreign key relation to ContentType of the generic object
- object_id: the id of the generic object
- content_object: the generic foreign key to the generic object
- distinction: a string representing a distinction of the relation, User could
have a 'veiwer' relation and an 'owner' relation for example.
- inheritable: a boolean that decides if events of the calendar should also
inherit this relation

**DISCLAIMER:** while this model is a nice out of the box feature to have, it
may not scale well.  If you use this, keep that in mind.

------
### 3. Event

This model stores metadata for a date.  You can relate this data to many
other models.

```python
from schedule.models import Calendar,Event
import datetime
import pytz

time_zone = pytz.timezone('Asia/Dhaka')

calendar = Calendar.objects.get(name="Test Calendar")

data = {'title': 'Recent Event',
        'start': datetime.datetime(2023, 1, 5, 0, 0,tzinfo=time_zone),
        'end': datetime.datetime(2023, 1, 10, 0, 0,tzinfo=time_zone)
        }
event1 = Event(**data)
event1.calendar = calendar
event1.save()
# List all events
all_events = Event.objects.all()
```
Here the calendar objects refer to the Calendar that we created earlier.

`Events` and `Calendar` have many-to-one relation. So we can also list events from calendar.

```python
# find all events from a calendar
all_events = calendar.events.all()
```


### 4. EventRelation

This is for relating data to an Event, there is also a distinction, so that
data can be related in different ways.  A good example would be, if you have
events that are only visible by certain users, you could create a relation
between events and users, with the distinction of 'visibility', or
'ownership'.

event: a foreign key relation to an Event model.
content_type: a foreign key relation to ContentType of the generic object
object_id: the id of the generic object
content_object: the generic foreign key to the generic object
distinction: a string representing a distinction of the relation, User could
have a 'viewer' relation and an 'owner' relation for example.

**DISCLAIMER:** while this model is a nice out of the box feature to have, it
may not scale well.  If you use this keep that in mind.


---
### 5. Rule

A rule defines how an event will recur. This is applicable for recurring events.
This defines a rule by which an event will recur.  This is defined by the
rrule in the dateutil documentation.

* name - the human friendly name of this kind of recursion.
* description - a short description describing this type of recursion.
* frequency - the base recurrence period
* param - extra params required to define this type of recursion. The params
  should follow this format:

param = [rruleparam:value;]*

rruleparam = see list below
value = int[,int]*

The options are: (documentation for these can be found at [here](https://dateutil.readthedocs.io/en/stable/rrule.html#module-dateutil.rrule) )
- count
- bysetpos
- bymonth
- bymonthday
- byyearday
- byweekno
- byweekday
- byhour
- byminute
- bysecond
- byeaster

|            |           |
|------------|-----------|
| count      | byweekday |
| bysetpos   | byhour    |
| bymonth    | byminute  |
| bymonthday | bysecond  |
| byyearday  | byeaster  |
| byweekno   |           |


Let's create a rule 

```python
from schedule.models import Calendar,Event,Occurrence,Rule
data = {
        'name': 'Weekly',
        'frequency': 'WEEKLY'
       }

weekly_rule = Rule(**data)
weekly_rule.save()
```
----
### 6. Occurrence

An occurrence is an instance of an event. Occurrence is for repeated  `Event` .
If we have an event and it is Weekly staff  meetings which occur every Tuesday, 
then next Tuesday’s staff meeting is an occurrence.

So using `Occurrence` an instance of a repeated `Event` can be modified or cancelled.
Let's see it in action. Before that we need to create an recurring `Event`.  So let's do that first and then we will see
how `Recurrence` works. 

```python
from schedule.models import Calendar,Event,Occurrence,Rule
import datetime
import pytz

time_zone = pytz.timezone('Asia/Dhaka')

calendar = Calendar.objects.get(name="Test Calendar")
weekly_rule = Rule.objects.get(name="Weekly")
data = {'title': 'Daily Exercise',
        'start': datetime.datetime(2023, 2, 1, 12, 0,tzinfo=time_zone),
        'end': datetime.datetime(2023, 2, 1, 12, 30,tzinfo=time_zone),
        'end_recurring_period': datetime.datetime(2024, 2, 1, 0, 0,tzinfo=time_zone),
        }

event2 = Event(**data)
event2.calendar = calendar
event2.rule = weekly_rule
event2.save()

# List all events
all_events = Event.objects.all()
[event.title for event in all_events]
```

**Output**
```
['Recent Event', 'Daily Exercise']
```

We've created a recurrence event named `Daily Exercise`. In the `start` and `end` time defines the first instance of the
event. The `end_recurring_period` determines for how long it will be repeated. Now between the first instance of the 
event and the `end_recurring_period` the event will be repeated as par the `rule`. Here, we've set the weekly rule that
was created earlier. Since the rule is to repeat the event weekly so let's check the weekday of the first instance of
the event.

```python
import datetime
import pytz

time_zone = pytz.timezone('Asia/Dhaka')
start_date = datetime.datetime(2023, 2, 1, 12, 0, tzinfo=time_zone)
start_date.strftime('%A')
```
**Output**
```
Wednesday
```
Since the first day is **Wednesday**, so this event will be repeated for every **Wednesday** from 12:00 to 12:30.
This event will be continued until the `end_recurring_period` date.

-----

Now think of one instance among these where we want to change 'Daily Exercise' time or cancel it. How do we do it?
This event instance is called **occurrence**.

For example: <br>
Let's say for date `2023/03/01` is Wednesday and we want to change the time for **Daily Exercise** for this day.
This instance is called occurrence of a recurring event.

```python
from schedule.models import Calendar,Event,Occurrence,Rule
import datetime
import pytz

time_zone = pytz.timezone('Asia/Dhaka')

event = Event.objects.get(title="Daily Exercise")
data = {'title': 'Exercise Time Change',
        'start': datetime.datetime(2023, 3, 1, 14, 0,tzinfo=time_zone),
        'end': datetime.datetime(2023, 3, 1, 14, 30,tzinfo=time_zone),
        'cancelled': False,
        'original_start': datetime.datetime(2023, 3, 1, 12, 0,tzinfo=time_zone),
        'original_end': datetime.datetime(2023, 3, 1, 12, 30,tzinfo=time_zone),
        
        }
occurrence1 = Occurrence(**data)
occurrence1.event = event
occurrence1.save()
# List all the Occurrence
all_occurrences = Occurrence.objects.all()
[(occurrence.title,occurrence.start,occurrence.end) for occurrence in all_occurrences]
```
**Output**
```
[('Exercise Time Change',
  datetime.datetime(2023, 3, 1, 8, 0, tzinfo=<UTC>),
  datetime.datetime(2023, 3, 1, 8, 30, tzinfo=<UTC>))]
```
In the `datetime` field, we passed an additional parameter `tzinfo`. It is used to tell system about  the timezone.
We will not describe it here in detail.

------
## How to get list of occurrences
Because some Event can recur indefinitely, you cannot have a function like, `event.get_all_occurrences()`, because that
would be an infinite list.

### get_occurrences()
So instead we have to define the interval to view occurrences between that interval. In the below example we have
defined a start date and end date. All the occurrences in this time interval will be shown.

```python
from schedule.models import Calendar,Event,Occurrence,Rule
import datetime
import pytz

time_zone = pytz.timezone('Asia/Dhaka')

event = Event.objects.get(title='Daily Exercise')

start_time = datetime.datetime(2023, 2, 8, 0, 0,tzinfo=time_zone)
end_time = datetime.datetime(2023, 3, 1, 23, 00,tzinfo=time_zone)

all_occurrences = event.get_occurrences(start=start_time,end=end_time)

for occurrence in all_occurrences:
  print("Title: {} \t\nStart: {} \t\nEnd: {} \t\n".format(occurrence.title,occurrence.start,occurrence.end))

```

The output is self-explanatory.

### occurrences_after()
This method produces a generator that generates events inclusively after the given datetime after. If no date is given 
then it uses now.

```python
from schedule.models import Calendar,Event,Occurrence,Rule
import datetime
import pytz

time_zone = pytz.timezone('Asia/Dhaka')

event = Event.objects.get(title='Daily Exercise')
start_time = datetime.datetime(2023, 1, 30, 11, 0,tzinfo=time_zone)
all_occurrences = event.occurrences_after(start_time)

for occurrence in all_occurrences:
  print("Title: {} \t\nStart: {} \t\nEnd: {} \t\n".format(occurrence.title,occurrence.start,occurrence.end))

```
Using the above methods we can get occurrences of a single events. In real life application there can be serveral events
. So now we will see how we can get occurrences from multiple events. Before that let's create some more events.

```python
from schedule.models import Calendar,Event,Rule
import datetime
import pytz

time_zone = pytz.timezone('Asia/Dhaka')

calendar = Calendar.objects.get(name="Test Calendar")

data = {'title': 'Ekushey February',
        'start': datetime.datetime(2023, 2, 21, 0, 0,tzinfo=time_zone),
        'end': datetime.datetime(2023, 2, 21, 23, 59,tzinfo=time_zone)
        }
event3 = Event(**data)
event3.calendar = calendar
event3.save()

weekly_rule = Rule.objects.get(name="Weekly")
data = {'title': 'Go to the Temple',
        'start': datetime.datetime(2023, 2, 3, 8, 0,tzinfo=time_zone),
        'end': datetime.datetime(2023, 2, 3, 8, 30,tzinfo=time_zone),
        'end_recurring_period': datetime.datetime(2023, 4, 1, 0, 0,tzinfo=time_zone),
        }

event4 = Event(**data)
event4.calendar = calendar
event4.rule = weekly_rule
event4.save()
```
----



## Periods

One of the goals of DjangoSchedule is to make occurrence generation and persistence easy. To do this it creates simple
classes for accessing these occurrences. These are Periods. Period is an object that is initiated with an iterable 
object of events, a start datetime, and an end datetime.

It is common to subclass Period for common periods of time. Some of these already exist in the project. Year, Month,
Week, Day.

```python
from schedule.models import Calendar,Event,Rule
from schedule.periods import Period
import datetime
import pytz

time_zone = pytz.timezone('Asia/Dhaka')
all_events = Event.objects.all()
start = datetime.datetime(2023,2,1,0,0,tzinfo=time_zone)
end = datetime.datetime(2023,3,1,0,0,tzinfo=time_zone)

period = Period(all_events,start,end)

all_occurrences = period.get_occurrences()

for occurrence in all_occurrences:
  print("Title: {} \t\nStart: {} \t\nEnd: {} \t\nClass: {} \t\n".format(occurrence.title,occurrence.start,occurrence.end,))


```


**Time Zone Note**


```python


from django.utils.timezone import localtime



localtime(tt.start)


#datetime.datetime(2023, 3, 1, 13, 58, tzinfo=<DstTzInfo 'Asia/Dhaka' +06+6:00:00 STD>)


```

--------

## Time Zone in Django

Naive and aware datetime objects¶
Python’s datetime.datetime objects have a tzinfo attribute that can be used to store time zone information, represented
as an instance of a subclass of datetime.tzinfo. When this attribute is set and describes an offset, a datetime object 
is aware. Otherwise, it’s naive.

```python
from datetime import datetime
from django.utils import timezone as dtz

# Naive Datetime
print(datetime.now())

# Timezone aware datetime
print(dtz.now())

```

**Output**
```
2023-01-30 17:19:33.638018
2023-01-30 11:19:33.638134+00:00
```

In the second output you can see additional +00:00 which means the second datetime is aware and in `UTC` format.

You can use is_aware() and is_naive() to determine whether datetime are aware or naive.

```python
from django.utils.timezone import is_aware, is_naive
from django.utils import timezone as dtz
from datetime import datetime

def check_awareness(dt):
  print(f"Datetime: {dt} \t\nAware: {is_aware(dt)}\t\nNaive: {is_naive(dt)}\t\n")

current_time = datetime.now()
check_awareness(current_time)

current_time = dtz.now()
check_awareness(current_time)

```

**Output**
```

Datetime: 2023-01-30 17:39:39.098868    
Aware: False    
Naive: True     

Datetime: 2023-01-30 11:39:39.099098+00:00      
Aware: True     
Naive: False  

```

We can also convert a **naive** datetime to **aware** datetime and vice versa using `make_aware` and `make_naive`
respectively.

```python

from django.utils.timezone import is_aware, is_naive, make_aware, make_naive
from django.utils import timezone as dtz
from datetime import datetime

def check_awareness(dt):
  print(f"Datetime: {dt} \t\nAware: {is_aware(dt)}\t\nNaive: {is_naive(dt)}\t\n")

current_time = datetime.now()
check_awareness(current_time)

aware_current_time = make_aware(datetime.now())
check_awareness(aware_current_time)
```

