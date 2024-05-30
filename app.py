import streamlit as st
from streamlit_option_menu import option_menu
import auth
import pickle

# Fungsi untuk memuat model machine learning
def load_model():
    with open("obesity_classifier.pkl", "rb") as file:
        model = pickle.load()
    return model

# CSS untuk latar belakang, gaya, dan animasi
def load_css():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://r4.wallpaperflare.com/wallpaper/535/845/69/digital-art-artwork-fantasy-art-planet-sun-hd-wallpaper-d866fd38b0b06cd800cc016ed8d284fa.jpg");
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
            margin: 0 1rem;
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
        </style>
        """, unsafe_allow_html=True
    )

# Halaman registrasi
def signup():
    st.title("Sign Up")

    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["user", "admin"])
        submit_button = st.form_submit_button(label="Sign Up")
        back_button = st.form_submit_button(label="Back to Landing Page")

        if submit_button:
            if not email or not password:
                st.error("Email and Password cannot be empty")
            elif auth.user_exists(email):
                st.error("Email already exists")
            elif role == 'admin':
                st.error("Cannot sign up with admin role")
            else:
                auth.create_user(email, password, role)
                st.success("User created successfully")
        if back_button:
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
        back_button = st.form_submit_button(label="Back to Landing Page")

        if submit_button:
            if not email or not password:
                st.error("Email and Password cannot be empty")
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
        if back_button:
            st.session_state['page'] = 'landing'
            st.experimental_rerun()

# Halaman utama setelah login
def main_page():
    st.title("Welcome to Go Motion")
    st.write(f"Hello, {st.session_state['email']}! You are logged in as {st.session_state['role']}.")
    st.write(f"Status: Login sebagai {st.session_state['role']}.")
    st.write("This is the main page of the application.")

    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()

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
        age = st.number_input("Age", min_value=1, max_value=120)
        gender = st.selectbox("Gender", ["Male", "Female"])
        height = st.number_input("Height (in cm)", min_value=50, max_value=250)
        weight = st.number_input("Weight (in kg)", min_value=20, max_value=200)

        calc = st.selectbox("How often do you drink alcohol?", ["Never", "Sometimes", "Frequently", "Always"])
        favc = st.selectbox("Do you eat high caloric food frequently?", ["No", "Yes"])
        fcvc = st.number_input("Do you usually eat vegetables in your meals?", min_value=0, max_value=10)
        ncp = st.number_input("How many main meals do you have daily?", min_value=0.0, max_value=10.0, step=0.1)
        scc = st.selectbox("Do you monitor the calories you eat daily?", ["No", "Yes"])
        smoke = st.selectbox("Do you smoke?", ["No", "Yes"])
        ch20 = st.number_input("How much water do you drink daily? (in liters)", min_value=0.0, max_value=10.0, step=0.1)
        fhwo = st.selectbox("Family History With Overweight", ["No", "Yes"])
        faf = st.number_input("How often do you have physical activity? (days per week)", min_value=0.0, max_value=7.0, step=0.1)
        tue = st.number_input("How much time do you use technological devices daily? (in hours)", min_value=0, max_value=24)
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
                model = load_model()
                prediction = model.predict([[height, weight, age, gender_value, calc_value, favc_value, fcvc, ncp, scc_value, smoke_value, ch20, fhwo_value, faf, tue, caec_value, mtrans_value]])[0]
                
                st.write(f"Your BMI is: {weight / ((height / 100) ** 2):.2f}")
                st.write(f"Predicted health status: {prediction}")
            else:
                st.error("Please fill in all the details")

# Halaman bantuan
def help_page():
    st.title("Help")
    st.write("This is the help page. How can we assist you?")
    # Anda bisa menambahkan lebih banyak konten di sini

# Halaman landing page
def landing_page():
    st.markdown(
        """
        <div class="title-box">
            <h1>Go Motion</h1>
        </div>
        <div class="info-box">
            <p>Aplikasi Go Motion merupakan solusi terbaik untuk membuat hidup menjadi lebih sehat dengan meningkatkan kegiatan aktifitas fisik.</p>
        </div>
        <div class="extra-box">
            <h3>Recommended Articles</h3>
            <ul>
                <li><a href="#" target="_blank">Article 1</a></li>
                <li><a href="#" target="_blank">Article 2</a></li>
                <li><a href="#" target="_blank">Article 3</a></li>
            </ul>
        </div>
        """, unsafe_allow_html=True
    )

    if st.session_state.get('redirect_page'):
        st.session_state['page'] = st.session_state['redirect_page']
        st.session_state['redirect_page'] = None
        st.experimental_rerun()

    if st.button("Sign Up Now"):
        st.session_state['page'] = 'signup'
        st.experimental_rerun()

    if st.button("Sign In"):
        st.session_state['page'] = 'login'
        st.experimental_rerun()

# Navigasi antara halaman
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
                options=["Home", "Articles", "Calculate BMI", "Cek Statusmu", "Help", "Admin Page", "Logout"]
                if st.session_state['role'] == 'admin'
                else ["Home", "Articles", "Calculate BMI", "Cek Statusmu", "Help", "Logout"],
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
        elif selected == "Cek Statusmu":
            obesity_classification_page()
        elif selected == "Help":
            help_page()
        elif selected == "Admin Page":
            st.write("Admin page content goes here.")
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
