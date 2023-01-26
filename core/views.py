from django.shortcuts import render





def show_calendar(request):
    return render('schedule/calendar.html')
