import time

TIMETABLE_SLOTS = {
    'Monday':    ['A', 'B', 'C', 'D', 'P', 'Q'],
    'Tuesday':   ['D', 'E', 'F', 'G', 'R', 'S'],
    'Wednesday': ['B', 'C', 'A', 'G', 'F', 'Challenge Lectures'],
    'Thursday':  ['C', 'A', 'B', 'E', 'Q', 'P'],
    'Friday':    ['E', 'F', 'D', 'G', 'S', 'R']
}

TIME_SLOTS = [
    '9:00 - 9:55 (1hr)',
    '10:00 - 10:55 (1hr)',
    '11:00 - 11:55 (1hr)',
    '12:00 - 12:55 (1hr)',
    '14:30 - 15:55 (1.5hr)',
    '16:00 - 17:25 (1.5hr)'
]

TIME_RANGES = [
    (900, 955), (1000, 1055), (1100, 1155), (1200, 1255),
    (1430, 1555), (1600, 1725)
]

# For Dark Theme
SLOT_COLORS_DARK = {
    'A': '#4e7ac7',  # Deep Blue
    'B': '#3c937c',  # Teal Green
    'C': '#a366ff',  # Rich Purple
    'D': '#e87d3a',  # Burnt Orange
    'E': '#c74e7a',  # Raspberry Red
    'F': '#4ec7c7',  # Cyan
    'G': '#e8c74e',  # Gold Yellow
    'P': '#7a4ec7',  # Violet
    'Q': '#4ec77a',  # Emerald
    'R': '#c77a4e',  # Copper
    'S': '#4e7ac7',  # Deep Blue (reused for completeness)
}

# HTML AND CSS TEMPLATE FOR DARK THEME
CSS_STYLE_DARK = """
<style>
    /* 1. Overall Theme & Body */
    body { font-family: 'Roboto', 'Arial', sans-serif; background-color: #121212; padding: 30px; color: #e0e0e0; }
    h1 { color: #f05a28; text-align: center; margin-bottom: 40px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; }

    /* 2. Container and Table Structure */
    .timetable-container { max-width: 1400px; margin: 0 auto; box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5); border-radius: 8px; overflow: hidden; border: 1px solid #333; }
    table { width: 100%; border-collapse: separate; border-spacing: 0; background-color: #1e1e1e; }

    /* 3. Cells (TH and TD) */
    th, td { padding: 18px 12px; text-align: center; border-bottom: 1px solid #333; border-right: 1px solid #333; font-size: 0.95em; }

    /* Header Row (Time Slots) */
    th { background-color: #333; color: #ffffff; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #555; }
    th:first-child { border-top-left-radius: 8px; }
    th:last-child { border-top-right-radius: 8px; border-right: none; }

    /* Day Column */
    td:first-child { background-color: #2c2c2c; font-weight: 700; color: #f0f0f0; text-align: left; padding-left: 25px; border-right: 2px solid #555; }

    /* 4. Class Slot Styles */
    .slot-content { border-radius: 4px; padding: 8px 10px; font-weight: 600; font-size: 1.05em; transition: transform 0.2s; cursor: default; }
    .slot-content:hover { transform: scale(1.05); box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4); }

    /* Course Name */
    .course-name { display: block; font-weight: 700; margin-bottom: 3px; color: #f0f0f0; }

    /* Room Info */
    .slot-info { font-size: 0.8em; font-weight: 400; color: #cccccc; display: block; }

    /* Empty / Optional */
    .challenge-slot { background-color: #3a3a3a; color: #ffb74d; font-weight: 500; border: 1px dashed #555; }
    .empty-slot { background-color: #1e1e1e; }

    /* 5. Highlight Current Slot */
    .current-slot {
        box-shadow: 0 0 15px 5px rgba(0, 255, 255, 0.7) !important;
        border: 3px solid #00ffff !important;
        animation: pulse 1.5s infinite alternate;
    }
    @keyframes pulse { from { opacity: 1; } to { opacity: 0.85; } }

    /* 6. Footer */
    .footer { text-align: center; margin-top: 40px; color: #666; font-size: 0.8em; }

    /* Print styles for export */
    @media print {
        .no-print { display: none !important; }
        body { background-color: #ffffff !important; color: #000000 !important; padding: 0 !important; }
        h1 { color: #0b2545 !important; margin-bottom: 20px !important; }
        .timetable-container { box-shadow: none !important; border: 1px solid #000000 !important; max-width: 100% !important; }
        table { background-color: #ffffff !important; }
        th { background-color: #f1f5f9 !important; color: #0b2545 !important; border-bottom: 2px solid #000000 !important; border-right: 1px solid #cccccc !important; }
        td { border-bottom: 1px solid #cccccc !important; border-right: 1px solid #cccccc !important; }
        td:first-child { background-color: #e2e8f0 !important; color: #0b2545 !important; border-right: 2px solid #000000 !important; }
        .slot-content { background-color: #f8fafc !important; border: 1px solid #000000 !important; color: #000000 !important; transform: none !important; box-shadow: none !important; }
        .course-name { color: #000000 !important; }
        .slot-info { color: #333333 !important; }
        .challenge-slot { background-color: #f8fafc !important; color: #000000 !important; border: 1px dashed #000000 !important; }
        .empty-slot { background-color: #ffffff !important; }
        .footer { color: #555555 !important; margin-top: 20px !important; }
    }
</style>
"""

