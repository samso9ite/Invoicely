import pdfkit

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from rest_framework import viewsets, serializers
from rest_framework import status, authentication, permissions
from rest_framework import response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from django.shortcuts import render
from .serializers import InvoiceSerializer, ItemSerializer
from django.core.exceptions import PermissionDenied
from .models import *

# Create your views here.

class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        team = self.request.user.teams.first()
        invoice_number = team.first_invoice_number 
        team.first_invoice_number = invoice_number + 1
        team.save()

        serializer.save(created_by=self.request.user, team=team, modified_by=self.request.user, invoice_number=invoice_number, bank_account=team.bank_account)

    def perform_update(self, serializer):
        obj = self.get_object()
        if self.request.user != obj.created_by:
            raise PermissionDenied("Wrong Owner")
        serializer.save()

@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def generate_pdf(request, invoice_id):
    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    invoice = get_object_or_404(Invoice, pk=invoice_id, created_by=request.user)
    team = Team.objects.filter(created_by=request.user).first()
    template_name = 'pdf.html'
    if invoice.is_credit_for:
        template_name = 'pdf_creditnote.html'
    template = get_template(template_name)
    html = template.render({'invoice':invoice, 'team':team})
    pdf = pdfkit.from_string(html, False, options={}, configuration=config)
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response

@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def send_reminder(request, invoice_id):
    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    invoice = get_object_or_404(Invoice, pk=invoice_id, created_by=request.user)
    team = Team.objects.filter(created_by=request.user).first()

    subject = 'Unpaid Invoice'
    from_email = team.email
    to = [invoice.client.email]
    text_content = 'You have an unpaid invoice. Invoice number: #' + str(invoice.invoice_number)
    html_content = 'You have an unpaid invoice. Invoice number: #' + str(invoice.invoice_number)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html") 

    template = get_template('pdf.html')
    html = template.render({'invoice': invoice, 'team': team})
    pdf = pdfkit.from_string(html, False, options={}, configuration=config)
    
    if pdf:
        name = 'invoice_%s.pdf' % invoice.invoice_number
        msg.attach(name, pdf, 'application/pdf')

    msg.send()
    return Response()



# class ItemViewSet(viewsets.ModelViewSet):
#     serializer_class = ItemSerializer
#     queryset = Item.objects.all()

#     def get_queryset(self):
#         invoice_id = self.request.GET.get('invoice_id', 0)
#         return self.queryset.filter(invoice__id=invoice_id)