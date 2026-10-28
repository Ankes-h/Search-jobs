"""Multi-format document exporter for AI Job Search (Search-Jobs).

Exports CVs and cover letters across all three supported formats:
  - LaTeX (.tex)
  - Markdown (.md)
  - Microsoft Word (.docx)

Can be used in this workspace or imported into other repositories and workflows.
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    _HAVE_DOCX = True
except ImportError:
    _HAVE_DOCX = False

NAVY = RGBColor(26, 82, 118)       # #1A5276
DARK_GRAY = RGBColor(70, 80, 95)    # #46505F
CHARCOAL = RGBColor(33, 37, 41)     # #212529

def add_heading_with_bottom_border(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(8)
    h.paragraph_format.space_after = Pt(3)
    h.paragraph_format.keep_with_next = True
    for run in h.runs:
        run.font.name = 'Calibri'
        run.font.color.rgb = NAVY
        run.font.size = Pt(13)
        run.bold = True
    
    pPr = h._element.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '1A5276')
    pBdr.append(bottom)
    pPr.append(pBdr)
    return h

def export_example_markdown_cv(dest_path: Path):
    content = """# [First Name] [Last Name]
**[City, Country]** | **Phone:** [Phone Number] | **Email:** [[your.email@example.com](mailto:your.email@example.com)]  
**Profiles:** [LinkedIn](https://linkedin.com) • [GitHub](https://github.com) • [Portfolio/Blog](https://example.com)

---

### Professional Summary
[Tailored 3-5 line elevator pitch connecting your core background, domain expertise, and key technical capabilities directly to the requirements of the target role.]

---

### Core Competencies
- **Primary Technical Domain:** [Skill 1, Skill 2, Framework 1, Framework 2, Tooling]
- **Software Engineering & Languages:** [Python, JavaScript/TypeScript, SQL, C++, Java]
- **Applied AI & Machine Learning:** [Prompt Engineering, LLM Integration, Data Pipelines, Model Evaluation]
- **Developer Tooling & Cloud:** [Git, GitHub Actions, Docker, Linux/Bash, VS Code / Antigravity]
- **Professional & Soft Skills:** [Technical Writing, Cross-Functional Collaboration, Problem Solving]

---

### Education
- **[Degree Name, e.g. B.Tech in Computer Science]** — *[University Name, City]* ([2025 - 2029])  
  [Relevant coursework, academic honors, or expected graduation year.]

- **[Secondary / High School Diploma]** — *[School Name, City]* ([Year - Year])  
  [Academic focus, honors, or key scores.]

---

### Professional Experience & Projects
#### [Project or Role Title] — *[Organization or Open Source]* ([Year - Present])
- [Action-oriented achievement bullet quantifying impact and naming specific technologies used.]
- [Engineered robust architecture or feature, explaining problem solved and outcome achieved.]
- [Collaborated across teams or maintained open-source repositories and comprehensive test suites.]

#### [Previous Role or Major Project] — *[Organization]* ([Year - Year])
- [Accomplishment bullet highlighting problem, action taken, and measurable business or technical results.]
- [Implemented key pipelines or workflows, improving efficiency, accuracy, or delivery speed.]

---

### Certifications
- **[Certification Name 1]** — [Issuing Organization] ([Year])
- **[Certification Name 2]** — [Issuing Organization] ([Year])

---

### Languages
- **[Language 1]:** [Native / Bilingual]
- **[Language 2]:** [Fluent / Professional working proficiency]

---

### References
Available upon request.
"""
    dest_path.write_text(content, encoding="utf-8")
    print(f"Created: {dest_path}")

def export_example_docx_cv(dest_path: Path):
    if not _HAVE_DOCX:
        print(f"Warning: python-docx not available, skipping {dest_path}")
        return
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.6)
        section.left_margin = Inches(0.7)
        section.right_margin = Inches(0.7)

    # Title
    p_name = doc.add_paragraph()
    p_name.paragraph_format.space_before = Pt(0)
    p_name.paragraph_format.space_after = Pt(2)
    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_name = p_name.add_run("[First Name] [Last Name]")
    r_name.font.name = 'Calibri'
    r_name.font.size = Pt(22)
    r_name.bold = True
    r_name.font.color.rgb = NAVY

    # Contact line
    p_contact = doc.add_paragraph()
    p_contact.paragraph_format.space_before = Pt(0)
    p_contact.paragraph_format.space_after = Pt(6)
    p_contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact_text = "[City, Country]  |  [Phone Number]  |  [your.email@example.com]\nLinkedIn: [LinkedIn URL]  |  GitHub: [GitHub URL]"
    r_contact = p_contact.add_run(contact_text)
    r_contact.font.name = 'Calibri'
    r_contact.font.size = Pt(9.5)
    r_contact.font.color.rgb = DARK_GRAY

    # Summary
    add_heading_with_bottom_border(doc, "PROFESSIONAL SUMMARY")
    p_sum = doc.add_paragraph()
    p_sum.paragraph_format.space_before = Pt(2)
    p_sum.paragraph_format.space_after = Pt(4)
    p_sum.paragraph_format.line_spacing = 1.15
    r_sum = p_sum.add_run("[Tailored 3-5 line elevator pitch connecting your core background, domain expertise, and key technical capabilities directly to the requirements of the target role.]")
    r_sum.font.name = 'Calibri'
    r_sum.font.size = Pt(10)
    r_sum.font.color.rgb = CHARCOAL

    # Core Competencies
    add_heading_with_bottom_border(doc, "CORE COMPETENCIES")
    competencies = [
        ("Primary Technical Domain", "[Skill 1, Skill 2, Framework 1, Framework 2, Tooling]"),
        ("Software Engineering & Languages", "[Python, JavaScript/TypeScript, SQL, C++, Java]"),
        ("Applied AI & Machine Learning", "[Prompt Engineering, LLM Integration, Data Pipelines, Model Evaluation]"),
        ("Developer Tooling & Cloud", "[Git, GitHub Actions, Docker, Linux/Bash, VS Code / Antigravity]"),
        ("Professional & Soft Skills", "[Technical Writing, Cross-Functional Collaboration, Problem Solving]")
    ]
    for category, details in competencies:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        r_c = p.add_run(category + ": ")
        r_c.font.name = 'Calibri'
        r_c.font.size = Pt(9.5)
        r_c.bold = True
        r_c.font.color.rgb = CHARCOAL
        r_d = p.add_run(details)
        r_d.font.name = 'Calibri'
        r_d.font.size = Pt(9.5)
        r_d.font.color.rgb = CHARCOAL

    # Education
    add_heading_with_bottom_border(doc, "EDUCATION")
    p_ed = doc.add_paragraph()
    p_ed.paragraph_format.space_before = Pt(2)
    p_ed.paragraph_format.space_after = Pt(2)
    r_deg = p_ed.add_run("[Degree Name, e.g. B.Tech in Computer Science]")
    r_deg.font.name = 'Calibri'
    r_deg.font.size = Pt(10)
    r_deg.bold = True
    r_deg.font.color.rgb = CHARCOAL
    r_inst = p_ed.add_run("  —  [University Name, City] ([2025 - 2029])\n")
    r_inst.font.name = 'Calibri'
    r_inst.font.size = Pt(9.5)
    r_inst.italic = True
    r_inst.font.color.rgb = DARK_GRAY
    r_notes = p_ed.add_run("[Relevant coursework, academic honors, or expected graduation year.]")
    r_notes.font.name = 'Calibri'
    r_notes.font.size = Pt(9)
    r_notes.font.color.rgb = CHARCOAL

    # Experience
    add_heading_with_bottom_border(doc, "PROJECTS & EXPERIENCE")
    p_proj = doc.add_paragraph()
    p_proj.paragraph_format.space_before = Pt(3)
    p_proj.paragraph_format.space_after = Pt(1)
    r_pt = p_proj.add_run("[Project or Role Title]")
    r_pt.font.name = 'Calibri'
    r_pt.font.size = Pt(10)
    r_pt.bold = True
    r_pt.font.color.rgb = CHARCOAL
    r_po = p_proj.add_run("  |  [Organization or Open Source]  ([Year - Present])")
    r_po.font.name = 'Calibri'
    r_po.font.size = Pt(9.5)
    r_po.italic = True
    r_po.font.color.rgb = DARK_GRAY

    for b in [
        "[Action-oriented achievement bullet quantifying impact and naming specific technologies used.]",
        "[Engineered robust architecture or feature, explaining problem solved and outcome achieved.]",
        "[Collaborated across teams or maintained open-source repositories and comprehensive test suites.]"
    ]:
        p_b = doc.add_paragraph(style='List Bullet')
        p_b.paragraph_format.space_before = Pt(1)
        p_b.paragraph_format.space_after = Pt(2)
        r_b = p_b.add_run(b)
        r_b.font.name = 'Calibri'
        r_b.font.size = Pt(9.5)
        r_b.font.color.rgb = CHARCOAL

    # Certifications & Languages
    add_heading_with_bottom_border(doc, "CERTIFICATIONS & LANGUAGES")
    p_cl = doc.add_paragraph()
    p_cl.paragraph_format.space_before = Pt(2)
    p_cl.paragraph_format.space_after = Pt(2)
    r_c1 = p_cl.add_run("Certifications: ")
    r_c1.bold = True
    r_c1.font.name = 'Calibri'
    r_c1.font.size = Pt(9.5)
    r_c2 = p_cl.add_run("[Certification 1], [Certification 2]\n")
    r_c2.font.name = 'Calibri'
    r_c2.font.size = Pt(9.5)
    r_l1 = p_cl.add_run("Languages: ")
    r_l1.bold = True
    r_l1.font.name = 'Calibri'
    r_l1.font.size = Pt(9.5)
    r_l2 = p_cl.add_run("[Language 1 (Native)], [Language 2 (Fluent)]")
    r_l2.font.name = 'Calibri'
    r_l2.font.size = Pt(9.5)

    doc.save(dest_path)
    print(f"Created: {dest_path}")

def export_example_markdown_cover_letter(dest_path: Path):
    content = """# [First Name] [Last Name]
[your.email@example.com] | [Phone Number] | [LinkedIn URL] | [GitHub URL]  
[City, Country]

---

**Date:** [Date, e.g. October 27, 2026]  
**Application for:** [Target Role Title]  
**Company:** [Target Company Name]  

---

Dear Hiring Team at [Target Company Name],

I am writing to express my strong enthusiasm for the [Target Role Title] position at [Target Company Name]. As a [Candidate Domain / Background / Degree status], I bring hands-on experience in [Core Capability 1], [Core Capability 2], and [Core Capability 3].

[Target Company Name]'s work in [Company mission / specialized engineering focus] strongly aligns with my technical focus. Key highlights from my recent background that directly map to your team's objectives include:

- **[Key Competency 1 / Architectural Experience]:** [Concrete evidence or project highlight with measurable results and technical depth.]
- **[Key Competency 2 / Technical Rigor]:** [Specific achievement, framework integration, or engineering pipeline developed.]
- **[Key Competency 3 / Fast Learning & Ownership]:** [Demonstrated track record of independent contribution, research, or cross-platform tool development.]

I am excited by the prospect of joining [Target Company Name] and contributing directly to your team's upcoming initiatives. I bring high curiosity, rapid execution, and a commitment to writing clean, maintainable, and verified code.

Thank you for your time and consideration. I would welcome the opportunity to discuss how my qualifications align with your requirements.

Kind regards,  
**[First Name] [Last Name]**
"""
    dest_path.write_text(content, encoding="utf-8")
    print(f"Created: {dest_path}")

def export_example_docx_cover_letter(dest_path: Path):
    if not _HAVE_DOCX:
        print(f"Warning: python-docx not available, skipping {dest_path}")
        return
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Name Header
    p_name = doc.add_paragraph()
    p_name.paragraph_format.space_before = Pt(0)
    p_name.paragraph_format.space_after = Pt(2)
    r_name = p_name.add_run("[First Name] [Last Name]")
    r_name.font.name = 'Calibri'
    r_name.font.size = Pt(20)
    r_name.bold = True
    r_name.font.color.rgb = NAVY

    # Contact line
    p_contact = doc.add_paragraph()
    p_contact.paragraph_format.space_before = Pt(0)
    p_contact.paragraph_format.space_after = Pt(12)
    r_contact = p_contact.add_run("[your.email@example.com]  |  [Phone Number]  |  [LinkedIn URL]\n[City, Country]")
    r_contact.font.name = 'Calibri'
    r_contact.font.size = Pt(9.5)
    r_contact.font.color.rgb = DARK_GRAY

    # Border separator
    pPr = p_contact._element.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '4')
    bottom.set(qn('w:color'), '1A5276')
    pBdr.append(bottom)
    pPr.append(pBdr)

    # Metadata block
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(6)
    p_meta.paragraph_format.space_after = Pt(10)
    r_meta = p_meta.add_run("Date: [Current Date]\nTo: Hiring Team at [Target Company Name]\nRole: [Target Role Title]")
    r_meta.font.name = 'Calibri'
    r_meta.font.size = Pt(10)
    r_meta.bold = True
    r_meta.font.color.rgb = CHARCOAL

    # Salutation
    p_sal = doc.add_paragraph()
    p_sal.paragraph_format.space_before = Pt(4)
    p_sal.paragraph_format.space_after = Pt(6)
    r_sal = p_sal.add_run("Dear Hiring Team at [Target Company Name],")
    r_sal.font.name = 'Calibri'
    r_sal.font.size = Pt(11)
    r_sal.bold = True
    r_sal.font.color.rgb = CHARCOAL

    # Opening
    p_op = doc.add_paragraph()
    p_op.paragraph_format.space_before = Pt(2)
    p_op.paragraph_format.space_after = Pt(6)
    p_op.paragraph_format.line_spacing = 1.15
    r_op = p_op.add_run("I am writing to express my strong enthusiasm for the [Target Role Title] position at [Target Company Name]. As a [Candidate Domain / Background / Degree status], I bring hands-on experience in [Core Capability 1], [Core Capability 2], and [Core Capability 3].")
    r_op.font.name = 'Calibri'
    r_op.font.size = Pt(10.5)
    r_op.font.color.rgb = CHARCOAL

    # Body
    p_why = doc.add_paragraph()
    p_why.paragraph_format.space_before = Pt(2)
    p_why.paragraph_format.space_after = Pt(6)
    p_why.paragraph_format.line_spacing = 1.15
    r_why = p_why.add_run("[Target Company Name]'s work in [Company mission / specialized engineering focus] strongly aligns with my technical focus. Key highlights from my recent background that directly map to your team's objectives include:")
    r_why.font.name = 'Calibri'
    r_why.font.size = Pt(10.5)
    r_why.font.color.rgb = CHARCOAL

    # Bullets
    bullets = [
        ("[Key Competency 1 / Architectural Experience]", "[Concrete evidence or project highlight with measurable results and technical depth.]"),
        ("[Key Competency 2 / Technical Rigor]", "[Specific achievement, framework integration, or engineering pipeline developed.]"),
        ("[Key Competency 3 / Fast Learning & Ownership]", "[Demonstrated track record of independent contribution, research, or cross-platform tool development.]")
    ]
    for b_title, b_desc in bullets:
        p_b = doc.add_paragraph(style='List Bullet')
        p_b.paragraph_format.space_before = Pt(2)
        p_b.paragraph_format.space_after = Pt(3)
        p_b.paragraph_format.line_spacing = 1.15
        r_bt = p_b.add_run(b_title + ": ")
        r_bt.font.name = 'Calibri'
        r_bt.font.size = Pt(10)
        r_bt.bold = True
        r_bt.font.color.rgb = NAVY
        r_bd = p_b.add_run(b_desc)
        r_bd.font.name = 'Calibri'
        r_bd.font.size = Pt(10)
        r_bd.font.color.rgb = CHARCOAL

    # Closing
    p_cl = doc.add_paragraph()
    p_cl.paragraph_format.space_before = Pt(4)
    p_cl.paragraph_format.space_after = Pt(6)
    p_cl.paragraph_format.line_spacing = 1.15
    r_cl = p_cl.add_run("I am excited by the prospect of joining [Target Company Name] and contributing directly to your team's upcoming initiatives. I bring high curiosity, rapid execution, and a commitment to writing clean, maintainable, and verified code.\n\nThank you for your time and consideration. I would welcome the opportunity to discuss how my qualifications align with your requirements.")
    r_cl.font.name = 'Calibri'
    r_cl.font.size = Pt(10.5)
    r_cl.font.color.rgb = CHARCOAL

    # Sign-off
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(10)
    p_sign.paragraph_format.space_after = Pt(2)
    r_so = p_sign.add_run("Kind regards,\n\n")
    r_so.font.name = 'Calibri'
    r_so.font.size = Pt(10.5)
    r_so.font.color.rgb = CHARCOAL

    r_nm = p_sign.add_run("[First Name] [Last Name]")
    r_nm.font.name = 'Calibri'
    r_nm.font.size = Pt(11)
    r_nm.bold = True
    r_nm.font.color.rgb = NAVY

    doc.save(dest_path)
    print(f"Created: {dest_path}")

def main():
    parser = argparse.ArgumentParser(description="Multi-format document exporter for AI Job Search.")
    parser.add_argument("--examples", action="store_true", help="Generate stock example templates in .md and .docx")
    parser.add_argument("--repo-root", default=".", help="Path to repo root")
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    cv_dir = repo / "cv"
    cl_dir = repo / "cover_letters"
    cv_dir.mkdir(parents=True, exist_ok=True)
    cl_dir.mkdir(parents=True, exist_ok=True)

    if args.examples or len(sys.argv) == 1:
        export_example_markdown_cv(cv_dir / "main_example.md")
        export_example_docx_cv(cv_dir / "main_example.docx")
        export_example_markdown_cover_letter(cl_dir / "cover_example.md")
        export_example_docx_cover_letter(cl_dir / "cover_example.docx")

if __name__ == "__main__":
    main()
