
# Agile Dashboard

A modular, modern Streamlit application for managing ideas and innovations with user authentication, responsive design, and role-based navigation.

## 🎯 Features

- **User Authentication** - Secure login system with rate limiting and session management
- **CSV Data Persistence** - All ideas stored in persistent CSV files
- **Idea Management** - Create, edit, delete, and publish ideas
- **User-Specific Views** - Filter ideas by owner in "My Ideas"
- **Advanced Filtering** - Search by name, description, category, date range, and status
- **Interactive Tables** - AgGrid-powered tables with sorting, pagination, and selection
- **Responsive Dashboard** - Wide-mode layout optimized for all screen sizes
- **Modular Architecture** - Clean separation of concerns with script-based page routing
- **Custom Styling** - Professional CSS for headers, forms, buttons, and UI elements
- **Role-Based Navigation** - Dynamic navigation with st.page_link()

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher (3.11 recommended)
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
- Rate limiting: Max 5 failed attempts per 15 minutes
- "Remember me" feature for persistent sessions
- SSO option available for alternative authentication

### Ideas (Dashboard)
- Browse all submitted ideas from all users
- Filter by:
  - **Search** - Name or description keywords
  - **Date Range** - From and To dates
  - **Category** - TRANSPORT, HEALTH, ENERGY, AI, etc.
- Select ideas with checkboxes
- **Actions:**
  - 🔎 Open - View idea details
  - ✏️ Edit - Modify selected idea
  - 🗑 Delete - Remove selected idea

### My Ideas
- View only ideas you've created
- Filter by search term or status (On Review, Accepted, Rejected)
- **Actions:**
  - ✏️ Edit - Modify your idea
  - 📤 Publish - Change status to Accepted
  - 🗑 Delete - Remove your idea

### New Idea
- Submit new ideas with:
  - Title (required)
  - Category (required)
  - Short description (required, max 200 chars)
  - Detailed description (required)
  - Estimated impact / target audience (required)
  - Visibility setting (Public/Private)
- **Save as Draft** - Save without all fields filled
- **Publish** - Submit complete idea (requires terms acceptance)

### Edit Idea
- Modify existing ideas
- All changes saved to CSV
- Redirect back to My Ideas after saving


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

The application follows a modern script-based architecture:

1. **streamlit_app.py** - Main entry point, loads data from CSV and routes based on authentication
2. **pages/** - Individual page modules (dashboard, myideas, publish_idea, edit_idea, login)
3. **pages/header.py** - Shared navigation header with st.page_link()
4. **styles/** - Centralized CSS management for consistent styling
5. **data/** - CSV storage for ideas, users, and login attempts
6. **generate_initial_data.py** - Script to populate initial idea data

## 🛠️ Technologies Used

- **Streamlit 1.29+** - Web application framework
- **Pandas** - Data manipulation and CSV handling
- **streamlit-aggrid** - Interactive data tables with selection
- **Python 3.8+** - Core language
- **HTML/CSS** - Custom styling and layout

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
│ └── config.toml # Streamlit configuration
├── styles/
│ ├── init.py
│ ├── main.py # Global CSS
│ ├── login.py # Login page styles
│ ├── dashboard.py # Dashboard styles
│ ├── header.py # Navigation styles
│ ├── edit_idea.py # Form styles
│ ├── myIdeas.py # My Ideas page styles
│ └── home.py # Home page styles
├── pages/
│ ├── init.py
│ ├── login.py # Authentication page
│ ├── dashboard.py # Ideas listing (all users)
│ ├── myideas.py # User's ideas only
│ ├── publish_idea.py # Create new idea
│ ├── edit_idea.py # Edit existing idea
│ ├── header.py # Shared navigation header
│ ├── experiments.py # Experiments page (placeholder)
│ ├── sprints.py # Sprints page (placeholder)
│ ├── team.py # Team page (placeholder)
│ ├── reports.py # Reports page (placeholder)
│ ├── profile.py # Profile page (placeholder)
│ └── messages.py # Messages page (placeholder)
├── elements/
│ ├── upm_logo.png # University logo
│ ├── Right Side.png # Login page illustration
│ ├── loginRateLimit.png # Rate limit popup
│ └── loginAccDeleted.png # Account deleted popup
├── data/
│ ├── users.csv # User credentials
│ ├── ideas.csv # All ideas (generated + user-created)
│ └── login_attempts.csv # Failed login tracking
├── streamlit_app.py # Main application entry point
├── generate_initial_data.py # Initial data generation script
├── README.md
└── .gitignore
```
