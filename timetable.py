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
    h1 { color: #bb86fc; text-align: center; margin-bottom: 40px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; }

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
</head>
<body>
    <h1>TIMETABLE</h1>
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
