
# Agile Dashboard

A modular, modern Streamlit application for managing ideas and innovations with user authentication, responsive design, and role-based navigation.

## 🎯 Features

- **User Authentication** - Secure login system with session management
- **Responsive Dashboard** - Wide-mode layout optimized for all screen sizes
- **Modular Architecture** - Cleanly separated pages and components for easy maintenance
- **Custom Styling** - Professional CSS for headers, forms, buttons, and UI elements
- **Role-Based Navigation** - Dynamic navigation tabs (Home, Ideas, My Ideas)
- **User Management** - Quick logout and settings functionality


## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher (3.11)
- pip (Python package manager)

### Installation

1. **Clone the repository:**
git clone https://github.com/Stayuptildawn/Agile-dashboard.git
cd Agile-dashboard



2. **Create a virtual environment:**
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate



3. **Install dependencies:**
pip install streamlit pandas streamlit-aggrid



4. **Run the application:**
streamlit run streamlit_app.py



The app will open in your browser at `http://localhost:8501`

## 🔐 Default Credentials

- **Username:** admin
- **Password:** aA1234

> ⚠️ **Important:** Change these credentials in `data/users.csv` for production use

## 📖 Usage

### Login Page
- Enter your credentials to access the dashboard
- Check "Remember me" to stay logged in
- Click "Sign in with SSO" for alternative authentication (coming soon)

### Dashboard
- **Navigation Bar** - Switch between Home, Ideas, and My Ideas sections
- **User Menu** - Located in the top-right corner
  - Click your profile icon to see user info
  - Use Settings for account configuration
  - Click Logout to exit the application

### Pages
- **Home** - Main dashboard overview
- **Ideas** - Browse and explore submitted ideas
- **My Ideas** - View and manage your own ideas

## 🎨 Customization

### Colors & Theme
Edit `.streamlit/config.toml`



### Styles
Modify CSS in `styles/` directory:
- `main.py` - Global styles for all pages
- `login.py` - Login page specific styles
- `dashboard.py` - Dashboard specific styles
- `header.py` - Header and navigation styles

### Users
Edit `data/users.csv` to add/modify user credentials:
username,password
admin,aA1234
user1,password123



## 🔧 Architecture

The application follows a modular architecture:

1. **streamlit_app.py** - Main router that handles authentication and page routing
2. **pages/** - Individual page modules that manage their own content
3. **styles/** - Centralized CSS management for consistent styling
4. **data/** - User database and application data

## 🛠️ Technologies Used

- **Streamlit** - Web application framework
- **Pandas** - Data manipulation and CSV handling
- **Python 3.8+** - Core language
- **HTML/CSS** - Styling and layout

## 📞 Support

For support, open an issue on GitHub or contact the development team.


## 📄 License

This project is licensed under the MIT License.

---

**Built with ❤️ using Streamlit**

## 📁 Project Structure

```
Agile-dashboard/
├── .streamlit/
│   └── config.toml
├── styles/
│   ├── __init__.py
│   ├── main.py
│   ├── login.py
│   ├── dashboard.py
│   └── header.py
├── pages/
│   ├── __init__.py
│   ├── login.py
│   ├── dashboard.py
│   └── header.py
├── elements/
│   ├── upm_logo.png
│   ├── Right Side.png
│   ├── Headline.png
│   ├── Email Form.png
│   ├── Password Form.png
│   ├── Sign in Button.png
│   ├── Sign in Button Google.png
│   └── SignupforFree.png
├── data/
│   └── users.csv
├── streamlit_app.py
├── README.md
└── .gitignore
```
