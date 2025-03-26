# Post-it Notes

## Overview
Post-it Notes is a simple web-based application for creating, managing, and storing notes. It allows users to save their notes persistently using a local database.

## Features
- Create, edit, and delete notes
- Persistent storage using SQLite (`loginData.db`)
- Simple and intuitive UI
- Built using Flask (Python backend)

## Technologies Used
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript

## Installation & Setup
### Prerequisites
Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Post-it-notes.git
   cd Post-it-notes
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open your browser and visit:
   ```
   http://127.0.0.1:5000
   ```

## Screenshots
### Login Page
![Home Page](public/images/Login.png)

### Create New Note
![Create Note](public/images/CreateNote.png)

### Display Notes
![Display Note](public/images/DisplayNote.png)

## Project Structure
```
Post-it-notes/
│── app.py              # Main Flask application
│── loginData.db        # SQLite database
│── requirements.txt    # Python dependencies
│── templates/          # HTML templates
│── static/             # CSS and JavaScript files
│── .gitignore          # Git ignore file
│── README.md           # Project documentation
```

## Contributing
Feel free to fork this repository and make your own modifications. Contributions are welcome!

## License
This project is licensed under the MIT License.
