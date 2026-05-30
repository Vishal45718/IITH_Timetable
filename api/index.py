import sys
import os
# Add root path to sys.path so we can import IITH_timetable correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, render_template_string
from IITH_timetable import generate_timetable_from_lists

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IITH Timetable Generator</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            background-color: #121212;
            color: #d1d5db;
            font-family: 'Outfit', sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            width: 100%;
            max-width: 480px;
            background: #1c1c1c;
            border-top: 5px solid #d32f2f;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
            padding: 40px;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            border-left: 1px solid #2a2a2a;
            border-right: 1px solid #2a2a2a;
            border-bottom: 1px solid #2a2a2a;
            text-align: center;
        }
        
        .logo-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-bottom: 25px;
            gap: 15px;
        }
        
        .logo-text-group {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
        }
        .logo-text-hindi {
            color: #799bec;
            font-weight: 700;
            font-size: 1.1rem;
            letter-spacing: 0.2px;
        }
        .logo-text-english {
            color: #799bec;
            font-weight: 700;
            font-size: 0.95rem;
            letter-spacing: 0.2px;
        }
        
        h1 {
            font-size: 1.5rem;
            font-weight: 800;
            color: #e2e8f0;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
            text-transform: uppercase;
        }
        .subtitle {
            color: #cbd5e1;
            font-size: 0.85rem;
            margin-bottom: 35px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            line-height: 1.4;
        }
        
        /* Wizard Steps */
        .step {
            display: none;
        }
        .step.active {
            display: block;
            animation: fadeIn 0.4s ease-out forwards;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .form-group {
            margin-bottom: 22px;
            position: relative;
            text-align: left;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #cbd5e1;
            font-weight: 700;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        input {
            width: 100%;
            padding: 12px 14px;
            background: #151515;
            border: 1.5px solid #2d2d2d;
            border-radius: 8px;
            color: #e2e8f0;
            font-family: inherit;
            font-size: 0.95rem;
            transition: all 0.25s ease;
        }
        input:focus {
            outline: none;
            border-color: #d32f2f;
            box-shadow: 0 0 0 3px rgba(211, 47, 47, 0.15);
        }
        input::placeholder {
            color: #666666;
        }
        
        /* Number selector custom design */
        .number-selector-wrapper {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin: 25px 0;
        }
        .num-btn {
            width: 46px;
            height: 46px;
            border-radius: 8px;
            background: #151515;
            border: 1.5px solid #2d2d2d;
            color: #ffffff;
            font-size: 1.3rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            transition: all 0.2s;
        }
        .num-btn:hover {
            border-color: #d32f2f;
            color: #d32f2f;
            background: rgba(211, 47, 47, 0.05);
        }
        #course_count {
            width: 60px;
            text-align: center;
            font-size: 1.6rem;
            font-weight: 800;
            color: #ffffff;
            padding: 5px;
            background: transparent;
            border: none;
        }
        
        /* Course Rows */
        .course-row {
            background: #151515;
            border: 1px solid #2d2d2d;
            border-left: 4px solid #d32f2f;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            position: relative;
            text-align: left;
        }
        .course-row-title {
            font-size: 0.9rem;
            font-weight: 800;
            color: #e0a92d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .remove-row-btn {
            background: none;
            border: none;
            color: #f43f5e;
            font-size: 0.75rem;
            font-weight: bold;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .remove-row-btn:hover {
            text-decoration: underline;
        }
        .input-grid {
            display: grid;
            grid-template-columns: 1fr 2fr 1fr;
            gap: 15px;
        }
        @media (max-width: 600px) {
            .input-grid {
                grid-template-columns: 1fr;
            }
        }
        
        .tip {
            font-size: 0.8rem;
            color: #777777;
            margin-top: 6px;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        /* Action buttons */
        .btn-container {
            display: flex;
            gap: 15px;
            margin-top: 25px;
        }
        button.primary-btn {
            width: 100%;
            padding: 14px;
            background: #d32f2f;
            border: none;
            border-radius: 8px;
            color: #ffffff;
            font-weight: 700;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            cursor: pointer;
            transition: all 0.25s ease;
            box-shadow: 0 4px 12px rgba(211, 47, 47, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        button.primary-btn:hover {
            background: #b71c1c;
            box-shadow: 0 6px 16px rgba(211, 47, 47, 0.3);
            transform: translateY(-1px);
        }
        button.primary-btn:active {
            transform: translateY(0);
        }
        button.secondary-btn {
            padding: 14px 22px;
            background: transparent;
            border: 1.5px solid #2d2d2d;
            color: #9ca3af;
            border-radius: 8px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 0.5px;
        }
        button.secondary-btn:hover {
            border-color: #ffffff;
            color: #ffffff;
            background: #151515;
        }
        
        .add-course-trigger {
            width: 100%;
            background: transparent;
            border: 1.5px dashed #2d2d2d;
            color: #888888;
            padding: 12px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 700;
            font-size: 0.85rem;
            margin-bottom: 20px;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }
        .add-course-trigger:hover {
            border-color: #d32f2f;
            color: #ffffff;
            background: rgba(211, 47, 47, 0.02);
        }
        
        .footer {
            margin-top: 30px;
            text-align: center;
            font-size: 0.75rem;
            color: #777777;
            border-top: 1px solid #2d2d2d;
            padding-top: 15px;
        }
    </style>
</head>
<body>

<div class="container" id="generator-card">
    <div class="logo-container">
        <!-- SVG recreation of official logo: orange circle and book shape -->
        <svg width="120" height="120" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="15" r="9" fill="#d32f2f" />
            <!-- Left Side Pages -->
            <polygon points="48 31, 35 24, 35 76, 48 83" fill="#d32f2f"/>
            <polygon points="33 24, 29 24, 29 74, 33 75" fill="#e64a19"/>
            <polygon points="27 24, 23 24, 23 72, 27 73" fill="#f57c00"/>
            <polygon points="21 24, 17 24, 17 70, 21 71" fill="#ffa726"/>
            <polygon points="15 24, 11 24, 11 68, 15 69" fill="#fbc02d"/>
            <!-- Right Side Pages -->
            <polygon points="52 31, 65 24, 65 76, 52 83" fill="#d32f2f"/>
            <polygon points="67 24, 71 24, 71 74, 67 75" fill="#e64a19"/>
            <polygon points="73 24, 77 24, 77 72, 73 73" fill="#f57c00"/>
            <polygon points="79 24, 83 24, 83 70, 79 71" fill="#ffa726"/>
            <polygon points="85 24, 89 24, 89 68, 85 69" fill="#fbc02d"/>
        </svg>
        <div class="logo-text-group">
            <span class="logo-text-hindi">भारतीय प्रौद्योगिकी संस्थान हैदराबाद</span>
            <span class="logo-text-english">Indian Institute of Technology Hyderabad</span>
        </div>
    </div>
    
    <h1>Timetable Planner</h1>
    <div class="subtitle">Inventing and Innovating in Technology for Humanity</div>
    
    <!-- STEP 1: Ask for course count -->
    <div class="step active" id="step1">
        <div style="margin-bottom: 20px;">
            <label style="font-size: 1.05rem; color: #e2e8f0; text-align: center;">How many courses do you want to register?</label>
        </div>
        <div class="number-selector-wrapper">
            <button type="button" class="num-btn" onclick="adjustCount(-1)">-</button>
            <input type="number" id="course_count" value="3" min="1" max="15" readonly>
            <button type="button" class="num-btn" onclick="adjustCount(1)">+</button>
        </div>
        <button type="button" class="primary-btn" style="margin-top: 20px;" onclick="goToStep2()">
            Continue
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
        </button>
    </div>
    
    <!-- STEP 2: Entry fields -->
    <div class="step" id="step2">
        <form method="POST" id="timetable-form">
            <div id="course-rows-container">
                <!-- Will be dynamically generated -->
            </div>
            
            <button type="button" class="add-course-trigger" onclick="addNewCourseRow()">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                Add Another Course
            </button>
            
            <div class="btn-container">
                <button type="button" class="secondary-btn" onclick="goToStep1()">Back</button>
                <button type="submit" class="primary-btn">Generate Timetable</button>
            </div>
        </form>
    </div>
    
    <div class="footer">
        IIT Hyderabad Timetable Planner
    </div>
</div>

<script>
    function adjustCount(change) {
        const input = document.getElementById('course_count');
        let val = parseInt(input.value) + change;
        if (val >= 1 && val <= 15) {
            input.value = val;
        }
    }
    
    function goToStep1() {
        document.getElementById('step2').classList.remove('active');
        document.getElementById('step1').classList.add('active');
        document.getElementById('generator-card').style.maxWidth = '480px';
    }
    
    function goToStep2() {
        const count = parseInt(document.getElementById('course_count').value);
        generateRows(count);
        
        document.getElementById('step1').classList.remove('active');
        document.getElementById('step2').classList.add('active');
        document.getElementById('generator-card').style.maxWidth = '750px';
    }
    
    function generateRows(count) {
        const container = document.getElementById('course-rows-container');
        container.innerHTML = '';
        
        for (let i = 1; i <= count; i++) {
            createRowMarkup(i);
        }
    }
    
    function createRowMarkup(index) {
        const container = document.getElementById('course-rows-container');
        const row = document.createElement('div');
        row.className = 'course-row';
        row.id = `course-row-${index}`;
        
        row.innerHTML = `
            <div class="course-row-title">
                <span>Course Entry #${index}</span>
                ${index > 1 ? `<button type="button" class="remove-row-btn" onclick="removeCourseRow(${index})">Remove</button>` : ''}
            </div>
            <div class="input-grid">
                <div class="form-group" style="margin-bottom:0">
                    <label>Slot(s)</label>
                    <input type="text" name="slots[]" placeholder="e.g. A, B" required>
                </div>
                <div class="form-group" style="margin-bottom:0">
                    <label>Course Name</label>
                    <input type="text" name="courses[]" placeholder="e.g. Software Eng" required>
                </div>
                <div class="form-group" style="margin-bottom:0">
                    <label>Classroom</label>
                    <input type="text" name="rooms[]" placeholder="e.g. CS-LH-1" required>
                </div>
            </div>
        `;
        container.appendChild(row);
    }
    
    function addNewCourseRow() {
        const container = document.getElementById('course-rows-container');
        const currentRowsCount = container.getElementsByClassName('course-row').length;
        const newIndex = currentRowsCount + 1;
        createRowMarkup(newIndex);
        
        // Auto scroll to new row smoothly
        const newRow = document.getElementById(`course-row-${newIndex}`);
        newRow.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    
    function removeCourseRow(index) {
        const row = document.getElementById(`course-row-${index}`);
        if (row) {
            row.remove();
            // Re-index remaining rows for semantic correctness
            const container = document.getElementById('course-rows-container');
            const rows = container.getElementsByClassName('course-row');
            for (let i = 0; i < rows.length; i++) {
                const currentIdx = i + 1;
                const currentRow = rows[i];
                currentRow.id = `course-row-${currentIdx}`;
                const titleSpan = currentRow.querySelector('.course-row-title span');
                titleSpan.textContent = `Course Entry #${currentIdx}`;
                
                const removeBtn = currentRow.querySelector('.remove-row-btn');
                if (currentIdx === 1 && removeBtn) {
                    removeBtn.remove();
                } else if (currentIdx > 1 && !removeBtn) {
                    const titleDiv = currentRow.querySelector('.course-row-title');
                    titleDiv.insertAdjacentHTML('beforeend', `<button type="button" class="remove-row-btn" onclick="removeCourseRow(${currentIdx})">Remove</button>`);
                } else if (removeBtn) {
                    removeBtn.setAttribute('onclick', `removeCourseRow(${currentIdx})`);
                }
            }
        }
    }
</script>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        slots = request.form.getlist("slots[]")
        courses = request.form.getlist("courses[]")
        rooms = request.form.getlist("rooms[]")

        return generate_timetable_from_lists(
            slots,
            courses,
            rooms
        )

    return render_template_string(HTML, generated=False)

if __name__ == "__main__":
    app.run(debug=True)