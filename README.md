# 📝 My First Blog

A Django-based blogging platform that started with the Django Girls tutorial and evolved into a multi-user blog with enhanced features — built primarily as a learning project to explore new concepts, not a full-featured production app.

**Live Demo**: [sujithts.pythonanywhere.com](https://sujithts.pythonanywhere.com/)

## Features

- **User Authentication** - Custom registration and login system
-  **Post Management** - Create, edit, and publish blog posts
-  **Comment System** - User comments with author moderation
-  **Pagination** - Clean navigation for posts and content
-  **Responsive Design** - Works on desktop and mobile
-  **Security** - CSRF protection and user permissions
##  Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/07SUJITH/my-first-blog.git
cd my-first-blog
```

### 2. Create & activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate     # Windows
```

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the project root:
```ini
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Apply migrations
```bash
python manage.py migrate
```

### 6. (Optional) Create a superuser
```bash
python manage.py createsuperuser
```

### 7. Run the development server
```bash
python manage.py runserver
```

### 8. View your blog

Visit `http://127.0.0.1:8000/` to see your blog!

## Project Structure

```
my-first-blog/
├── accounts/         # User registration & auth
├── blog/             # Main blog functionality
├── mysite/           # Django project settings
├── static_src/       # shared static files
├── templates/        # Shared templates
└── requirements.txt
```

## Key Commands

```bash
# Development
python manage.py runserver
python manage.py shell

# Database
python manage.py makemigrations
python manage.py migrate
```

## Deployment to PythonAnywhere

Follow these steps to deploy and update your Django blog on PythonAnywhere.

### 1. Initial Setup
1. Open a Bash console on PythonAnywhere.  
2. Install the PythonAnywhere CLI:
    ```bash
    pip install --user pythonanywhere
    ```
3. Auto-configure your app (replace with your repo URL):
    ```bash
    pa_autoconfigure_django.py --python=3.10 https://github.com/your-username/my-first-blog.git
    ```

4. Create a Django superuser:
    ```bash
    python manage.py createsuperuser
    ```

### 2. Configure Environment Variables
In the PythonAnywhere **Files** tab → **project directory**, add
.env file
- `DJANGO_SECRET_KEY=your_secret_key`
- `DEBUG=False`
- `ALLOWED_HOSTS=yourdomain.pythonanywhere.com`

### 3. Deploying Updates
After pushing changes to GitHub:
```bash
# 1. open Bash console
cd ~/yourusername.pythonanywhere.com

# 2. Pull latest commits
git pull 

# 3. Activate virtualenv
workon yourusername.pythonanywhere.com

# 4. Install new dependencies
pip install -r requirements.txt

# 5. Apply migrations
python manage.py migrate

# 6. Collect static files
python manage.py collectstatic 
```
Finally, click **Reload** on the **Web** tab.

### 4. Troubleshooting Tips
- Check **Error logs** under the **Web** tab for stack traces.
- Run `python manage.py makemigrations` if you see migration errors.
- Confirm `DEBUG=False` and correct `ALLOWED_HOSTS` in production.
- Use `tail -f server.log` in Bash to watch real-time logs.

## Built With

- **Django 5.1.2** - Web framework
- **SQLite** - Database (development)
- **PythonAnywhere** - Hosting platform

## License

Based on the [Django Girls Tutorial](https://tutorial.djangogirls.org/) - extended with additional features. Feel free to use, modify, and learn.

## Final Thoughts
My First Blog is a learning-focused project built to explore Django’s built-in features — like authentication, models, views, templates, and deployment.
It’s not a polished product, but a stepping stone for understanding how Django works in practice.

A first blog — not the final word.