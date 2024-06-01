import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import auth
import pickle
import requests
import re
from PIL import Image
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

# Fungsi untuk memuat animasi Lottie dari URL
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Fungsi untuk memuat model machine learning
def load_model():
    with open("obesity_classifier.pkl", "rb") as file:
        obesity_classifier = pickle.load(file) 
    return obesity_classifier

# CSS untuk latar belakang, gaya, dan animasi
def load_css():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://img.freepik.com/free-photo/sports-equipment-paper-background_23-2147735014.jpg?t=st=1717171847~exp=1717175447~hmac=8ce274d41b7add0762ef7d267cdad64bb214a4ea239582b26e4ba176d2e3870f&w=1060");
            background-size: cover;
            transition: background 0.5s ease;
        }
        .title-box {
            text-align: center;
            margin-top: 2rem;
        }
        .title-box h1 {
            font-size: 3rem;
            color: #fff;
        }
        .info-box {
            text-align: center;
            margin-top: 2rem;
            color: #fff;
            background: rgba(0, 0, 0, 0.5);
            padding: 1rem;
            border-radius: 1rem;
        }
        .center-buttons {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 4rem;
        }
        .center-buttons button {
            font-weight: bold;
            font-size: 1.1rem;
            padding: 0.5rem 1rem;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 0 0.5rem;
            transition: background-color 0.3s ease;
        }
        .center-buttons button:hover {
            background-color: #0056b3;
        }
        .extra-box {
            text-align: center;
            margin-top: 1rem;
            color: #fff;
            background: rgba(0, 0, 0, 0.5);
            padding: 1rem;
            border-radius: 1rem;
        }
        .top-menu {
            display: flex;
            justify-content: flex-end;
            background: rgba(0, 0, 0, 0.7);
            padding: 0.5rem 1rem;
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        .top-menu a {
            color: #fff;
            margin: 0 1rem;
            text-decoration: none;
            font-weight: bold;
        }
        .button-container {
            display: flex;
            justify-content: center;
            margin-top: 4rem;
        }
        .button-container .stButton {
            margin: 0 0.5rem;
        }
        .article-container {
            background: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            padding: 10px;
            margin-top: 10px;
            text-align: center;
        }
        .article-container img {
            border-radius: 10px;
        }
        </style>
        """, unsafe_allow_html=True
    )

# Fungsi Validasi
def check_uppercase(password):
    return any(c.isupper() for c in password)

def check_lowercase(password):
    return any(c.islower() for c in password)

def check_digit(password):
    return any(c.isdigit() for c in password)

def check_no_symbols(password):
    return password.isalnum()

def is_valid_password(password):
    return check_uppercase(password) and check_lowercase(password) and check_digit(password) and check_no_symbols(password)

def is_valid_email(email):
    return email.endswith('@gmail.com')


# Fungsi untuk menyimpan artikel yang diunggah
def save_article(title, description, image, link):
    if 'articles' not in st.session_state:
        st.session_state['articles'] = []
    st.session_state['articles'].append({
        "title": title,
        "description": description,
        "image": image,
        "link": link
    })

# Fungsi untuk membuat koneksi ke database
def create_connection():
    return sqlite3.connect('users.db')

# Halaman registrasi
def signup():
    st.title("Sign Up")

    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        role = st.selectbox("Role", ["user", "admin"])
        submit_button = st.form_submit_button(label="Sign Up")

        # Checkbox ketentuan password
        st.write("Password must contain:")
        st.checkbox("At least one uppercase letter", value=check_uppercase(password), disabled=True)
        st.checkbox("At least one lowercase letter", value=check_lowercase(password), disabled=True)
        st.checkbox("At least one digit", value=check_digit(password), disabled=True)
        st.checkbox("No symbols", value=check_no_symbols(password), disabled=True)

        if submit_button:
            if not email or not password:
                st.error("Email and Password cannot be empty")
            elif not is_valid_email(email):
                st.error("Email harus diakhiri dengan @gmail.com")
            elif not is_valid_password(password):
                st.error("Password harus mengandung huruf besar, huruf kecil, dan angka. Tidak boleh ada simbol.")
            elif password != confirm_password:
                st.error("Password dan konfirmasi password tidak cocok.")
            elif auth.user_exists(email):
                st.error("Email already exists")
            elif role == 'admin':
                st.error("Cannot sign up with admin role")
            else:
                auth.create_user(email, password, role)
                st.success("User created successfully")

    if st.button("Back"):
        st.session_state['page'] = 'landing'
        st.experimental_rerun()

# Halaman login
def login():
    st.title("Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["user", "admin"])
        submit_button = st.form_submit_button(label="Login")

        if submit_button:
            if not email or not password:
                st.error("Email and Password cannot be empty")
            elif not is_valid_email(email):
                st.error("Email harus diakhiri dengan @gmail.com")
            elif not is_valid_password(password):
                st.error("Password harus mengandung huruf besar, huruf kecil, dan angka. Tidak boleh ada simbol.")
            else:
                user = auth.check_credentials(email, password, role)
                if user:
                    st.success("Login successful")
                    st.session_state['logged_in'] = True
                    st.session_state['email'] = email
                    st.session_state['role'] = user[3]
                    st.experimental_rerun()
                else:
                    st.error("Invalid email or password")

    if st.button("Back"):
        st.session_state['page'] = 'landing'
        st.experimental_rerun()

# Halaman utama setelah login
def main_page():
    st.title("Welcome to Go Motion Dashboard")
    st.write(f"Hello, {st.session_state['email']}! You are logged in as {st.session_state['role']}.")

    # Contoh data untuk grafik
    bmi_data = {
        'Category': ['Insufficient Weight', 'Normal Weight', 'Overweight Level 1', 'Overweight Level 2', 'Obesity Level 1', 'Obesity Level 2', 'Obesity Level 3'],
        'Count': [5, 20, 10, 7, 15, 5, 3]
    }
    fig = px.bar(
        bmi_data, 
        x='Category', 
        y='Count', 
        title='BMI Categories Distribution',
        template='plotly_dark'
    )
    fig.update_layout(
        title={'x': 0.5, 'xanchor': 'center'},
        font=dict(size=14),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    # Menampilkan grafik
    st.plotly_chart(fig)

    # Menampilkan grafik
    st.plotly_chart(fig)

    # Grafik interaktif lainnya
    age_data = {
        'Age Group': ['<18', '18-25', '26-35', '36-45', '46-55', '56-65', '>65'],
        'Count': [5, 15, 20, 10, 7, 3, 2]
    }
    fig2 = px.pie(age_data, values='Count', names='Age Group', title='Age Distribution of Users')

    st.plotly_chart(fig2)

    st.write("Dashboard ini memberikan gambaran umum tentang data pengguna dan distribusi kategori BMI.")

    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()

# Halaman artikel
def articles_page():
    st.title("Articles")
    st.write("Here are some interesting articles for you to read.")
    display_articles()

# Halaman hitung BMI sebagai template untuk model ML
def bmi_page():
    st.title("Calculate BMI")

    with st.form("bmi_form"):
        height = st.number_input("Height (in cm)", min_value=50, max_value=250)
        weight = st.number_input("Weight (in kg)", min_value=20, max_value=200)
        submit_button = st.form_submit_button(label="Calculate BMI")

        if submit_button:
            if height and weight:
                bmi = weight / ((height / 100) ** 2)
                st.write(f"Your BMI is: {bmi:.2f}")
                
                # Placeholder untuk hasil prediksi model ML
                st.write("Predicted health status: ... (ML Model Placeholder)")
            else:
                st.error("Please enter both height and weight")

# Halaman klasifikasi obesitas
def obesity_classification_page():
    st.title("Check Your Condition")

    with st.form("obesity_form"):
        age = st.slider("Age", min_value=1, max_value=120)
        gender = st.selectbox("Gender", ["Male", "Female"])
        height = st.slider("Height (in meters)", min_value=0.5, max_value=2.5, step=0.01)
        weight = st.slider("Weight (in kg)", min_value=20, max_value=200)

        calc = st.selectbox("How often do you drink alcohol?", ["Never", "Sometimes", "Frequently", "Always"])
        favc = st.selectbox("Do you eat high caloric food frequently?", ["No", "Yes"])
        fcvc = st.slider("Do you usually eat vegetables in your meals?", min_value=0, max_value=10)
        ncp = st.slider("How many main meals do you have daily?", min_value=0, max_value=10)
        scc = st.selectbox("Do you monitor the calories you eat daily?", ["No", "Yes"])
        smoke = st.selectbox("Do you smoke?", ["No", "Yes"])
        ch20 = st.slider("How much water do you drink daily? (in liters)", min_value=0.0, max_value=10.0, step=0.1)
        fhwo = st.selectbox("Family History With Overweight", ["No", "Yes"])
        faf = st.slider("How often do you have physical activity? (days per week)", min_value=0, max_value=7)
        tue = st.slider("How much time do you use technological devices daily? (in hours)", min_value=0, max_value=24)
        caec = st.selectbox("Do you eat any food between meals?", ["No", "Sometimes", "Frequently", "Always"])
        mtrans = st.selectbox("Which transportation do you usually use?", ["Automobile", "Motorbike", "Bike", "Public Transportation", "Walking"])

        submit_button = st.form_submit_button(label="Check Status")

        if submit_button:
            if all([age, height, weight]):
                gender_value = 1 if gender == "Male" else 0
                calc_value = {"Never": 0, "Sometimes": 1, "Frequently": 2, "Always": 3}[calc]
                favc_value = 1 if favc == "Yes" else 0
                scc_value = 1 if scc == "Yes" else 0
                smoke_value = 1 if smoke == "Yes" else 0
                fhwo_value = 1 if fhwo == "Yes" else 0
                caec_value = {"No": 0, "Sometimes": 1, "Frequently": 2, "Always": 3}[caec]
                mtrans_value = {"Automobile": 0, "Motorbike": 1, "Bike": 2, "Public Transportation": 3, "Walking": 4}[mtrans]

                # Load model and predict
                obesity_classifier = load_model()
                prediction = obesity_classifier.predict([[age, gender_value, height, weight, calc_value, favc_value, fcvc, ncp, scc_value, smoke_value, ch20, fhwo_value, faf, tue, caec_value, mtrans_value]])[0]
                
                st.write(f"Your BMI is: {weight / ((height) ** 2):.2f}")
                if int(prediction) == 0:
                     st.write(f"Predicted health status: Issufficient Weight")
                if int(prediction) == 1:
                     st.write(f"Predicted health status: Normal Weight")
                if int(prediction) == 2:
                     st.write(f"Predicted health status: OverWeight Level 1")
                if int(prediction) == 3:
                     st.write(f"Predicted health status: OverWeight Level 2")
                if int(prediction) == 4:
                     st.write(f"Predicted health status: Obesity Level 1")
                if int(prediction) == 5:
                     st.write(f"Predicted health status: Obesity Level 2")
                if int(prediction) == 5:
                     st.write(f"Predicted health status: Obesity Level 3")
            else:
                st.error("Please fill in all the details")

# Fungsi untuk menampilkan artikel
def display_articles():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM articles")
    articles = c.fetchall()
    conn.close()

# Menampilkan artikel dalam grid
    cols_per_row = 2
    num_articles = len(articles)
    rows = (num_articles // cols_per_row) + (1 if num_articles % cols_per_row != 0 else 0)

    for row in range(rows):
        cols = st.columns(cols_per_row)
        for col_num in range(cols_per_row):
            article_index = row * cols_per_row + col_num
            if article_index < num_articles:
                article = articles[article_index]
                with cols[col_num]:
                    st.markdown(f"### {article[1]}")
                    st.image(article[3], use_column_width=True)
                    st.write(article[2])
                    st.markdown(f"[Read more]({article[4]})")

# Halaman admin untuk menambahkan dan menghapus artikel
def admin_page():
    st.title("Admin Page")
    st.write("Manage articles")

    with st.form("article_form"):
        title = st.text_input("Title")
        description = st.text_area("Description")
        image_url = st.text_input("Image URL")
        url = st.text_input("Article URL")
        submit_button = st.form_submit_button(label="Add Article")

        if submit_button:
            if title and description and image_url and url:
                conn = create_connection()
                c = conn.cursor()
                c.execute("INSERT INTO articles (title, description, image_url, url) VALUES (?, ?, ?, ?)", (title, description, image_url, url))
                conn.commit()
                conn.close()
                st.success("Article added successfully")
            else:
                st.error("All fields are required")

    st.write("### Existing Articles")

    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM articles")
    articles = c.fetchall()
    conn.close()

    for article in articles:
        st.markdown(f"#### {article[1]}")
        st.image(article[3], use_column_width=True)
        st.write(article[2])
        st.markdown(f"[Read more]({article[4]})")
        if st.button(f"Delete {article[1]}", key=article[0]):
            delete_article(article[0])
            st.success(f"Article '{article[1]}' deleted successfully")
            st.experimental_rerun()

# Fungsi untuk menghapus artikel dari database
def delete_article(article_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute("DELETE FROM articles WHERE id = ?", (article_id,))
    conn.commit()
    conn.close()

# Halaman bantuan
def help_page():
    st.title("Help")
    st.write("This is the help page. How can we assist you?")

# Halaman landing
def landing_page():
    st.markdown("""
    <div class="title-box">
        <h1>Welcome to Go Motion</h1>
    </div>
    <div class="info-box">
        <p>Platform untuk deteksi dini risiko kesehatan Anda</p>
    </div>
    """, unsafe_allow_html=True)


    # Animasi Lottie
    lottie_animation = load_lottie_url("https://lottie.host/2f5893df-cc66-48be-be2d-9092bd6a9877/xKC7RTy8kE.json")
    if lottie_animation:
        st_lottie(lottie_animation, height=300, key="landing")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Sign Up Now"):
            st.session_state['page'] = 'signup'
            st.experimental_rerun()
    with col2:
        if st.button("Sign In"):
            st.session_state['page'] = 'login'
            st.experimental_rerun()

 # Menampilkan artikel dalam kolom
    display_articleslp()

    st.markdown("""
    <div class="extra-box">
        <p>Tentang Kami</p>
    </div>
    """, unsafe_allow_html=True)

# Menampilkan artikel dalam kolom
def display_articleslp():
    articles = [
        {
            "title": "Sit Down While You Eat. It Makes A Big Difference.",
            "description": "Learn about the essential nutrients your body needs.",
            "image_url": "https://d35oenyzp35321.cloudfront.net/MHC_Blog_Health_Benefits_of_Sitting_Down_to_Eat_38a8bf3be5.jpg",
            "url": "https://www.maxhealthcare.in/blogs/sit-down-while-you-eat-it-makes-big-difference"
        },
        {
            "title": "Indian Diet Plan In Pregnancy",
            "description": "Discover how staying healthy in pregnancy.",
            "image_url": "https://d35oenyzp35321.cloudfront.net/indian_diet_plan_ae5b9f7f27.jpg",
            "url": "https://www.maxhealthcare.in/blogs/indian-diet-plan-pregnancy"
        },
        {
            "title": "Understanding BMI",
            "description": "A guide to understanding Body Mass Index and its implications.",
            "image_url": "https://d35oenyzp35321.cloudfront.net/love_your_age_fce9d54f64.jpg",
            "url": "https://www.maxhealthcare.in/blogs/love-your-age"
        },
        {
            "title": "Healthy Eating on a Budget",
            "description": "Tips for maintaining a healthy diet without breaking the bank.",
            "image_url": "https://via.placeholder.com/150",
            "url": "https://example.com/article4"
        },
        {
            "title": "Managing Stress",
            "description": "Techniques to help you manage stress effectively.",
            "image_url": "https://via.placeholder.com/150",
            "url": "https://example.com/article5"
        },
        {
            "title": "The Role of Sleep in Health",
            "description": "Learn about the importance of sleep for your wellbeing.",
            "image_url": "https://via.placeholder.com/150",
            "url": "https://example.com/article6"
        }
    ]

    st.markdown("## Rekomendasi Artikel")

    for i in range(0, len(articles), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(articles):
                article = articles[i + j]
                with cols[j]:
                    st.image(article["image_url"], use_column_width=True)
                    st.markdown(f"### {article['title']}")
                    st.write(f"{article['description']} [Read more]({article['url']})")


# Fungsi utama untuk mengatur halaman-halaman
def main():
    load_css()
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'page' not in st.session_state:
        st.session_state['page'] = 'landing'
    if 'role' not in st.session_state:
        st.session_state['role'] = None

    if st.session_state['logged_in']:
        with st.sidebar:
            selected = option_menu(
                menu_title="Menu",
                options=["Home", "Articles", "Calculate BMI", "Check Your Condition", "Help", "Admin Page", "Logout"]
                if st.session_state['role'] == 'admin'
                else ["Home", "Articles", "Calculate BMI", "Check Your Condition", "Help", "Logout"],
                icons=["house", "book", "calculator", "check-circle", "question-circle", "gear", "door-open"],
                menu_icon="cast",
                default_index=0,
            )

        if selected == "Home":
            main_page()
        elif selected == "Articles":
            articles_page()
        elif selected == "Calculate BMI":
            bmi_page()
        elif selected == "Check Your Condition":
            obesity_classification_page()
        elif selected == "Help":
            help_page()
        elif selected == "Admin Page":
            admin_page()
        elif selected == "Logout":
            st.session_state['logged_in'] = False
            st.session_state['page'] = 'landing'
            st.experimental_rerun()
    else:
        if st.session_state['page'] == 'landing':
            landing_page()
        elif st.session_state['page'] == 'login':
            login()
        elif st.session_state['page'] == 'signup':
            signup()

if __name__ == "__main__":
    main()
