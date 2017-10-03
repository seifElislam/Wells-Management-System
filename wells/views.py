# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import *
from django.db.models import Q


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth_login(request, user)
                request.session['user_id'] = user.id
                return HttpResponseRedirect('/home/')
            else:
                return HttpResponse('Your account is disabled')
        else:
            print("Invalid login details")
            return render(request, 'wells/login.html', {"error_msg": "Invlaid login details"})
    else:
        return render(request, 'wells/login.html')


@login_required
def index(request):
    wells = Well.objects.all().count()
    users = User.objects.all().count()
    wc = WaterCut.objects.all().aggregate(Max('value'))
    return render(request, 'wells/home.html', {'value': wc['value__max'], "no_wells": wells, "no_users": users})


@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')


@login_required
def users(request):
    if request.method == 'POST':
        pass
    else:
        all_users = User.objects.all()
        return render(request, 'wells/users.html', {'users': all_users})


@login_required
def fields(request):
    if request.method == 'POST':
        if request.POST['name'] != '' and request.POST['location'] != '':
            name = request.POST['name']
            location = request.POST['location']
            print(name, location)
            new_field = Field()
            new_field.name = name
            new_field.location = location
            new_field.save()
            return HttpResponseRedirect('/fields/')
    elif request.method == 'GET':
        all_fields = Field.objects.all()
        return render(request, 'wells/fields.html', {'fields': all_fields})


@login_required
def wells(request):
    if request.method == 'POST':
        if request.POST['name'] != '' and request.POST['date'] != '' and request.POST['normal'] != '':
            name = request.POST['name']
            location = request.POST['location']
            schedule_date = request.POST['date'][5:]
            print(name, location)
            new_schedule = Schedule.objects.get_or_create(date=schedule_date, field=Field.objects.get(id=request.POST['field']))
            # new_schedule = Schedule()
            # new_schedule.date = schedule
            # new_schedule.field = Field.objects.get(id=request.POST['field'])
            # new_schedule.save()
            # schedule_id = new_schedule.id
            new_pump = Pump()
            new_pump.config = request.POST['config']
            new_pump.pump_type = request.POST['pump_type']
            new_pump.pump_depth = request.POST['pump_depth']
            new_pump.save()
            pump_id = new_pump.id
            print('pump id :', pump_id)
            new_well = Well()
            new_well.name = name
            new_well.pump = Pump.objects.get(id=pump_id)
            new_well.location = location
            new_well.field = Field.objects.get(id=request.POST['field'])
            new_well.normal_value = request.POST['normal']
            new_well.statues = request.POST['status']
            # new_well.schedule_id = Schedule.objects.get(id=schedule_id)
            # new_well.check_id = Schedule.objects.get(id=schedule_id)
            new_well.save()
            new_well.schedule_id.add(new_schedule[0])
            # new_well.check_id.add(new_schedule[0])


            return HttpResponseRedirect('/wells/')
    elif request.method == 'GET':
        all_fields = Field.objects.all()
        all_wells = Well.objects.all()
        return render(request, 'wells/well.html', {'fields': all_fields, 'wells': all_wells, 'key': 'All'})


@login_required
def select_wells(request):
    if request.method == 'POST':
        print(type(request.POST['field'].encode('utf8')))
        if request.POST['field'].encode('utf8') != "0":
            print('enter')
            wells = list(Well.objects.filter(field_id=request.POST['field']))
            if wells is not []:
                # wells = ''
                selected_field = Field.objects.get(id=request.POST['field'])
                name = selected_field.name
        else:
            wells = Well.objects.all()
            name = "All"
        all_fields = Field.objects.all()
        return render(request, 'wells/well.html', {'fields': all_fields, 'wells': wells, 'key': name})


@login_required
def operations(request):
    if request.method == 'POST':
        print(type(request.POST['field'].encode('utf8')))
        if request.POST['field'].encode('utf8') != "0":
            print('enter')
            wells = list(Well.objects.filter(field_id=request.POST['field']))
            if wells is not []:
                # wells = ''
                selected_field = Field.objects.get(id=request.POST['field'])
                name = selected_field.name
        else:
            wells = Well.objects.all()
            name = "All"
        all_fields = Field.objects.all()
        return render(request, 'wells/operation.html', {'fields': all_fields, 'wells': wells, 'key': name})
    else:
        wells = Well.objects.all()
        name = "All"
        all_fields = Field.objects.all()
        return render(request, 'wells/operation.html', {'fields': all_fields, 'wells': wells, 'key': name})


