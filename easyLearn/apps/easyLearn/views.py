from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Section, Training, Activity, TrainingProgress, SectionProgress, ActivityProgress


def home(request):
    return redirect('/easylearn')


def index(request):
    context = {
        'trainings': Training.objects.all(),
        'sections': Section.objects.all(),
    }
    # print(Training.objects.all())
    return render(request, "index.html", context)


def process(request):
    if request.POST.get('action') == 'registration':
        errors = User.objects.register_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/easylearn')
        else:
            hash_userpw = bcrypt.hashpw(
                str(request.POST['password']).encode(), bcrypt.gensalt())
            # add the user to the DB
            user = User.objects.create()
            user.fname = request.POST['fname']
            user.lname = request.POST['lname']
            user.email = request.POST['email']
            user.password = hash_userpw
            user.save()
            email = request.POST['email']
            user1 = User.objects.get(email=email)
            request.session['id'] = user1.id
            request.session['fname'] = user1.fname
            return redirect('/trainings')

    if request.POST.get('action') == 'login':
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/easylearn')
        email = request.POST['email']
        user1 = User.objects.get(email=email)
        request.session['id'] = user1.id
        request.session['fname'] = user1.fname
        return redirect('/trainings')


def showDashboard(request):
    if 'id' not in request.session:
        return redirect('/easylearn')
    else:
        this_user = User.objects.get(id=request.session['id'])
        print("User is logged showDashboard", this_user.id)

    trainingStatus = TrainingProgress.objects.filter(user_id=this_user.id)

    context = {
        'users': this_user,
        'trainings': Training.objects.all(),
        'trainingStatus': trainingStatus,
        'sections': Section.objects.all()
    }
    return render(request, "dashboard.html", context)


def showTrainingDetail(request, training_id):
    if 'id' not in request.session:
        return redirect('/easylearn')
    else:
        this_user = User.objects.get(id=request.session['id'])

    t = Training.objects.get(id=training_id)

    # Get training logging
    trainingStatusObject = TrainingProgress.objects.filter(
        user_id=this_user.id, training_id=training_id)
    status = ''

    # Check if user is in table
    if trainingStatusObject:
        for status in trainingStatusObject:
            # check if status is completed
            if status.status == 'Completed':
                status = 'Completed'
            elif status.status == 'In Progress':
                print(status.status)
                status = 'In Progress'
            else:
                print(
                    '>> WRONG STATUS DETECTED {id, status}',
                    status.id,
                    status.status)
                status = 'error'
    else:
        # save new entry
        newStatus = TrainingProgress(
            status='In Progress', 
            training_id=training_id, 
            user_id=this_user.id
            )
        newStatus.save()
        status = 'In Progress'
        print('New Status generated')

    allSections = Training.objects.get(id=training_id).sections.all()
    sectionCount = 0
    sectionStatusArray = []

    # get all sections and save their status in array sectionStatusArray
    for section in allSections:
        sectionCount = sectionCount + 1
        for section in section.sectionprogress_set.filter(user_id=this_user.id):
            sectionStatusArray.append(section.status)
        print("All Sections", sectionCount,
              sectionStatusArray.count('Completed'))

    # if the amount of completed sections == to the amount of sections in training -> set the training to completed
    try:
        if sectionCount == sectionStatusArray.count('Completed'):
            newStatus = trainingStatusObject[0]
            newStatus.status = 'Completed'
            newStatus.save()
            print(trainingStatusObject[0].status, '< Training Status')
        print(sectionCount, sectionStatusArray,
              sectionStatusArray.count('Completed'))
    except:
        pass

    context = {
        'status': status,
        'trainings': Training.objects.filter(id=training_id),
        'sections': t.sections.all().order_by('order'),
        'sectionProgresses': SectionProgress.objects.filter(user_id=this_user).all()
    }
    return render(request, "training_detail.html", context)


