from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from django.http import HttpResponse
from io import BytesIO
import datetime

def generate_quote_pdf(quote):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Header
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=20,
        spaceAfter=30,
        alignment=1  # Center
    )
    
    story.append(Paragraph("NORTE GESTIÓN", title_style))
    story.append(Paragraph("Presupuesto", styles['Heading1']))
    story.append(Spacer(1, 12))
    
    # Quote info
    quote_info = [
        ['Número:', quote.numero],
        ['Fecha:', quote.fecha.strftime('%d/%m/%Y')],
        ['Vencimiento:', quote.fecha_vencimiento.strftime('%d/%m/%Y')],
        ['Cliente:', quote.cliente.nombre],
    ]
    
    if quote.cliente.telefono:
        quote_info.append(['Teléfono:', quote.cliente.telefono])
    if quote.cliente.email:
        quote_info.append(['Email:', quote.cliente.email])
    
    quote_table = Table(quote_info, colWidths=[2*inch, 4*inch])
    quote_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(quote_table)
    story.append(Spacer(1, 20))
    
    # Items table
    items_data = [['Descripción', 'Cantidad', 'Precio Unit.', 'Subtotal', 'IVA', 'Total']]
    
    for item in quote.items.all():
        items_data.append([
            item.descripcion,
            f"{item.cantidad:,.2f}",
            f"${item.precio_unitario:,.2f}",
            f"${item.subtotal:,.2f}",
            f"${item.iva_monto:,.2f}",
            f"${item.total:,.2f}"
        ])
    
    # Totals
    items_data.append(['', '', '', '', '', ''])  # Empty row
    items_data.append(['', '', '', 'SUBTOTAL:', f"${quote.subtotal:,.2f}", ''])
    items_data.append(['', '', '', 'IVA:', f"${quote.iva_total:,.2f}", ''])
    items_data.append(['', '', '', 'TOTAL:', '', f"${quote.total:,.2f}"])
    
    items_table = Table(items_data, colWidths=[3*inch, 0.8*inch, 1*inch, 1*inch, 1*inch, 1*inch])
    
    items_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),  # Description left aligned
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        
        # Data rows
        ('GRID', (0, 0), (-1, -4), 1, colors.black),
        
        # Totals section
        ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
        ('ALIGN', (3, -3), (3, -1), 'RIGHT'),
        ('ALIGN', (4, -3), (-1, -1), 'RIGHT'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
    ]))
    
    story.append(items_table)
    story.append(Spacer(1, 20))
    
    # Observations
    if quote.observaciones:
        story.append(Paragraph("<b>Observaciones:</b>", styles['Normal']))
        story.append(Paragraph(quote.observaciones, styles['Normal']))
        story.append(Spacer(1, 12))
    
    # Footer
    footer_text = f"Presupuesto válido hasta el {quote.fecha_vencimiento.strftime('%d/%m/%Y')}"
    story.append(Paragraph(footer_text, styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def create_pdf_response(quote):
    pdf_buffer = generate_quote_pdf(quote)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="presupuesto_{quote.numero}.pdf"'
    response.write(pdf_buffer.getvalue())
    pdf_buffer.close()
    
    return response