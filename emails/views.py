import datetime
from rest_framework.views import APIView
from rest_framework.response import Response

from emails.models import Email
from django.contrib.auth.models import User


from emails.serializers import EmailSerializer
# Create your views here.
class GetEmailsByReceiverAddress(APIView):
    def get(self, request, receiver_address):
        emails = Email.objects.filter(receiver_address=receiver_address)
        serializer = EmailSerializer(emails, many=True)
        return Response(serializer.data)
    
class GetEmailById(APIView):
    def get(self, request, pk):
        email = Email.objects.get(pk=pk)
        serializer = EmailSerializer(email)
        return Response(serializer.data)
    
class ChangeEmailStatusToRead(APIView):
    def put(self, request, pk):
        email = Email.objects.filter(pk=pk)[0]
        email.unread = 1
        email.save()
        return Response(request.data)

class CheckValidAddress(APIView):
    def get(self, request, receiver_address):
        if User.objects.filter(email = receiver_address).exists():
            return Response({'status': 200, 'message': 'Email Address Valid'})
        return Response({'status': 400, 'message': 'Email Address Not Found'})

class WriteEmailToOthers(APIView):
    def post(self, request, format=None):
        # Process Data from request
        topic = request.data['topic']
        receiver_address = request.data['receiver_address']
        sender_address = request.data['sender_address']
        text = request.data['text']
        attachment = request.data['attachment']
        
        if attachment == '' or attachment == None or attachment == 'undefined':
            attachment = None
        
        date_sent = datetime.datetime.now()
        reply = request.data['reply']
        if reply == '' or reply == None or reply == 'undefined':
            reply = None
        
        unread = 0
        
        serializer = EmailSerializer(data={
            'name': topic,
            'receiver_address': receiver_address,
            'sender_address': sender_address,
            'text': text,
            'attatchment': attachment,
            'date_sent': date_sent,
            'reply': reply,
            'unread': unread,
        })
        
        if serializer.is_valid():
            serializer.save()
            return Response({'email': serializer.data, 'status': 200})
        return Response({'errors': serializer.errors, 'status': 400})
    
class GetSentEmailsBySenderAddress(APIView):
    def get(self, request, sender_address):
        emails = Email.objects.filter(sender_address=sender_address)
        serializer = EmailSerializer(emails, many=True)
        return Response(serializer.data)