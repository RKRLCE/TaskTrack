# TaskTrack

TaskTrack is an assignment tracker app made for students. It helps organize tasks, manage deadlines, track progress, save notes, and keep school work in one place.

## Requirements

Before running the app, make sure you have the following installed on your computer:

- Python 3
- pip (usually included with Python)
- Flask

You can check if Python is installed by running:

    python --version

or on macOS/Linux:

    python3 --version

If Python is not installed, download it from the official website:

https://www.python.org/downloads/

## Project Files

Make sure these files and folders stay in the same project folder:

- `app.py`
- `Templates/`
- `static/`

Example structure:

    TaskTrack/
    ├── app.py
    ├── Templates/
    │   └── index.html
    ├── static/
    │   └── logo.png
    ├── settings.json
    └── tasktrack_data.json

## How to Run TaskTrack

Follow the instructions below based on your operating system.

### For macOS / Linux

1. Open Terminal and go to the project folder.

   Example:

       cd TaskTrack

2. Create a virtual environment named `fl_venv`.

       python3 -m venv fl_venv

3. Activate the virtual environment.

       . fl_venv/bin/activate

4. Install Flask.

       pip install flask

5. Run the app.

       python app.py

   If that does not work, try:

       python3 app.py

6. Open your browser and go to:

       http://127.0.0.1:5000

7. To stop the app, press:

       Ctrl + C

### For Windows

1. Open Command Prompt or PowerShell and go to the project folder.

   Example:

       cd TaskTrack

2. Create a virtual environment named `fl_venv`.

       python -m venv fl_venv

3. Activate the virtual environment.

   For Command Prompt:

       fl_venv\Scripts\activate

   For PowerShell:

       .\fl_venv\Scripts\Activate.ps1

4. Install Flask.

       pip install flask

5. Run the app.

       python app.py

6. Open your browser and go to:

       http://127.0.0.1:5000

7. To stop the app, press:

       Ctrl + C

## Notes

- Make sure `Templates` and `static` stay in the same folder as `app.py`.
- If the virtual environment is already created, you do not need to create it again. You only need to activate it.
- If Flask is already installed inside the virtual environment, you do not need to install it again.
- If `python` does not work on your computer, try using `python3`.

## Credits

- Rayen Leigh C. Elecho
- Jerriel Aljamz L. Salih