def startSection(request, section_id, training_id):
    if 'id' not in request.session:
        return redirect('/easylearn')
    else:
        this_user = User.objects.get(id=request.session['id'])

    activities = Activity.objects.filter(section_id=section_id)

    # Get section logging
    sectionStatusObject = SectionProgress.objects.filter(
        user_id=this_user.id, section_id=section_id)

    status = ''

    # Check if user is in table
    if sectionStatusObject:
        for status in sectionStatusObject:
            # Check if status is completed
            if status.status == 'Completed':
                status = 'Completed'
            # Check if status in In Progress
            elif status.status == 'In Progress':
                status = 'In Progress'
            else:
                # Print error if not Completed or In Progress as status
                print(
                    '>> WRONG STATUS DETECTED {id, status}', status.id, status.status)
                status = 'error'
    else:
        # Save new entry in DB if no entry yet
        newStatus = SectionProgress(
            status='In Progress', section_id=section_id, user_id=this_user.id)
        newStatus.save()
        status = 'In Progress'
        print('New Status generated for sectionID:', section_id)

    # Get training logging
    sectionStatusObject = SectionProgress.objects.filter(
        user_id=this_user.id, section_id=section_id)

    allActivities = Training.objects.get(id=training_id).sections.get(
        id=section_id).activity_set.all().order_by("order")
    print(allActivities)

    activityCount = 0
    activityStartArray = []

    # Get all activitys and save their status in array activityStartArray
    for activity in allActivities:
        activityCount = activityCount + 1
        for activity in activity.activityprogress_set.filter(user_id=this_user.id):
            activityStartArray.append(activity.status)

    # Check if the amount of completed activitys is == to the amount of activitys in training, set the training to completed
    try:
        if activityCount == activityStartArray.count('Completed'):
            print(sectionStatusObject[0].status, '< Training Status')
            newStatus = sectionStatusObject[0]
            newStatus.status = 'Completed'
            newStatus.save()
    except:
        pass

    context = {
        'status': status,
        'trainings': Training.objects.filter(id=training_id),
        'sections': Section.objects.filter(id=section_id),
        'activities': activities.order_by('order'),
        'activityProgresses': ActivityProgress.objects.filter(user_id=this_user).all()
    }
    return render(request, "section_detail.html", context)


def startActivity(request, section_id, training_id, activity_id):
    # Get the count from the startSection method to iterate through the sections that you can set the status to complete after the activities are completed
    if 'id' not in request.session:
        return redirect('/easylearn')
    else:
        this_user = User.objects.get(id=request.session['id'])
        print("User is logged startActivity", this_user.id)

    activityIdForNext = []
    activityIdForPrev = []
    nextActivityId = 0
    prevActivityId = 0

    # convert string to int to do calculations. It is a string as the activity_id is comming from the URL
    activity_id = int(activity_id)

    # get all actionIds ordered by 'order'
    allActivities = Training.objects.get(id=training_id).sections.get(
        id=section_id).activity_set.all().order_by('order')

    # go through all until you find the id you are currenty in
    for activity, nextActivity in zip(allActivities, allActivities[1:]):
        if activity.id not in activityIdForNext:
            activityIdForNext.append(activity.id)

        if nextActivity.id not in activityIdForNext:
            activityIdForNext.append(nextActivity.id)

        # get the id from the array which is next
        if activity.id == activity_id:
            # create array nextActivityId
            nextActivityId = nextActivity.id

    # go through all until you find the id you are currenty in
    for prevActivity, activity in zip(allActivities, allActivities[1:]):
        if activity.id not in activityIdForPrev:
            activityIdForPrev.append(activity.id)

        if prevActivity.id not in activityIdForPrev:
            activityIdForPrev.append(prevActivity.id)

        # get the id from the array which is next
        if activity.id == activity_id:
            # create array nextActivityId
            prevActivityId = prevActivity.id

    allActivityStatuses = []
    for activity in allActivities:
        try:
            allActivityStatuses.append(activity.activityprogress_set.get(
                activity_id=activity.id, user_id=user_id).status)
        except:
            pass
    print('allActivityStatuses', allActivityStatuses)

    # Get section logging
    activityStatusObject = ActivityProgress.objects.filter(
        user_id=this_user.id,
        activity_id=activity_id)

    status = ''

    # Check if user is in table
    if activityStatusObject:
        for status in activityStatusObject:
            # check if status is completed
            if status.status == 'Completed':
                status = 'Completed'
            elif status.status == 'In Progress':
                status = 'In Progress'
            else:
                print(
                    '>> WRONG STATUS DETECTED {id, status}', status.id, status.status)
                status = 'error'
    else:
        # save new entry
        newStatus = ActivityProgress(
            status='In Progress', activity_id=activity_id, user_id=this_user.id)
        newStatus.save()
        status = 'In Progress'

    context = {
        'status': status,
        'trainings': Training.objects.filter(id=training_id),
        'sections': Section.objects.filter(id=section_id),
        'actions': Activity.objects.filter(id=activity_id),
        'nextActivity': nextActivityId,
        'prevActivity': prevActivityId
    }
    return render(request, "activity.html", context)