@login_required
def schedule(request):
    if request.method == 'POST':
        print(request.POST)
        if request.POST['date'] != '':
            selected_schedule = Schedule.objects.filter(date=request.POST['date'][5:])
            if selected_schedule:
                print("found")
                print(request.POST['date'][5:])
                print(selected_schedule[0].id)
                # wells = Well.objects.filter(schedule_id=selected_schedule[0].id).filter(field_id=request.POST['field'])
                wells = Well.objects.filter(Q(schedule_id=selected_schedule[0].id)|Q(check_id=selected_schedule[0].id)).filter(field_id=request.POST['field'])
            else:
                print("not found")
                wells = ''
            all_fields = Field.objects.all()
            return render(request, 'wells/schedule.html', {'fields': all_fields, 'wells': wells})
    elif request.method == 'GET':
        all_fields = Field.objects.all()
        all_wells = Well.objects.all()
        return render(request, 'wells/schedule.html', {'fields': all_fields, 'wells': all_wells})


@login_required
def get_user(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'wells/user_details.html', {'user': user})


@login_required
def new_user(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/users/')
    if request.method == 'POST':
        if request.POST['username'] != '' and request.POST['password'] != '' and request.POST['email'] != '':
            username = request.POST['username']
            password = request.POST['password']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            print(username, password, first_name, last_name, email)
            User.objects.create_user(
                username=username, first_name=first_name,
                last_name=last_name, password=password,
                email=email)
            return HttpResponseRedirect('/users/')
        else:
            return render(request, 'wells/new_user.html')
    else:

        return render(request, 'wells/new_user.html')


@login_required
def well_info(request, well_id):
    selected_well = Well.objects.get(id=well_id)
    return render(request, 'wells/well_info.html', {'well': selected_well})


@login_required
def well_operations(request, well_id):
    selected_well = Well.objects.get(id=well_id)
    selected_operations = selected_well.operations.all()
    return render(request, 'wells/well_operation.html', {'well': selected_well, 'operations': selected_operations})


@login_required
def add_operations(request, well_id):
    if request.method == 'POST':
        if request.POST['gross'] != '':
            performance = OperationPerformance()
            performance.gross = request.POST['gross']
            performance.net = request.POST['net']
            performance.gor = request.POST['gor']
            performance.dfl = request.POST['dfl']
            performance.liq = request.POST['liq']
            performance.wc = request.POST['wc']
            performance.sep_p = request.POST['sep_p']
            performance.remarks = request.POST['remarks']
            performance.save()
            id = performance.id
        operation = Operation()
        operation.description = request.POST['desc']
        operation.date = request.POST['date']
        try:
            if id is not None:
                operation.performance = performance
        except:
            pass
        operation.operation = OperationName.objects.get(id=request.POST['key'])
        operation.user = request.user
        if 'sketch' in request.FILES:
            operation.sketch = request.FILES['sketch']
        operation.save()
        print(request.POST['well_id'])
        print(type(request.POST['well_id']))
        selected_well = Well.objects.get(id=request.POST['well_id'])
        selected_well.operations.add(operation)
        # return render(request, 'wells/well_operation.html', {'well': selected_well})
        return HttpResponseRedirect('/operation/{}'.format(request.POST['well_id']))
    else:
        keys = OperationName.objects.all()
        selected_well = Well.objects.get(id=well_id)
        return render(request, 'wells/add_operation.html', {'well': selected_well, 'keys': keys})


@login_required
def add_keys(request):

    if request.method == 'POST':
        if request.POST['key'] != '':
            key = OperationName.objects.create(name=request.POST['key'])
        else:
            pass
        keys = OperationName.objects.all()
        return render(request, 'wells/keys.html', {'keys': keys})

    else:
        keys = OperationName.objects.all()
        return render(request, 'wells/keys.html', {'keys': keys})


@login_required
def show_sketch(request, operation_id, well_id):
    well = Well.objects.get(id=well_id)
    operation = Operation.objects.get(id=operation_id)
    return render(request, 'wells/sketch.html', {'operation': operation, 'well': well})


@login_required
def add_wc(request):
    if request.method == 'POST':
        wells = [key for key in request.POST.keys() if key.startswith('w-')]
        n_values = [key for key in request.POST.keys() if key.startswith('n-')]
        normal_wc = {}
        for e in wells:
            normal_wc[e] = float(request.POST[filter(lambda x: x.endswith(e[-1]), n_values)[0]])
        for key in normal_wc.keys():
            well = Well.objects.get(id=key[-1])
            wc = WaterCut.objects.create(user=request.user, value=request.POST[key], well=well)
            if float(request.POST[key]) != well.normal_value:
                date = well.schedule_id.all()[0].date
                check_date = date[:-1] + str(int(date[-1])+1)
                new_check = Schedule.objects.get_or_create(date=check_date, field=well.field)
                well.check_id.clear()
                well.check_id.add(new_check[0])
                well.need_check = True
            else:
                well.check_id.clear()
                well.need_check = False

        return HttpResponseRedirect('/schedule/')


@login_required
def show_schedule(request, well_id):
    well = Well.objects.get(id=well_id)
    wc_values = WaterCut.objects.filter(well_id=well).all()
    return render(request, 'wells/show_schedule.html', {'wc_values': wc_values, 'well': well})


