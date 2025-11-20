
# Agile Dashboard

A modular, modern Streamlit application for managing ideas and innovations with user authentication, responsive design, and role-based navigation.

## 🎯 Features

### Public Access
- **📊 Statistics Dashboard** - View innovation metrics without login
- **🔍 Browse Public Ideas** - Explore published ideas with advanced filtering
- **📈 Category Analytics** - See idea distribution across categories
- **🕒 Recent Activity** - Track the latest submissions

### Authenticated Users
- **✏️ Full CRUD Operations** - Create, read, update, and delete ideas
- **👤 Personal Workspace** - Manage your own ideas in "My Ideas"
- **📤 Publish Control** - Draft, review, and publish ideas
- **🔐 User Authentication** - Secure login with rate limiting
- **💾 CSV Persistence** - All changes saved automatically

### Technical Features
- **Wide-mode responsive layout**
- **Interactive AgGrid tables** with sorting and pagination
- **Real-time data synchronization** across pages
- **Public/private visibility settings**
- **Flash notifications** for user actions
- **Modern UI** with custom CSS styling

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

## 📖 Usage Guide

### 🏠 Home Page
- **Public Access**: View statistics and public ideas without login
- **Statistics Cards**: Total ideas, acceptance rate, review status, categories
- **Category Distribution**: Visual breakdown with percentages
- **Recent Activity**: 5 most recent published ideas
- **Filters**: Search by name/description, date range, category

### 💡 Ideas Page
- Browse all submitted ideas (authenticated users only)
- Advanced filtering and sorting
- Edit and delete functionality
- Select ideas with checkboxes

### 📝 My Ideas Page
- View only your submitted ideas
- Filter by status (On Review, Accepted, Rejected)
- Edit drafts before publishing
- Publish or delete your ideas
- Track submission history

### ➕ New Idea Page
- **Required Fields**:
- Title
- Category
- Short Description (max 200 chars)
- Detailed Description
- Estimated Impact / Target Audience
- **Actions**:
- Save as Draft (partial completion allowed)
- Publish (requires all fields + terms acceptance)
- **Visibility**: Public or Private

### ✏️ Edit Idea Page
- Modify existing ideas
- Auto-saves to CSV
- Returns to "My Ideas" after saving


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
├── streamlit_app.py # Main entry point & routing
├── generate_initial_data.py # Initial data population script
├── README.md # This file
├── requirements.txt # Python dependencies
├── .gitignore # Git ignore rules
│
├── pages/ # Application pages
│ ├── login.py # Authentication page
│ ├── home.py # Landing page with statistics
│ ├── dashboard.py # Ideas management (all ideas)
│ ├── myideas.py # User's personal ideas
│ ├── publish_idea.py # Create new idea form
│ ├── edit_idea.py # Edit existing idea
│ ├── header.py # Shared navigation header
│ └── [other pages] # Additional features
│
├── styles/ # CSS styling modules
│ ├── init.py
│ ├── main.py # Global styles
│ ├── login.py # Login page styles
│ ├── dashboard.py # Dashboard styles
│ ├── header.py # Navigation styles
│ ├── edit_idea.py # Form styles
│ └── home.py # Home page styles
│
├── data/ # Data storage (CSV files)
│ ├── ideas.csv # All ideas database
│ ├── users.csv # User credentials
│ └── login_attempts.csv # Failed login tracking
│
└── elements/ # Static assets
├── upm_logo.png # University logo
├── Right Side.png # Login illustration
├── loginRateLimit.png # Rate limit popup
└── loginAccDeleted.png # Account deleted popup
```