def updateActivity(request, training_id, section_id, activity_id):
    this_user = User.objects.get(id=request.session['id'])
    activityIdForNext = []
    activityIdForPrev = []
    nextActivityId = 0
    prevActivityId = 0

    # convert string to int to do calculations
    activity_id = int(activity_id)

    # get all actionIds ordered by 'order'
    allActivities = Training.objects.get(id=training_id).sections.get(
        id=section_id).activity_set.all().order_by('order')

    # go through all until you find the id you are currenty in
    for activity, nextActivity in zip(allActivities, allActivities[1:]):
        if activity.id not in activityIdForNext:
            activityIdForNext.append(activity.id)

        if nextActivity.id not in activityIdForNext:
            activityIdForNext.append(nextActivity.id)

        # get the id from the array which is next
        if activity.id == activity_id:

            # create array nextActivityId
            nextActivityId = nextActivity.id

    # go through all until you find the id you are currenty in
    for prevActivity, activity in zip(allActivities, allActivities[1:]):
        if activity.id not in activityIdForPrev:
            activityIdForPrev.append(activity.id)

        if prevActivity.id not in activityIdForPrev:
            activityIdForPrev.append(prevActivity.id)

        # get the id from the array which is next
        if activity.id == activity_id:
            # create array nextActivityId
            prevActivityId = prevActivity.id

    allActivityStatuses = []

    for activity in allActivities:
        try:
            allActivityStatuses.append(activity.activityprogress_set.get(
                activity_id=activity.id, user_id=user_id).status)
        except:
            pass

    # Get section logging
    activityStatusObject = ActivityProgress.objects.filter(
        user_id=this_user.id, activity_id=activity_id)

    # Check if user is in table
    if activityStatusObject:
        for status in activityStatusObject:
            # check if status is completed
            if status.status == 'Completed':
                status = 'Completed'
            elif status.status == 'In Progress':
                status = 'In Progress'
            else:
                print(
                    '>> WRONG STATUS DETECTED {id, status}', status.id, status.status)
                status = 'error'
    else:
        # save new entry
        newStatus = ActivityProgress(
            status='In Progress', activity_id=activity_id, user_id=this_user.id)
        newStatus.save()
        status = 'In Progress'
        print('New Status generated')

    user_id = this_user.id
    activityStatus = ActivityProgress.objects.get(
        activity_id=prevActivityId, user_id=user_id)
    activityStatus.status = 'Completed'
    activityStatus.save()
    print("Activity ID", prevActivityId, "updated to Completed")

    context = {
        'trainings': Training.objects.filter(id=training_id),
        'sections': Section.objects.filter(id=section_id),
        'actions': Activity.objects.filter(id=activity_id).all(),
        'nextActivity': nextActivityId,
        'prevActivity': prevActivityId
    }
    return render(request, "activity.html", context)


# method should run only when all activities are completed
def completion(request, training_id, section_id, activity_id):
    if 'id' not in request.session:
        return redirect('/easylearn')
    else:
        this_user = User.objects.get(id=request.session['id'])

    this_user = User.objects.get(id=request.session['id'])
    user_id = this_user.id

    activity = Training.objects.get(id=training_id).sections.get(
        id=section_id).activity_set.get(id=activity_id)
    activityStatus = activity.activityprogress_set.get(
        activity_id=activity.id, user_id=user_id)

    # activityStatus = Training.objects.get(id=training_id).sections.get(id=section_id).activity_set.get(id=activity_id, user_id = user_id)
    activityStatus.status = 'Completed'
    activityStatus.save()

    # Set SectionProgress to Completed
    section_id_int = int(section_id)
    sectionStatus = SectionProgress.objects.get(
        section_id=section_id_int, user_id=user_id)

    allActivities = Activity.objects.filter(section_id=section_id).all()
    allActivities = Training.objects.get(id=training_id).sections.get(
        id=section_id).activity_set.all().order_by('order')
    allSectionStatus = []

    for activity in allActivities:
        try:
            allSectionStatus.append(activity.activityprogress_set.get(
                activity_id=activity.id, user_id=user_id).status)
        except:
            pass

    # Check if all activities per section are completed
    print('completed activities: ', allSectionStatus.count('Completed'))
    # get count of all activities in section
    print('all activities', len(allActivities))
    # check if same amount of actions have status complete as in section in general
    print(allSectionStatus)

    contextMissing = {
        'trainings': Training.objects.filter(id=training_id),
        'sections': Section.objects.filter(id=section_id),
    }

    if allSectionStatus.count('Completed') != len(allActivities):
        return render(request, "missing_activity.html", contextMissing)

    sectionStatus.status = 'Completed'
    sectionStatus.save()

    context = {
        'users': this_user,
        'trainings': Training.objects.filter(id=training_id),
        'sections': Section.objects.filter(id=section_id)
    }
    return render(request, "completed.html", context)


def logout(request):
    request.session.clear()
    return redirect('/easylearn')
