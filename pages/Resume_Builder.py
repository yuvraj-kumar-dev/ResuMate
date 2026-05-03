import streamlit as st
from reportlab.pdfgen import canvas
from io import BytesIO

# Helper function to wrap text
def draw_paragraph(c, text, x, y, max_width, font_size=12, line_height=16):
    c.setFont("Helvetica", font_size)
    words = text.split()
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        if c.stringWidth(test_line, "Helvetica", font_size) <= max_width:
            line = test_line
        else:
            c.drawString(x, y, line)
            y -= line_height
            line = word
    if line:
        c.drawString(x, y, line)
        y -= line_height
    return y

def generate_pdf(data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    y = 800
    margin_x = 50
    content_width = 500

    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(300, y, data["name"])
    y -= 25
    c.setFont("Helvetica", 12)
    c.drawCentredString(300, y, f"{data['address']} | {data['contact']}")
    y -= 20
    c.line(margin_x, y, margin_x + content_width, y)
    y -= 30

    # Objective
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin_x, y, "Objective")
    y -= 20
    y = draw_paragraph(c, data["objective"], margin_x, y, content_width)
    y -= 10

    # Education
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin_x, y, "Education")
    y -= 20
    c.setFont("Helvetica", 12)
    for edu in data["education"].split("\n"):
        y = draw_paragraph(c, edu.strip(), margin_x, y, content_width)
    y -= 10

    # Experience
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin_x, y, "Experience")
    y -= 20
    c.setFont("Helvetica", 12)
    for exp in data["experience"].split("\n"):
        y = draw_paragraph(c, exp.strip(), margin_x, y, content_width)
    y -= 10

    # Projects
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin_x, y, "Projects")
    y -= 20
    c.setFont("Helvetica", 12)
    for proj in data["projects"].split("\n"):
        y = draw_paragraph(c, proj.strip(), margin_x, y, content_width)
    y -= 10

    # Skills
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin_x, y, "Skills")
    y -= 20
    c.setFont("Helvetica", 12)
    y = draw_paragraph(c, data["skills"], margin_x, y, content_width)

    c.save()
    buffer.seek(0)
    return buffer

##################################################################################

st.title("📄 Resume Generator")

with st.form("resume_form"):
    name = st.text_input("Full Name")
    address = st.text_input("Address")
    contact = st.text_input("Contact Info")
    objective = st.text_area("Career Objective")
    education = st.text_area("Education (Use new line for each degree)")
    experience = st.text_area("Experience (Use new line for each point)")
    projects = st.text_area("Projects (Use new line for each project)")
    skills = st.text_area("Skills (comma-separated)")

    submitted = st.form_submit_button("Generate Resume")

if submitted:
    resume_data = {
        "name": name,
        "address": address,
        "contact": contact,
        "objective": objective,
        "education": education,
        "experience": experience,
        "projects": projects,
        "skills": skills,
    }

    pdf_file = generate_pdf(resume_data)
    st.success("🎉 Resume generated successfully!")

    st.download_button(
        label="📥 Download Resume PDF",
        data=pdf_file,
        file_name="resume.pdf",
        mime="application/pdf"
    )
