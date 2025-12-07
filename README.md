# 🛒 Django E-Commerce Website  
A clean and fully-functional E-Commerce web application built using Django.  
Features include product management, cart system, checkout flow, customer accounts, and admin order management.
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/ce64e62f-9208-46fd-b562-ee1f77068f4f" />


---

## ⭐ Features

### 👤 Customer Module
- User signup, login & logout  
- Customer profile linked with Django User  
- View products & product details  
- Add to Cart  
- Remove from Cart  
- Quantity + / – update  
- Checkout and place order  
- Order success page  
- My Orders (order history)  
- Order detail page with item breakdown  

---

### 🛍️ Product Module
- Add Product (Admin only)  
- Edit Product (Admin only)  
- Delete Product (Soft Delete)  
- Product list & priority-based ordering  
- Product detail page  

---

### 📦 Orders Module
- Complete cart system  
- Checkout page showing summary  
- Convert cart → confirmed order  
- Order status workflow  
- Customer order history  
- Admin order dashboard  
- Inline admin status update  
- Admin order detail page  

---

### 🎨 Themes / UI
- Dynamic banner (SiteSettings model)  
- Clean home page layout  
- Modern product cards  
- Admin UI separated from customer UI  
- Badges for order ID and order status  
- Number formatting using `django.contrib.humanize`  

---

### 🔐 Role-Based Access
- Admin access protected  
- Admin cannot add to cart / checkout  
- Admin sees Manage Products and Manage Orders  
- Customers see shopping features  
- Backend security in views  

---

## 🛠️ Tech Stack
- **Python 3**  
- **Django Framework**  
- **SQLite / PostgreSQL**  
- **HTML, CSS, Bootstrap**  
- **Django Templates**  
- **Django Contrib Humanize**  

---
###🔑 Admin creation
- sign up and login as normal user
- from django.contrib.auth.models import User

u = User.objects.get(username="your username or email")  # change if needed

u.is_staff = True

u.is_superuser = True

u.save()

---

---

###📂 Project Structure
<img width="1024" height="1536" alt="foldee structure" src="https://github.com/user-attachments/assets/01acba2f-ebaa-4469-ab01-b5c129be169b" />

---

---
###👨‍💻 Author

Adhil C R
Django Developer | Computer Engineering Student

---

###🧠 Mind Map  
<img width="1406" height="1668" alt="Mind map (1)" src="https://github.com/user-attachments/assets/93bfed3e-749f-4939-a036-e541666ad34a" />


###🗂 ERD Flowchart  
<img width="1008" height="1651" alt="Data model Flowchart ERD (1)" src="https://github.com/user-attachments/assets/fb9cb5d8-2193-4332-a4cc-cc97bcb9054f" />

