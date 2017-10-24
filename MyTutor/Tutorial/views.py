from ast import literal_eval
from django.contrib import auth
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, datetime, time, timedelta
import time
from .models import Tutor, PrivateTutor, ContractedTutor, MyUser, Notification, TutorialSession, Student, Tutor, Wallet
from decimal import Decimal

COMMISION = 1.05
# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)
#####homepage###
def home(request):
	return render(request, 'home.html')
####login####
def login(request):
	if request.user.is_authenticated(): #visitor or client
		myuser = MyUser.objects.get(user=request.user)
		return HttpResponseRedirect('/Tutorial/' + str(myuser.id)) #searchTutors/'+str(request.user.id)

	username = request.POST.get('username', '')
	password = request.POST.get('password', '')

	user = auth.authenticate(username=username, password=password) #if sucess, should get not none

	if user is not None and user.is_active:
		auth.login(request, user)
		myuser = MyUser.objects.get(user=request.user)
		return HttpResponseRedirect('/Tutorial/' + str(myuser.id))
	else:
		return render(request, 'registration/login.html')

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/Tutorial/')
####search tutor####
def index(request, myuser_id):
	"""all_users = User.objects.all()
	list = []
	for user in all_users:
		html = '<p>User {name} has username: {user_name} </b></p>'
		list.append(html.format(name=user.name, user_name = user.user_name))
	output = '<hr>'.join(list)
	return HttpResponse(output)"""
	all_tutors = Tutor.objects.all()
	private_tutors = PrivateTutor.objects.all()
	myuser = get_object_or_404(MyUser, pk=myuser_id)
	student = get_object_or_404(Student, myuser=myuser)
	params = {"user": myuser, "latest_Tutor_list": all_tutors, 'student': student}
	return render(request, 'searchtutors/index.html', params)


def tutorpage(request, myuser_id, tutor_id):
	tutor = get_object_or_404(Tutor, pk=tutor_id)
	myuser = get_object_or_404(MyUser, pk=myuser_id)
	student = get_object_or_404(Student, myuser=myuser)
	return render(request, 'searchtutors/tutorpage.html', {'user':myuser, 'tutor': tutor, 'student':student})

####my account####
def myaccount(request, myuser_id):
	myuser = get_object_or_404(MyUser, pk=myuser_id)
	return render(request, 'myaccount/myaccount.html', {'user':myuser })

def myprofile(request, myuser_id):
	myuser = get_object_or_404(MyUser, pk=myuser_id)
	return render(request, 'myaccount/myprofile.html', {'user':myuser })

def mybooking(request, myuser_id):
	myuser = get_object_or_404(MyUser, pk=myuser_id)
	mystudent = get_object_or_404(Student,myuser=myuser)
	booking = TutorialSession.objects.filter(student=mystudent)
	return render(request, 'myaccount/mybooking.html', {'user': myuser , 'session_list': booking })

def selectbooking(request, student_id, tutor_id ):	#receive data: starttime (yyyymmddhhmm string)
	begintime = request.POST['starttime']
	tutor = get_object_or_404(Tutor, pk=tutor_id)
	student = get_object_or_404(Student, pk=student_id)
	tutorial_session = tutor.tutorialsession_set.filter(starttime=begintime)

	if tutorial_session: #if it is not empty, you cannot make this session
		return render(request, 'searchtutors/tutorpage.html',
					  {'fail': tutorial_session, 'tutor': tutor, 'student': student, 'begintime': begintime})
	else:
		# time solving
		if PrivateTutor.objects.filter(tutor = tutor).count() == 0:
			thistutor = ContractedTutor.objects.get(tutor = tutor)
		else:
			thistutor = PrivateTutor.objects.get(tutor = tutor)
		wallet = student.myuser.wallet
		if wallet.balance < thistutor.hourly_rate * COMMISION:
			return #fixme should report that not enough money
		wallet.balance = wallet.balance - Decimal.from_float(thistutor.hourly_rate * COMMISION) #fixme didn't add money to tutor account
		wallet.save()
		timeformat = '%Y%m%d%H%M'  # fixme currently I don't care about exceed 14 days, or illegal booking ,only check availability
		bookingtime = time.mktime(datetime.strptime(begintime, timeformat).timetuple())
		now = datetime.now()
		showingtime = time.mktime(datetime(now.year, now.month, now.day, 0, 0).timetuple())
		half_hour_diff = int(bookingtime - showingtime) / 1800
		hour_diff = int (half_hour_diff / 2)
		#modify timeslot string
		timeslot = list(tutor.timeslot)
		timeslot[hour_diff] = '0'
		tutor.timeslot = "".join(timeslot)
		tutor.save()
		tutor.tutorialsession_set.create(starttime=begintime, status=1, tutor=tutor, student=student)
		#message delivering
		content = "System notification [ " + str(datetime(now.year, now.month, now.day, now.hour, now.minute)) + " ]: You have booked a session on " + str(datetime.strptime(begintime, timeformat)) + " with tutor " + tutor.myuser.user.username + " ,with wallet balance deduced by " + str(thistutor.hourly_rate * COMMISION) + " to " + str(wallet.balance)
		notification = Notification(content = content, myuser = student.myuser)
		notification.save()
		return render(request, 'searchtutors/tutorpage.html', {'success': tutorial_session, 'tutor': tutor, 'student': student})


def cancelbooking(request, myuser_id, tutorial_sessions_id): #, student_id, tutor_id):
	#begintime = request.POST['starttime']
	tutorial_session =get_object_or_404(TutorialSession, pk=tutorial_sessions_id)
	tutor = tutorial_session.tutor
	#student = tutorial_session.student
	myuser = get_object_or_404(MyUser, pk=myuser_id)
	timeformat = '%Y%m%d%H%M'  # fixme currently I don't care about exceed 14 days, or illegal booking ,only check availability
	bookingtime = time.mktime(datetime.strptime(tutorial_session.starttime, timeformat).timetuple())
	now = datetime.now()
	showingtime = time.mktime(datetime(now.year, now.month, now.day, 0, 0).timetuple())
	half_hour_diff = int(bookingtime - showingtime) / 1800
	hour_diff = int(half_hour_diff / 2)
	timeslot = list(tutor.timeslot)
	timeslot[hour_diff] = '1'
	tutor.timeslot = "".join(timeslot)
	tutor.save()
	tutorial_session.status = 3
	tutorial_session.save()
	# message delivering
	content = "System notification [ " + str(
		datetime(now.year, now.month, now.day, now.hour, now.minute)) + " ]: You have cancelled the session on " + str(
		datetime.strptime(bookingtime, timeformat)) + " with tutor " + tutor.myuser.user.username
	notification = Notification(content=content, myuser=myuser)
	notification.save()
	return render(request, 'myaccount/mybooking.html', {'myuser': myuser})

def mywallet(request, myuser_id):
	myuser = get_object_or_404(MyUser, pk=myuser_id)
	return render(request, 'myaccount/mywallet.html', {'user':myuser })

####message####
def message(request, myuser_id):
	myuser = get_object_or_404(MyUser, pk=myuser_id)
	messages = Notification.objects.filter(myuser=myuser)
	return render(request, 'message/message.html', {'user': myuser, 'messages': messages})
