"""Searchable PDF exporter"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def export_searchable_pdf(text: str, job_id: str) -> str:
    """Export text to searchable PDF"""
    output_file = os.path.join(OUTPUT_DIR, f"{job_id}.pdf")
    
    # Create PDF
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Add content
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor='black'
    )
    
    story.append(Paragraph('OCR Extracted Text', title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Add extracted text
    for paragraph in text.split('\n'):
        if paragraph.strip():
            story.append(Paragraph(paragraph, styles['Normal']))
        else:
            story.append(Spacer(1, 0.1*inch))
    
    doc.build(story)
    
    return output_file


class SearchablePDFExporter:
    """Legacy class - use export_searchable_pdf function instead"""
    
    @staticmethod
    def export(text: str, filename: str, output_dir: str = "outputs") -> str:
        """Export text to searchable PDF"""
        return export_searchable_pdf(text, filename)
