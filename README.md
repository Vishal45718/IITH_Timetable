# IITH Timetable Generator

##  Overview

This is a Python-based command-line utility designed to generate a  weekly class schedule for **IIT Hyderabad (IITH)** use. The generator takes your registered course slots, course names, and classrooms as input, and outputs a  HTML file.

The core timetable structure is based on the institution's fixed slot template (1hr and 1.5hr slots):

| Day | 9:00 - 9:55 | 10:00 - 10:55 | 11:00 - 11:55 | 12:00 - 12:55 | 14:30 - 15:55 | 16:00 - 17:25 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Monday** | A | B | C | D | P | Q |
| **Tuesday** | D | E | F | G | R | S |
| **Wednesday** | B | C | A | G | F | Challenge |
| **Thursday** | C | A | B | E | Q | P |
| **Friday** | E | F | D | G | S | R |

---

## Key Features

* **Personalized Content:** The final timetable displays actual **Course Names** and Room Numbers, not just slot letters.
* **Optimized Layout:** The layout is optimized for viewing, with **Days on the Y-axis** and **Time Slots on the X-axis**.
* **Dynamic Highlighting:** The currently active class (based on the viewing device's time) is highlighted with a striking **cyan/blue holographic glow**.
* **Clean Look:** All empty/free slots are blank for maximum visual clarity.

---

##  Getting Started

### Prerequisites

You only need **Python 3** installed on your system. The script uses no external dependencies.

### Installation and Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Vishal45718/IITH_Timetable.git](https://github.com/Vishal45718/IITH_Timetable.git)
    cd IITH_Timetable
    ```
2.  **Run the Script:**
    ```bash
    python3 timetable_maker.py
    ```

### Usage Instructions

The script is interactive and will guide you through the input process:

1.  **Enter Slots:** Input all registered slot letters separated by commas (e.g., `A, B, C, Q, R`).
2.  **Enter Details:** For each registered slot (e.g., 'A'), you will be prompted to enter the **Course Name** and the **Classroom**.

### Output

Upon successful completion, the script will generate a file named:
`professional_dark_timetable.html`

Open this file in any web browser to view your custom schedule.

---

## Visual Example

A screenshot of the generated HTML output is provided below:
<img width="1456" height="647" alt="image" src="https://github.com/user-attachments/assets/679a175b-f678-4dc8-a8fc-e2e16d3ffb4f" />



---

##  Contribution

We encourage contributions from the IITH community to improve this tool!

If you find bugs or have suggestions (e.g., support for Minor/LA slots, conflict detection), please follow these steps:

1.  **Fork** the repository.
2.  Create a new **Feature Branch** (`git checkout -b feature/new-feature`).
3.  Commit your changes (`git commit -m 'feat: added new feature'`).
4.  Push to the branch.
5.  Open a **Pull Request**.

---

##  License

This project is licensed under the **MIT License**.

The MIT License allows anyone to reuse your code for almost any purpose (even commercial) as long as they include a copy of the license and your copyright notice.

**You, as the creator of the code, hold the copyright.**

You should create a separate file named `LICENSE` in the root of your repository with the following content (replace `[year]` with `2025` and `[fullname]` with your name):