# HTML GENERATION FUNCTION
def generate_timetable_html(slots, user_data, slots_color_map):

    html_output = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Professional Dark Timetable</title>
    {CSS_STYLE_DARK}
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
</head>
<body>
    <h1>TIMETABLE</h1>
    <div style="display: flex; justify-content: center; gap: 15px; margin-bottom: 30px; flex-wrap: wrap;" class="no-print">
        <!-- Back button -->
        <a href="/" style="display: inline-flex; align-items: center; justify-content: center; text-decoration: none; color: #e2e8f0; border: 1.5px solid #444; background: #1c1c1c; padding: 10px 20px; border-radius: 8px; font-weight: 600; font-size: 0.9em; transition: all 0.25s ease; gap: 8px;" onmouseover="this.style.borderColor='#f05a28'; this.style.color='#f05a28';" onmouseout="this.style.borderColor='#444'; this.style.color='#e2e8f0';">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
            Back to Planner
        </a>
        
        <!-- Export PDF button -->
        <button onclick="window.print()" style="display: inline-flex; align-items: center; justify-content: center; background: #f05a28; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: 600; font-size: 0.9em; cursor: pointer; transition: all 0.25s ease; gap: 8px;" onmouseover="this.style.backgroundColor='#d4481b';" onmouseout="this.style.backgroundColor='#f05a28';">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9V2h12v7"></path><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
            Print / Save PDF
        </button>
        
        <!-- Export HTML button -->
        <button onclick="downloadHTML()" style="display: inline-flex; align-items: center; justify-content: center; background: #1c1c1c; color: #e2e8f0; border: 1.5px solid #444; padding: 10px 20px; border-radius: 8px; font-weight: 600; font-size: 0.9em; cursor: pointer; transition: all 0.25s ease; gap: 8px;" onmouseover="this.style.borderColor='#f05a28'; this.style.color='#f05a28';" onmouseout="this.style.borderColor='#444'; this.style.color='#e2e8f0';">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
            Download HTML
        </button>
        
        <!-- Save as Image button -->
        <button onclick="downloadPNG()" style="display: inline-flex; align-items: center; justify-content: center; background: #1c1c1c; color: #e2e8f0; border: 1.5px solid #444; padding: 10px 20px; border-radius: 8px; font-weight: 600; font-size: 0.9em; cursor: pointer; transition: all 0.25s ease; gap: 8px;" onmouseover="this.style.borderColor='#f05a28'; this.style.color='#f05a28';" onmouseout="this.style.borderColor='#444'; this.style.color='#e2e8f0';">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
            Save as Image (PNG)
        </button>
    </div>
    <div class="timetable-container">
    <table>
        <thead>
            <tr>
                <th>Day / Time</th>
                {''.join(f'<th>{ts}</th>' for ts in TIME_SLOTS)}
            </tr>
        </thead>
        <tbody>
    """

    days_of_week = list(slots.keys())
    current_day = time.strftime('%A')
    current_hour_minute = int(time.strftime('%H%M'))

    for day in days_of_week:
        html_output += f"<tr>"
        html_output += f"<td>{day}</td>"

        for i, (start_time, end_time) in enumerate(TIME_RANGES):
            slot_name = slots[day][i]

            cell_content = ""
            cell_class = ""

            if slot_name in user_data:
                data = user_data[slot_name]
                color = slots_color_map.get(slot_name, '#555')

                border_color = color.replace('#', '#') if color != '#555' else '#777'

                cell_content = f"""
                    <div class="slot-content" style="background-color: {color}; border: 1px solid {border_color};">
                        <span class="course-name">{data['name']}</span>
                        <span class="slot-info">Room: {data['room']}</span>
                    </div>
                """

                if day == current_day and start_time <= current_hour_minute <= end_time:
                    cell_class = "current-slot"

            elif slot_name == 'Challenge Lectures':
                cell_content = f"""
                    <div class="challenge-slot">
                        Optional Lectures<span class="slot-info">1.5 hr Enrichment</span>
                    </div>
                """
            else:
                cell_class = "empty-slot"

            html_output += f"<td class='{cell_class}'>{cell_content}</td>"

        html_output += "</tr>"

    html_output += f"""
        </tbody>
    </table>
    </div>
    <div class="footer">Generated on {time.strftime('%Y-%m-%d at %H:%M:%S')}. | Empowered by your institutional Timetable Generator.</div>
    <script>
        function downloadHTML() {{
            const clone = document.documentElement.cloneNode(true);
            const buttons = clone.querySelector('.no-print');
            if (buttons) buttons.remove();
            const scriptTag = clone.querySelector('script');
            if (scriptTag) scriptTag.remove();
            
            const htmlContent = '<!DOCTYPE html>\\n' + clone.outerHTML;
            const blob = new Blob([htmlContent], {{ type: 'text/html' }});
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'iith_timetable.html';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }}

        function downloadPNG() {{
            const element = document.querySelector('.timetable-container');
            if (typeof html2canvas === 'undefined') {{
                alert('Export library is still loading, please try again in a second!');
                return;
            }}
            html2canvas(element, {{
                backgroundColor: '#121212',
                scale: 3, // Premium high-resolution vector scaling!
                useCORS: true,
                logging: false
            }}).then(canvas => {{
                const link = document.createElement('a');
                link.href = canvas.toDataURL('image/png');
                link.download = 'iith_timetable.png';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }});
        }}
    </script>
