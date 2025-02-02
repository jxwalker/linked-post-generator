# Linked Post Generator
An AI-powered tool for generating and scheduling social media posts from news sources.

## Features

- 🤖 AI-powered post generation from RSS feeds
- 📅 Automated post scheduling
- 📱 Multi-platform support (LinkedIn, Twitter)
- 📊 Post history tracking and analytics
- 📧 Email notifications
- 🔐 User authentication and management

## Prerequisites

- Python 3.8+
- Node.js 14+
- SQLite (or another supported database)
- OpenAI API key

## Getting Started Guide

### 1. Backend Setup

#### 1.1 Create and activate virtual environment
```bash
# Create venv
python -m venv venv

# Activate venv
# On Windows:
venv\Scripts\activate
# On Unix/MacOS:
source venv/bin/activate
```

#### 1.2 Install dependencies
```bash
pip install -r requirements.txt
```

#### 1.3 Set up environment variables
```bash
# Copy template
cp .env.template .env

# Edit .env with your values, especially:
# - SECRET_KEY (generate a secure random string)
# - OPENAI_API_KEY (get from OpenAI dashboard)
# - SMTP settings (if you want email notifications)
```

#### 1.4 Initialize database and create superuser
```bash
# Run initialization script
python scripts/init_db.py admin@example.com your_password
```

#### 1.5 Start the backend server
```bash
# Start with hot reload
uvicorn src.main:app --reload --port 8000
```

### 2. Frontend Setup

#### 2.1 Install Node.js dependencies
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

#### 2.2 Configure frontend environment
```bash
# Create .env file
echo "REACT_APP_API_BASE_URL=http://localhost:8000/api/v1" > .env
```

#### 2.3 Start frontend development server
```bash
npm start
```

### 3. Testing the Application

#### 3.1 Access the application
- Open your browser and navigate to `http://localhost:3000`
- You should see the login page

#### 3.2 Login
- Use the superuser credentials you created:
  - Email: admin@example.com
  - Password: your_password

#### 3.3 Create your first post
1. Click "Create Post" in the sidebar
2. Add a news source (example RSS feeds):
   - TechCrunch: `https://techcrunch.com/feed/`
   - The Verge: `https://www.theverge.com/rss/index.xml`
3. Select platforms (LinkedIn/Twitter)
4. Click "Generate Posts"

#### 3.4 Verify functionality
- Check the generated post content
- Verify it's saved in Post History
- Check the database entries:
```sql
# Using SQLite CLI
sqlite3 linkedpost.db

# View posts
SELECT * FROM post_history;

# View users
SELECT * FROM users;
```

### 4. Troubleshooting

#### 4.1 Backend issues
- Check logs in the terminal running uvicorn
- Verify database connection:
```bash
sqlite3 linkedpost.db .tables
```
- Check API endpoints at `http://localhost:8000/docs`

#### 4.2 Frontend issues
- Check browser console for errors
- Verify API connection:
```bash
curl http://localhost:8000/api/v1/health
```

#### 4.3 Common issues
- CORS errors: Verify ALLOWED_ORIGINS in .env
- Database errors: Delete linkedpost.db and rerun init_db.py
- Authentication issues: Clear browser localStorage and login again

### 5. Monitoring

#### 5.1 Backend monitoring
- API documentation: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/v1/health`

#### 5.2 Database monitoring
```bash
# Check database size
ls -lh linkedpost.db

# Check table structure
sqlite3 linkedpost.db ".schema"
```

#### 5.3 Scheduler monitoring
- Check scheduled jobs in the backend logs
- View scheduled tasks in the frontend Scheduler panel

### 6. Next Steps

After verifying basic functionality:
1. Set up proper email notifications
2. Configure social media platform API keys
3. Add more news sources
4. Customize post generation prompts

Need help? Check the error logs or create an issue in the repository.

## Project Structure

```
├── src/                    # Backend source code
│   ├── api/               # API endpoints
│   │   ├── api/               # API endpoints
│   │   ├── core/              # Business logic
│   │   ├── models/            # Database models
│   │   └── utils/             # Utility functions
│   ├── frontend/              # React frontend
│   │   ├── src/
│   │   │   ├── components/    # Reusable components
│   │   │   ├── pages/         # Page components
│   │   │   └── services/      # API services
│   │   └── public/
│   ├── scripts/               # Utility scripts
│   ├── migrations/            # Database migrations
│   └── tests/                 # Test suites
└──
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [React](https://reactjs.org/) - Frontend framework
- [OpenAI](https://openai.com/) - AI capabilities

## Contact

Project Link: [https://github.com/jxwalker/linked-post-generator](https://github.com/jxwalker/linked-post-generator)
