# Django-Scheduler

## Models

Here are the major models of Django-Scheduler
1. [Calendar](#Calendar)
2. CalendarRelation
3. Event
4. EventRelation
5.  Rule
6. Occurrence 

### 1. Calendar

```python

from schedule.models import Calendar
# Create a Calendar
calendar = Calendar(name = 'Test Calendar')
calendar.save()
# Get all calendars
all_calendars = Calendar.objects.all()

```

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

### 3. Event

This model stores meta data for a date.  You can relate this data to many
other models.

```python
from schedule.models import Calendar,Event
import datetime

calendar = Calendar.objects.get(name="Test Calendar")

data = {'title': 'Recent Event',
        'start': datetime.datetime(2008, 1, 5, 0, 0),
        'end': datetime.datetime(2008, 1, 10, 0, 0)
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

### 6. Occurrence

An occurrence is an instance of an event. Occurrence is for repeated  `Event` .
If we have an event and it is Weekly staff  meetings which occur every Tuesday, 
then next Tuesday’s staff meeting is an occurrence.

So using `Occurrence` an instance of a repeated `Event` can be modified or cancelled.
Let's see it in action. Before that we need to create an recurring `Event`.  So let's do that first and then we will see
how `Recurrence` works. 

```python
from schedule.models import Calendar,Event,Occurrence

```