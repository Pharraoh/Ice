🧠 Project Overview
Ice is a full-stack dating web application that allows users to discover, match, and communicate with each other in real time. The platform focuses on user interaction and engagement through features like matching, chat, and status updates.

🚀 Key Features
- User authentication system
- User matching system
- Search users by username
- Online/Offline user status
- Real-time one-on-one chat
- Status/Story feature (text, image)
- Automatic status expiration (Celery + Redis)
- Profile editing with multiple images

🛠 Tech Stack
- Backend: Django
- Frontend: HTML, CSS, JavaScript
- Real-time features: Django channels and websockets
- Media storage: Cloudinary
- Task Queue: Celery + Redis

👨‍💻 My Contribution
I independently designed and developed the entire platform, including:
- Building the matching system and user interaction logic
- Implementing a real-time chat system using Django channels and websockets
- Developing a WhatsApp-style status feature with auto-expiration using Celery and Redis
- Creating online/offline presence tracking
- Designing user profile management with multiple image uploads
- Structuring the backend architecture and database models

📌 Future Improvements
- Push notifications
- Match recommendation algorithm
- Mobile app version
- Read receipts & typing indicators


⚙️ Installation & Setup
# Clone the repository
git clone https://github.com/Pharraoh/Ice.git

# Navigate into the project
cd Ice

# Create virtual environment
python -m venv venv

# Activate environment
venv\Scripts\activate
# or
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start Redis (required for Celery)
# Make sure Redis server is running

# Start server
python manage.py runserver
