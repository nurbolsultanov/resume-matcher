from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
import io

SECTION_HEADERS = [
    'PROFESSIONAL SUMMARY', 'TECHNICAL SKILLS', 'EXPERIENCE',
    'PROJECTS', 'EDUCATION', 'SKILLS', 'CERTIFICATIONS',
    'PORTFOLIO PROJECTS', 'PROFESSIONAL EXPERIENCE'
]


def build_story(text, body_s, bullet_s, name_s, section_s, sp_bullet, sp_body, sp_section):
    name_style = ParagraphStyle('Name', fontSize=name_s, fontName='Helvetica-Bold',
                                 alignment=TA_CENTER, spaceAfter=3)
    contact_style = ParagraphStyle('Contact', fontSize=body_s - 0.5, fontName='Helvetica',
                                    alignment=TA_CENTER, spaceAfter=6)
    section_style = ParagraphStyle('Section', fontSize=section_s, fontName='Helvetica-Bold',
                                    spaceBefore=sp_section, spaceAfter=2,
                                    textColor=colors.HexColor('#1a1a1a'))
    body_style = ParagraphStyle('Body', fontSize=body_s, fontName='Helvetica',
                                 spaceAfter=sp_body, leading=body_s * 1.35)
    bullet_style = ParagraphStyle('Bullet', fontSize=bullet_s, fontName='Helvetica',
                                   spaceAfter=sp_bullet, leftIndent=10, leading=bullet_s * 1.35)

    story = []
    lines = text.split('\n')
    is_first = True
    is_second = False

    for line in lines:
        s = line.strip()
        if not s:
            story.append(Spacer(1, 2))
            continue
        if is_first:
            story.append(Paragraph(s, name_style))
            is_first = False
            is_second = True
            continue
        if is_second:
            story.append(Paragraph(s, contact_style))
            story.append(HRFlowable(width="100%", thickness=0.5,
                                     color=colors.HexColor('#1a1a1a'), spaceAfter=3))
            is_second = False
            continue
        if any(s.upper() == h for h in SECTION_HEADERS):
            story.append(Paragraph(s.upper(), section_style))
            story.append(HRFlowable(width="100%", thickness=0.3,
                                     color=colors.HexColor('#cccccc'), spaceAfter=2))
            continue
        if s.startswith('- '):
            story.append(Paragraph(f"• {s[2:]}", bullet_style))
            continue
        story.append(Paragraph(s, body_style))

    return story


def render_pdf(story, margin):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                             rightMargin=margin, leftMargin=margin,
                             topMargin=margin, bottomMargin=margin)
    page_counts = []

    def on_page(canvas, doc):
        page_counts.append(1)

    doc.build(story, onLaterPages=on_page, onFirstPage=on_page)
    return buffer.getvalue(), len(page_counts)


def generate_pdf_from_text(text: str) -> bytes:
    margin = 0.6 * inch

    configs = [
        (14, 9.5, 9.0, 10.5, 1.5, 2.0, 7.0),
        (13, 9.0, 8.5, 10.0, 1.2, 1.8, 6.0),
        (12, 8.5, 8.0, 9.5, 1.0, 1.5, 5.0),
        (11, 8.0, 7.5, 9.0, 0.8, 1.2, 4.0),
        (10, 7.5, 7.0, 8.5, 0.5, 1.0, 3.5),
        (10, 7.0, 6.5, 8.0, 0.3, 0.8, 3.0),
    ]

    for name_s, body_s, bullet_s, section_s, sp_bullet, sp_body, sp_section in configs:
        story = build_story(text, body_s, bullet_s, name_s, section_s,
                            sp_bullet, sp_body, sp_section)
        pdf_bytes, pages = render_pdf(story, margin)
        if pages <= 1:
            return pdf_bytes

    # fallback
    story = build_story(text, 7.0, 6.5, 10.0, 8.0, 0.2, 0.5, 2.5)
    pdf_bytes, _ = render_pdf(story, margin)
    return pdf_bytes