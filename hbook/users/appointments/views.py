from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from hbook.users.models import User2Serializer
from hbook.users.appointments.models import AppointmentRegister, Appointment, AppointmentSerializer, AppointmentRegisterSerializer
from rest_framework.decorators import action

class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def create(self, request):
        from datetime import datetime, timedelta
        x=request.POST._mutable
        request.POST._mutable=True
        request.POST['creator']=User2Serializer(request.user.details, context={'request': request}).data['url']
        request.POST['time_begin']=datetime.now()
        request.POST['time_end']=datetime.now()+timedelta(hours=16)
        request.POST._mutable=x
        return super(AppointmentViewSet, self).create(request)

    @action(detail=False)
    def search(self, request):
        n = request.GET.get("key", 'a')
        self.queryset = Appointment.objects.filter(name__contains=n)
        return super(AppointmentViewSet, self).list(request)

class AppointmentRegisterViewSet(ModelViewSet):
    queryset = AppointmentRegister.objects.all()
    serializer_class = AppointmentRegisterSerializer

    def create(self, request):
        from datetime import datetime, timedelta
        x=request.POST._mutable
        request.POST._mutable=True
        request.POST['registered_user']=User2Serializer(request.user.details, context={'request': request}).data['url']
        
        a=request.POST.get("appointment", "#")
        if a=="#":
            return Response({"error":"appointment is needed"})
        else:
            a=a.split("/")[-2:-1][0]
            n = len(AppointmentRegister.objects.filter(appointment = a))
            request.POST['approx_time']=datetime.now()+n*timedelta(minutes=10)
            request.POST['line_index']=n
            request.POST._mutable=x
            return super(AppointmentRegisterViewSet, self).create(request)
    
    @action(detail=True, methods=['POST'])
    def complete(self, request, pk):
        from datetime import datetime, timedelta
        time_spent = request.POST.get("time_spent")
        time_paused = request.POST.get("time_paused")
        # print(time_spent, time_paused)
        this = AppointmentRegister.objects.get(pk=pk)
        this.status=3
        this.time_utilized=time_spent
        this.details = time_paused
        this.save()

        objs = AppointmentRegister.objects.filter(appointment=this.appointment).order_by('line_index')
        completed = objs.filter(status=3)

        val=0
        # take avg of all times
        for curr in completed:
            val += curr.time_utilized
        
        val /= len(completed)

        ncompleted = objs.filter(status=0)
        for curr in ncompleted:
            curr.approx_time = datetime.now() + timedelta(seconds=val)
            curr.save()
        
        this.approx_time = datetime.now()
        this.save()

        

        return Response({"status":"AAl ej veelll"})
