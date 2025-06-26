from datetime import date
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from .models import Examallotment
from reportlab.platypus import PageBreak
from io import BytesIO
from reportlab.lib.units import mm
from django.http import HttpResponse
# adminapp/views.py  (or wherever build_attendance_table lives)
import os                       # ← add this line
from io import BytesIO
from django.conf import settings
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Image, Spacer, PageBreak
)
# … the rest of your imports


from adminapp.models import AddexamHall   
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


from datetime import datetime
from typing import List, Optional


from reportlab.platypus import (
    Paragraph, Table, TableStyle, Spacer, PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet
from adminapp.models import AddexamHall, Room 



def hall_for_room(room_no: str) -> AddexamHall | None:
    """
    Return the AddexamHall instance whose rooms_list contains `room_no`.
    Assumes rooms_list is a comma-separated list like "103,104,105".
    """
    return (
        AddexamHall.objects
        .filter(rooms_list__regex=rf'(^|,){room_no}(,|$)')
        .first()
    )


def generate_examallotment_pdf(request):
    # Query data from the Examallotment table
    examallotments = Examallotment.objects.all()

    # Create a buffer to store PDF in memory
    buffer = BytesIO()

    # Create a PDF document with slightly adjusted margins
    pdf = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=72, bottomMargin=72)
    elements = []

    # Iterate through examallotments and group by department
    departments = sorted(set(examallotment.department for examallotment in examallotments))
    for department in departments:
        # Add page break for each department after the first one
        if elements:
            elements.append(PageBreak())

        # Add Aditya Engineering College centered
        logo_path = os.path.join(
            settings.BASE_DIR,              # project root
            'static',                       #  ← adjust if your static dir differs
            'adlogo.png'                     #  ← replace with your file name
            )

        # 2) build an Image flowable (tweak size as you like)
        logo = Image(logo_path, width=350, height=80)  # pick size you like
        logo.hAlign = "CENTER"  # px ≈ points here

        # 3) wrap it in a 1-cell table and center it
        #logo_tbl = Table([[logo]], colWidths=[500])    # same width you use later
        #logo_tbl.hAlign = 'CENTER'

        # 4) add to elements *before* the title
        elements.append(logo)
        elements.append(Spacer(1, 6)) 

        # Add Seating Arrangement heading centered
        elements.append(Paragraph("<b>SEATING ARRANGEMENT</b>", getSampleStyleSheet()['Title']))
        elements.append(Spacer(1, 12))  # Add some space after the heading

        # Collect starttime, endtime, and date from examallotment table for the current department
        department_examallotments = examallotments.filter(department=department)
        starttime = department_examallotments.first().starttime
        #endtime = department_examallotments.first().endtime
        date = department_examallotments.first().date
        venue = "BGB"  # Venue information

        # Add exam timings header before the start time
        # Create a table for Exam Timings and Date on the same line

        # Define style for body text
        body_text_style = getSampleStyleSheet()['BodyText']

        # Create a table for Exam Timings and Date
        exam_timings_and_date = Table([
        ['', '', Paragraph("<b>Date:</b> 21-05-2025 " , body_text_style)]
        ], colWidths=[270, 100, 200])

        exam_timings_and_date.setStyle(TableStyle([
            ('ALIGN', (2, 0), (2, 0), 'RIGHT')  # Align the date cell to the right
        ]))


        # Append the table to the elements list
        elements.append(exam_timings_and_date)



        elements.append(Spacer(1, 6))  # Adjust spacing after the header

        # Add starttime, endtime, date, and venue for the current department
        #start_time = f"<b>Reported time:</b> {starttime}"
        #end_time = f"<b>End Time:</b> {endtime}"
        # exam_date = f"<b>Date:</b> {date}"
        exam_venue = f"<b>Venue:</b> {venue}"
        elements.extend([
            #Paragraph(start_time, getSampleStyleSheet()['BodyText']),
            #Paragraph(end_time, getSampleStyleSheet()['BodyText']),
            #Paragraph(exam_date, getSampleStyleSheet()['BodyText']),
            Paragraph(exam_venue, getSampleStyleSheet()['BodyText']),
            Spacer(1, 18)  # Adjust spacing
        ])

        # Add department heading
        elements.append(Paragraph(f"<b>Department: {department}</b>", getSampleStyleSheet()['Title']))
        elements.append(Spacer(1, 12))  # Add some space after department heading

        # Create a dictionary to hold data for each room
        room_data = {}

        # Filter examallotments for the current department
        department_examallotments = examallotments.filter(department=department)

        # Iterate through examallotments for this department and group by room
        for examallotment in department_examallotments:
            key = examallotment.RoomNo
            if key not in room_data:
                room_data[key] = []
            room_data[key].append(examallotment)

        # Initialize serial number
        serial_no = 1

        # Create a list to hold combined data for all rooms in this department
        combined_data = [['S.No', 'Roll Numbers', 'Room No', 'Total']]

        # Iterate through room data
        for room, room_examallotments in room_data.items():
            # Initialize variables for roll number range and total count for this room
            roll_numbers = []
            total_count = len(room_examallotments)

            # Iterate through examallotments for this room
            for examallotment in room_examallotments:
                roll_numbers.append(examallotment.Student_Id)

            # Append combined data for this room to the list
            combined_data.append([
                serial_no,
                f"{min(roll_numbers)} to {max(roll_numbers)}",
                room,
                total_count
            ])

            # Increment serial number for the next entry
            serial_no += 1

        # Add table with left and right padding for all rooms in this department


        # Define the column widths
        col_widths = [150, 150, 150, 100]  # Adjust the widths as needed

        # Create the table
        table = Table(combined_data, colWidths=col_widths)

        # Define the table style
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),        # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),               # Center alignment for all cells
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),     # Bold font for header row
            ('BOTTOMPADDING', (0, 0), (-1, 0), 18),              # Padding for header row
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),      # Alternate row background color
            ('GRID', (0, 0), (-1, -1), 1, colors.black),         # Gridlines for all cells
            ('LEFTPADDING', (0, 0), (-1, -1), 6),                # Left padding for all cells
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),               # Right padding for all cells
        ])

        # Apply the style to the table
        table.setStyle(style)

        # Add the table to the elements list
        elements.append(table)



        # Add a spacer to increase the gap
        elements.append(Spacer(1, 36))

        # Create a table to place "Exam Cell In Charge" and "Head of the Department" on the same line
        in_charge_and_hod_table = Table([
            [Paragraph("Exam Cell In Charge:", getSampleStyleSheet()['BodyText']), Spacer(1, 1), Paragraph("Head of the Department:", getSampleStyleSheet()['BodyText'])]
        ], colWidths=[200, 100, 200])
        in_charge_and_hod_table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT')]))
        elements.append(in_charge_and_hod_table)

    # Build PDF
    pdf.build(elements)

    # Get PDF content from buffer
    pdf_content = buffer.getvalue()
    buffer.close()

    # Serve the PDF as a download
    response = HttpResponse(pdf_content, content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename=examallotment.pdf'
    return response




def download_room_report(request):
    buffer = BytesIO()
    pdf    = SimpleDocTemplate(buffer, pagesize=letter,
                               leftMargin=36, rightMargin=36,
                               topMargin=72, bottomMargin=72)
    elements = []

    # every distinct room in the allotment table
    for room in (
        Examallotment.objects
        .values_list('RoomNo', flat=True)
        .distinct()
    ):
        room_data = Examallotment.objects.filter(RoomNo=room)
        if not room_data.exists():
            continue

        hall = hall_for_room(room.replace('Room', '').strip())   # <<< key line
        elements.extend(get_room_elements(room, list(room_data), hall))
        elements.append(PageBreak())

    pdf.build(elements)
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')




# ── 2. main routine to build one room-sheet ─────────────────────────
def get_room_elements(room_number: str,
                      room_data: List,
                      hall: AddexamHall | None):
    """
    Build the PDF flowables (elements) for a single room sheet.
    * room_number – plain string, e.g. "103"
    * room_data   – list of Examallotment rows for that room
    * hall        – AddexamHall that owns this room, or None
    """
    styles   = getSampleStyleSheet()
    elements = []

    # ── College title ───────────────────────────────────────────────
    logo_path = os.path.join(
        settings.BASE_DIR,              # project root
        'static',                       #  ← adjust if your static dir differs
        'adlogo.png'                     #  ← replace with your file name
    )

        # 2) build an Image flowable (tweak size as you like)
    logo = Image(logo_path, width=350, height=80)  # pick size you like
    logo.hAlign = "CENTER"  # px ≈ points here

    # 3) wrap it in a 1-cell table and center it
    #logo_tbl = Table([[logo]], colWidths=[500])    # same width you use later
    #logo_tbl.hAlign = 'CENTER'

    # 4) add to elements *before* the title
    elements.append(logo)
    elements.append(Spacer(1, 6)) 

    # ── Header-left : venue & room ──────────────────────────────────
    left_table = Table([
        [Paragraph("<b>Venue:</b> BGB",        styles['BodyText'])],
        [Paragraph(f"<b>Room Number:</b> {room_number}", styles['BodyText'])],
    ], hAlign='LEFT')

    # ── Header-right : date + subjects from hall (if any) ───────────
    if hall:
        exam_date = hall.date.strftime('%d-%m-%Y') if hall.date else '—'
        sub1      = hall.subject1 or '—'
        sub2      = hall.subject2 or '—'
    else:
        exam_date = sub1 = sub2 = '—'

    right_table = Table([
        [Paragraph(f"<b>Date:</b> {exam_date}",         styles['BodyText'])],
        [Paragraph(f"<b>Subject 1:</b> {sub1}",         styles['BodyText'])],
        [Paragraph(f"<b>Subject 2:</b> {sub2}",         styles['BodyText'])],
    ], hAlign='RIGHT')

    header = Table([[left_table, right_table]], colWidths=[400, 150])
    header.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    elements += [header, Spacer(1, 12)]

    # ── Roll-number grid (unchanged) ────────────────────────────────
    elements.append(create_roll_number_grid(room_data))
    elements.append(Spacer(1, 24))

    # ── Bottom summary table (unchanged) ────────────────────────────
    summary = Table(
        [['Year', 'Branch', 'No. Registered', 'Presentees', 'Absentees'],
         ['',     '',       '',               '',           ''],
         ['',     '',       '',               '',           '']],
        colWidths=[100, 100, 120, 100, 100]
    )
    summary.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements += [summary, Spacer(1, 24)]

    
    sig_table = Table(
        [["", "", "__________________________", "__________________________"],
         ["", "", "Invigilator 1 Signature",     "Invigilator 2 Signature"]],
        colWidths=[50, 150, 150, 150]
    )
    sig_table.setStyle(TableStyle([
        ('ALIGN', (2,0), (3,1), 'CENTER'),
        ('LINEABOVE', (2,0), (2,0), 0.8, colors.black),
        ('LINEABOVE', (3,0), (3,0), 0.8, colors.black),
        ('TOPPADDING', (2,0), (3,0), 20),
    ]))
    elements.append(sig_table)

    return elements

    

def infer_students_per_bench(room_data):
    # Count the number of students assigned to each bench
    bench_students_count = {}
    for examallotment in room_data:
        bench_number = examallotment.BenchNo
        if bench_number not in bench_students_count:
            bench_students_count[bench_number] = 0
        bench_students_count[bench_number] += 1
    
    # Determine the most common number of students per bench
    most_common_count = max(bench_students_count.values(), default=0)
    
    # Return the most common count as the inferred students per bench
    return most_common_count



def create_roll_number_grid(room_data):
    # Get roll numbers, ensure they are valid strings
    roll_numbers = sorted([str(r.Student_Id) for r in room_data if r.Student_Id])

    # Define how many columns per row
    columns_per_row = 6

    # Create rows of roll numbers
    grid_data = [roll_numbers[i:i+columns_per_row] for i in range(0, len(roll_numbers), columns_per_row)]

    # Pad the last row if it's incomplete
    if grid_data and len(grid_data[-1]) < columns_per_row:
        grid_data[-1] += [''] * (columns_per_row - len(grid_data[-1]))

    # Define column widths equally across the page
    col_widths = [85] * columns_per_row  # Adjust width as needed

    table = Table(grid_data, colWidths=col_widths, hAlign='CENTER')
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    return table

def generate_attendance_sheet(request, room_no):
    students = Student.objects.filter(room_no=room_no).order_by('roll_no')

    # Divide into two series
    group_23 = [s for s in students if s.roll_no.startswith('23')]
    group_20 = [s for s in students if s.roll_no.startswith('20')]

    # Create response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Attendance_Room_{room_no}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)

    def draw_sheet(title, student_group):
        p.setFont("Helvetica-Bold", 14)
        p.drawString(200, 800, f"Attendance Sheet - Room {room_no} ({title})")

        headers = ["S.No", "Roll No", "Name", "Signature"]
        x_positions = [50, 100, 250, 450]
        y = 770

        # Draw table headers
        p.setFont("Helvetica-Bold", 12)
        for i, header in enumerate(headers):
            p.drawString(x_positions[i], y, header)

        y -= 25
        p.setFont("Helvetica", 11)
        for i, student in enumerate(student_group, start=1):
            if y < 100:  # Create new page if space is over
                p.showPage()
                y = 800
                p.setFont("Helvetica-Bold", 14)
                p.drawString(200, 800, f"Attendance Sheet - Room {room_no} ({title})")
                y -= 30
                p.setFont("Helvetica-Bold", 12)
                for j, header in enumerate(headers):
                    p.drawString(x_positions[j], y, header)
                y -= 25
                p.setFont("Helvetica", 11)

            p.drawString(x_positions[0], y, str(i))
            p.drawString(x_positions[1], y, student.roll_no)
            p.drawString(x_positions[2], y, student.name)
            p.line(x_positions[3], y - 2, x_positions[3] + 100, y - 2)  # Signature line
            y -= 20

    # Draw two sheets
    if group_23:
        draw_sheet("23 Series", group_23)
        p.showPage()

    if group_20:
        draw_sheet("20 Series", group_20)

    p.save()
    return response