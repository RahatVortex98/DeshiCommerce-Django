# 🛍️ DeshiCommerce - Django eCommerce Web Application

DeshiCommerce is a full-featured, dynamic eCommerce web application built using Django and PostgreSQL. It includes everything you need to run an online store: product listings, variations (color/size), add-to-cart functionality, customer reviews and ratings, user authentication, admin controls, and more.

Designed to be clean, professional, and fully scalable.

---

## 🚀 Features

- 🛒 Product listing with category filtering
- 🔍 Product detail pages with image gallery and variations
- 🛍️ Add to cart with stock check
- 🧾 Dynamic cart system
- ⭐ Customer reviews and star-based rating system (0.5 to 5 stars)
- 🔐 User registration, login, and logout
- 🧑 Admin dashboard via Django Admin
- 🖼️ Media uploads for product images
- 📅 Auto timestamps for reviews and products
- 🧠 Smart review handling (only one review per user per product; updatable)
- 📱 Responsive UI using Bootstrap

---

## 🧑‍💻 Tech Stack

- **Backend:** Django 5.x
- **Frontend:** HTML5, Bootstrap, Font Awesome
- **Database:** PostgreSQL
- **Authentication:** Django’s built-in auth system
- **Reviews & Ratings:** Custom `ReviewRating` model with rating radio buttons
- **Cart System:** Session-based, supports variations

---

## 📁 Project Structure

```
deshiCommerce/
├── accounts/               # User model and auth views
├── store/                  # Product, Category, ReviewRating models
├── carts/                  # Cart and cart items
├── templates/
│   ├── base.html
│   ├── store/
│   │   ├── product_detail.html
│   │   ├── category.html
├── static/                 # CSS, JS, and images
├── media/                  # Uploaded product images
├── manage.py
├── requirements.txt
└── db.postgresql
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/deshiCommerce.git
cd deshiCommerce
```

### 2. Create Virtual Environment

```bash
python -m venv venv
# Activate virtualenv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. PostgreSQL Configuration

Update the `DATABASES` section in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Migrate Database & Create Superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run Server

```bash
python manage.py runserver
```

Then visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## ✨ Admin Panel

- URL: `/admin/`
- Manage:
  - Products
  - Categories
  - Variations
  - Review ratings
  - Users

---

## ⭐ Review & Rating System

Each product has its own review section:

- Logged-in users can:
  - Submit one review per product
  - Edit their review later
- Rating uses 0.5 to 5 stars
- Star icons rendered dynamically with logic
- Review model:

```python
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

---

## 🧾 Cart System

- Session-based cart with variation handling
- Select color and size (if applicable) before adding to cart
- Quantity and stock managed dynamically
- Cart stored per user (or session if not logged in)

---

## 🖼️ Media Uploads

Images for products are stored in `/media/`. Make sure to configure:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

Add in `urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 🔐 Authentication

- Register/Login via `accounts/`
- CSRF-protected forms
- Custom user model for future scalability

---

## 🌍 Deployment (Heroku/Render)

### Environment Variables Needed:

- `DEBUG=False`
- `ALLOWED_HOSTS=['yourdomain.com']`
- `SECRET_KEY=your_secret_key`
- `DATABASE_URL` for PostgreSQL

### Production Steps:

1. Install `gunicorn`, `whitenoise`, and `dj-database-url`
2. Set `DEBUG=False` and configure static/media settings
3. Use `collectstatic`
4. Add Procfile for Heroku

---

## 📦 requirements.txt

```txt
Django>=5.0
psycopg2-binary
Pillow
django-crispy-forms
gunicorn
whitenoise
dj-database-url
```

Generate with:

```bash
pip freeze > requirements.txt
```

---

## 👨‍💻 Author

**Rahat**  
Django Developer  
📧 Email / LinkedIn / Portfolio (add your links here)

---






![verfication](https://github.com/user-attachments/assets/9124cca1-009a-454c-897c-b26e5edabfa4)
![notregisteracc](https://github.com/user-attachments/assets/6844a73b-3939-43c5-9abd-fdb4f4819b7a)
![resetemaillink](https://github.com/user-attachments/assets/94c68a33-b8e7-4c21-b24c-25b49ab3e052)
![after click reset link](https://github.com/user-attachments/assets/32fbc680-3619-4fdc-910f-898c2672a6ea)
![after reset new password](https://github.com/user-attachments/assets/1bfd26b2-faa4-47a3-814e-ff2342ebf4b4)
![Capture](https://github.com/user-attachments/assets/92fa4355-580a-4efc-9b7c-2d02f263bf7b)
![variation of product](https://github.com/user-attachments/assets/77d28aa6-cc81-474e-af64-13e4f31c3334)
![bill payment review1](https://github.com/user-attachments/assets/085d0add-cdc5-4e9c-8b64-ed801fea0f0f)
![bill payment review 2](https://github.com/user-attachments/assets/abf4fd04-8839-4597-b067-eff33b033b96)
![initial stage if ur logged in](https://github.com/user-attachments/assets/69fcafd7-856d-468f-a9f4-4d04132f005f)
![if u are not loggin](https://github.com/user-attachments/assets/98f08e36-a859-458d-8f9d-09f8548352df)
![after submission](https://github.com/user-attachments/assets/81cb7a55-5dac-4b49-b2fe-7a45b3b4a31f)
![same user can update review](https://github.com/user-attachments/assets/c0471c01-e515-40d2-80d9-cf9aa639a1a8)
![must purchase for po![displaying reveiw rating](https://github.com/user-attachments/assets/b9d6e2f2-38ee-49ca-9ef5-b4f6931c2ef8)
sting review](https://github.com/user-attachments/assets/d4314ff3-c554-4593-8719-016ba09b356e)
