import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import hashlib
import pickle

# Fungsi untuk hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Fungsi untuk membuat koneksi ke database
def create_connection():
    return sqlite3.connect('users.db')

# Fungsi untuk membuat pengguna baru
def create_user(email, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hash_password(password)))
    conn.commit()
    conn.close()

# Fungsi untuk memeriksa apakah pengguna ada
def user_exists(email):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    return user

# Fungsi untuk memeriksa kredensial pengguna
def check_credentials(email, password):
    user = user_exists(email)
    if user and user[2] == hash_password(password):
        return True
    return False

# Fungsi untuk memuat model machine learning
def load_model():
    with open("obesity_classifier.pkl", "rb") as file:
        model = pickle.load(file)
    return model

# CSS untuk latar belakang, gaya, dan animasi
def load_css():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://media.istockphoto.com/id/1302561463/id/foto/latar-belakang-iridescent-holografik-unicorn-warna-warni-pelangi-foil-abstrak-indah-pelangi.jpg?s=612x612&w=0&k=20&c=6k8vaozkyangY_Kg2uW9sf_TsA8AaZH9C94K5jKVBAs=");
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
        .login-box, .signup-box {
            background: rgba(255, 255, 255, 0.8);
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.5s ease, opacity 0.5s ease;
            max-width: 400px;
            margin: 2rem auto;
        }
        .login-box.animate, .signup-box.animate {
            transform: translateY(-10px);
            opacity: 0.9;
        }
        </style>
        """, unsafe_allow_html=True
    )

# JavaScript untuk animasi
def load_js():
    st.markdown(
        """
        <script>
        function animateBox() {
            var boxes = document.querySelectorAll('.login-box, .signup-box');
            boxes.forEach(function(box) {
                box.classList.add('animate');
                setTimeout(function() {
                    box.classList.remove('animate');
                }, 500);
            });
        }
        document.addEventListener("DOMContentLoaded", function() {
            var radios = document.querySelectorAll('input[type="radio"]');
            radios.forEach(function(radio) {
                radio.addEventListener('change', animateBox);
            });
        });
        </script>
        """, unsafe_allow_html=True
    )

# Halaman registrasi
def signup():
    st.title("Sign Up")

    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label="Sign Up")

        if submit_button:
            if not email or not password:
                st.error("Email and Password cannot be empty")
            elif user_exists(email):
                st.error("Email already exists")
            else:
                create_user(email, password)
                st.success("User created successfully")

# Halaman login
def login():
    st.title("Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label="Login")

        if submit_button:
            if not email or not password:
                st.error("Email and Password cannot be empty")
            elif check_credentials(email, password):
                st.success("Login successful")
                st.session_state['logged_in'] = True
                st.session_state['email'] = email
                st.experimental_rerun()  # Refresh the page to reflect the login status
            else:
                st.error("Invalid email or password")

# Halaman utama setelah login
def main_page():
    st.title("Welcome to Go Motion")
    st.write(f"Hello, {st.session_state['email']}!")
    st.write("This is the main page of the application.")
    
    if st.button("Logout"):
        st.session_state['logout_confirm'] = True

    if st.session_state.get('logout_confirm', False):
        if st.button("Yes, log me out"):
            st.session_state['logged_in'] = False
            st.session_state['logout_confirm'] = False
            st.experimental_rerun()
        if st.button("Cancel"):
            st.session_state['logout_confirm'] = False

# Halaman artikel
def articles_page():
    st.title("Articles")
    st.write("Here are some interesting articles for you to read.")
    # Anda bisa menambahkan lebih banyak konten di sini

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
    st.title("Cek Statusmu")

    with st.form("obesity_form"):
        height = st.number_input("Height (in cm)", min_value=50, max_value=250)
        weight = st.number_input("Weight (in kg)", min_value=20, max_value=200)
        age = st.number_input("Age", min_value=1, max_value=120)
        gender = st.selectbox("Gender", ["Male", "Female"])
        submit_button = st.form_submit_button(label="Check Status")

        if submit_button:
            if height and weight and age:
                bmi = weight / ((height / 100) ** 2)
                gender_value = 1 if gender == "Male" else 0
                
                model = load_model()
                prediction = model.predict([[height, weight, age, gender_value]])[0]
                
                st.write(f"Your BMI is: {bmi:.2f}")
                st.write(f"Predicted Obesity Status: {prediction}")
            else:
                st.error("Please enter height, weight, and age")

# Halaman help
def help_page():
    st.title("Help")
    st.write("If you need help, please contact our support team.")
    # Anda bisa menambahkan lebih banyak konten di sini

# Navigasi antara halaman
def main():
    load_css()
    load_js()
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",
                options=["Home", "Articles", "Calculate BMI", "Cek Statusmu", "Help", "Logout"],
                icons=["house", "book", "calculator", "check-circle", "question-circle", "door-open"],
                menu_icon="cast",
                default_index=0,
            )

        if selected == "Home":
            main_page()
        elif selected == "Articles":
            articles_page()
        elif selected == "Calculate BMI":
            bmi_page()
        elif selected == "Cek Statusmu":
            obesity_classification_page()
        elif selected == "Help":
            help_page()
        elif selected == "Logout":
            st.session_state['logout_confirm'] = True
            main_page()
    else:
        st.markdown('<div class="title-box"><h1>Go Motion</h1></div>', unsafe_allow_html=True)

        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Login", "Sign Up"])

        if page == "Login":
            with st.container():
                st.markdown('<div class="login-box">', unsafe_allow_html=True)
                login()
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            with st.container():
                st.markdown('<div class="signup-box">', unsafe_allow_html=True)
                signup()
                st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
