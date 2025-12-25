"""Searchable PDF exporter"""
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch


class SearchablePDFExporter:
    """Export OCR results as searchable PDF"""
    
    @staticmethod
    def export(text: str, filename: str, output_dir: str = "outputs") -> str:
        """Export text to searchable PDF"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename
        base_name = os.path.splitext(filename)[0]
        output_file = os.path.join(output_dir, f"{base_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        
        # Create PDF
        doc = SimpleDocTemplate(output_file, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Add content
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='black'
        )
        story.append(Paragraph('OCR Extracted Text', title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Add text
        story.append(Paragraph(f"<b>Source:</b> {filename}", styles['Normal']))
        story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Add extracted text
        for paragraph in text.split('\n'):
            if paragraph.strip():
                story.append(Paragraph(paragraph, styles['Normal']))
        
        doc.build(story)
        
        return output_file