</body>
</html>
    """

    return html_output


# Input for course names & classrooms
def get_user_course_data():
    print("\n=============================================")
    print("                 TIMETABLE                   ")
    print("=============================================")
    print("Welcome! Let's personalize your schedule with Course Names.")

    course_input = input("Enter all your registered Course Slots (A-G, P-S), separated by commas (e.g., A, C, Q, B): ")
    user_slots = [slot.strip().upper() for slot in course_input.split(',') if slot.strip()]

    if not user_slots:
        print("\n!!Error: No slots entered. Exiting.")
        return None, None

    print(f"\nRegistered Slots Detected: {user_slots}")

    user_course_data = {}

    print("\nPlease enter the Course Name and Classroom for each of your registered slots:")

    for slot in user_slots:
        course_name = input(f"Enter the **Course Name** for slot **{slot}**: ").strip()
        room = input(f"Enter the **Classroom** for slot **{slot}**: ").strip()

        user_course_data[slot] = {
            'name': course_name if course_name else f"Course {slot}",
            'room': room if room else "TBD"
        }

    return user_slots, user_course_data


def generate_timetable(slot, course, room):
    user_data = {}
    if slot:
        # Support comma-separated slots (e.g. A, B, C) or a single slot
        slots_list = [s.strip().upper() for s in slot.split(',') if s.strip()]
        for s in slots_list:
            user_data[s] = {
                'name': course.strip() if course.strip() else f"Course {s}",
                'room': room.strip() if room else "TBD"
            }
    return generate_timetable_html(TIMETABLE_SLOTS, user_data, SLOT_COLORS_DARK)


def generate_timetable_from_lists(slots_list, courses_list, rooms_list):
    user_data = {}
    for slot, course, room in zip(slots_list, courses_list, rooms_list):
        if not slot:
            continue
        # Split by comma in case they entered multiple slots for a single course row
        sub_slots = [s.strip().upper() for s in slot.split(',') if s.strip()]
        for s in sub_slots:
            user_data[s] = {
                'name': course.strip() if course.strip() else f"Course {s}",
                'room': room.strip() if room else "TBD"
            }
    return generate_timetable_html(TIMETABLE_SLOTS, user_data, SLOT_COLORS_DARK)


if __name__ == "__main__":

    user_slots, user_data = get_user_course_data()

    if user_data:
        html_content = generate_timetable_html(TIMETABLE_SLOTS, user_data, SLOT_COLORS_DARK)

        file_name = "professional_dark_timetable.html"
        try:
            with open(file_name, 'w') as f:
                f.write(html_content)

            print("Timetable Generated!")
            print(f"File saved as: **{file_name}**")
            print("Open this HTML file to view your new darker, personalized schedule.")

        except Exception as e:
            print(f"\n!! Error saving file: {e}")
