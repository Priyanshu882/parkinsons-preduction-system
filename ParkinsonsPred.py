import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import base64

# Set page configuration
st.set_page_config(
    page_title="Health Assistant",
    layout="wide",
    page_icon="🧑‍⚕️"
)

# Function to Set Background Image
def set_background(image_path):
    with open(image_path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    
    bg_image = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* Custom Styling */
    .css-1d391kg, .stTextInput > div > input {{
        background-color: rgba(47, 63, 89, 0.8) !important;
        color: #CCCFDA !important;
        border-radius: 8px;
        padding: 10px;
    }}
    
    .stButton > button {{
        background-color: #FF4B4B !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px;
    }}

    h1, h2, h3 {{
        color: #CCCFDA !important;
        text-align: center;
    }}

    [data-testid="stSidebar"] {{
        background-color: #4F5D81 !important;
    }}
    </style>
    """
    st.markdown(bg_image, unsafe_allow_html=True)

# Call the function with your image path
set_background("C:/Users/priya/OneDrive/Desktop/FinalProject/background.png")

# Load Parkinson's Model
parkinsons_model = pickle.load(open("C:/Users/priya/OneDrive/Desktop/FinalProject/parkinsons_model.sav", 'rb'))

# Sidebar for navigation
with st.sidebar:
    selected = option_menu(
        "Parkinson's Disease Prediction System",
        ['Home', 'Parkinsons Prediction', 'About Parkinson’s Disease', 'ML Model Info', 'About us'],
        menu_icon='hospital-fill',
        icons=['house', 'activity', 'info', 'cpu', 'info-circle'],
        default_index=0
    )

# Home Page
if selected == "Home":
    st.title("🧑‍⚕️ Health Assistant")
    st.markdown("## 🌿 A Machine Learning-Based Parkinson’s Disease Prediction System")
    
    st.write("""
        Parkinson's disease is a **progressive nervous system disorder** that affects movement, speech, and overall quality of life.  
        Early diagnosis can significantly improve **treatment outcomes and symptom management**.
    """)

    st.subheader("🔍 Why is Early Detection Important?")
    st.write("""
        - There is **no cure** for Parkinson’s, but **early treatment** can help **slow down** the disease.
        - Many symptoms start subtly, so **early diagnosis is key** to managing the condition effectively.
        - Advanced AI-based tools can assist **doctors and patients** in identifying potential cases at an early stage.
    """)

    st.subheader("🛠️ How This Application Works")
    st.write("""
        - This app uses a **Machine Learning model** trained on real patient data to predict Parkinson's disease.
        - By analyzing **22 voice-related parameters**, the model can detect subtle variations linked to Parkinson’s.
        - The prediction is **quick, easy, and reliable**—just input your data and get an instant result!
    """)

    st.subheader("🚀 Get Started")
    st.write("""
        - **Go to "Parkinsons Prediction"** from the sidebar to use the ML model.
        - Learn more about **Parkinson’s disease and its symptoms** in the "About Parkinson’s Disease" section.
        - Understand how **our AI-powered model** makes predictions in the "ML Model Info" section.
    """)

    st.success("🌟 This tool is designed to assist in **early detection** and **awareness**—take the first step towards better health today!")


# Parkinson's Prediction Page
elif selected == "Parkinsons Prediction":
    st.title("🧠 Parkinson's Disease Prediction")
    st.markdown("### 🏥 Predict Parkinson’s Disease using AI & Machine Learning")

    # Step 1: Select Input Method
    st.markdown("#### ✍️ Choose Your Input Method:")
    input_method = st.radio(
        "",
        ["🔢 Enter Values One by One", "📑 Paste All Values (Comma-Separated)"],
        index=0,
        horizontal=True
    )

    input_labels = [
        'MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)', 'MDVP:Jitter(Abs)',
        'MDVP:RAP', 'MDVP:PPQ', 'Jitter:DDP', 'MDVP:Shimmer', 'MDVP:Shimmer(dB)',
        'Shimmer:APQ3', 'Shimmer:APQ5', 'MDVP:APQ', 'Shimmer:DDA', 'NHR',
        'HNR', 'RPDE', 'DFA', 'spread1', 'spread2', 'D2', 'PPE'
    ]

    user_inputs = []

    if input_method == "🔢 Enter Values One by One":
        st.markdown("#### 🔬 Enter Each Parameter Below:")
        cols = st.columns(3)  # Organizing in 3 columns for a neat look
        for index, label in enumerate(input_labels):
            with cols[index % 3]:  # Distribute inputs across columns
                user_inputs.append(st.text_input(f"📌 {label}", placeholder="Enter value..."))

    else:
        st.markdown("#### 📝 Paste Your Values Below:")
        all_values = st.text_area("📋 Enter all values (comma-separated):", placeholder="e.g., 119.99,131.31,111.12,...")
        if all_values:
            user_inputs = all_values.split(',')

    # Prediction Button with Animation
    if st.button("🔍 Predict Now", help="Click to analyze the input and predict!"):
        try:
            user_inputs = [float(x.strip()) for x in user_inputs]
            if len(user_inputs) != len(input_labels):
                st.error(f"⚠️ Please enter exactly {len(input_labels)} values.")
            else:
                with st.spinner("🤖 AI is analyzing the data..."):
                    prediction = parkinsons_model.predict([user_inputs])
                    st.success("✅ Prediction Complete!")

                # Show result with icons & color
                if prediction[0] == 0:
                    st.markdown("### 🟢 **No Parkinson’s Detected!**")
                    st.markdown("✔️ The person is **healthy** based on the input data. Keep maintaining a good lifestyle! 🎉")
                else:
                    st.markdown("### 🔴 **Parkinson’s Disease Detected!**")
                    st.error("⚠️ The model predicts a risk of Parkinson's Disease. Please consult a doctor for further analysis.")

        except ValueError:
            st.error("⚠️ Please enter valid numerical values.")


# Parkinson's Disease Information Page
elif selected == "About Parkinson’s Disease":
    st.title("ℹ️ About Parkinson’s Disease")

    with st.expander("📌 What is Parkinson’s Disease?"):
        st.write("""
            Parkinson’s disease is a **progressive nervous system disorder** that affects movement.  
            It occurs when **dopamine-producing neurons** in the brain become damaged or die.
        """)

    with st.expander("🩺 Symptoms of Parkinson’s Disease"):
        st.write("""
            Common symptoms include:
            - **Tremors** (shaking in hands or fingers)
            - **Slow movements** (bradykinesia)
            - **Muscle stiffness**
            - **Balance and posture instability**
            - **Speech and writing difficulties**
        """)

    with st.expander("🔬 How is Parkinson’s Disease Diagnosed?"):
        st.write("""
            Parkinson’s disease is **diagnosed clinically** based on symptoms.  
            Additional tests include:
            - **Neurological Examination**
            - **DaTscan** (Dopamine Transporter Scan)
            - **Speech Analysis**
            - **Machine Learning models** (like this app!) for early detection.
        """)

# ML Model Information Page
elif selected == "ML Model Info":
    st.title("🤖 Machine Learning Model Details")

    with st.expander("🧠 Model Overview"):
        st.write("""
            This application uses a **Support Vector Machine (SVM) Model** to detect Parkinson’s Disease.  
            It is trained using **frequency measurements** as input.
        """)

    with st.expander("📊 Features Used in the Model"):
        st.write("""
            - The model directly takes **frequency values** as input.
            - No additional feature extraction or preprocessing is applied.
        """)

    with st.expander("🛠️ Machine Learning Algorithm Used"):
        st.write("""
            - The model is implemented using **Support Vector Machine (SVM)**.
            - It runs locally without the need for cloud-based computation.
            - The dataset used consists of **frequency-based measurements** for Parkinson’s Disease detection.
        """)

    st.info("✅ Our ML model provides **fast and reliable** Parkinson’s Disease predictions using frequency data!")


# About Us Page
if selected == "About us":
    st.title("ℹ️ About This Application")

    st.markdown("""
        ## 🏥 Empowering Early Detection of Parkinson's Disease
        Parkinson’s disease is a **neurodegenerative disorder** that affects movement and speech.  
        This application uses **cutting-edge Machine Learning** to assist in **early detection**, which is **crucial for effective treatment**.
    """)

    st.subheader("🧠 How This AI-Powered System Works")
    st.write("""
        - The system analyzes **22 voice-related parameters** extracted from speech patterns.
        - It uses a **pre-trained ML model** to detect subtle variations associated with Parkinson’s.
        - The model was trained on real-world patient data to ensure **high accuracy and reliability**.
    """)

    st.subheader("🚀 Why Use This Application?")
    st.write("""
        - **Fast & Easy**: Just enter the required data, and get an instant prediction.
        - **AI-Driven Accuracy**: Uses advanced algorithms to analyze speech characteristics.
        - **Helps in Early Diagnosis**: Assists individuals and healthcare professionals in **identifying risks sooner**.
    """)

    st.subheader("📊 Machine Learning Model Details")
    st.write("""
        - **Model Type**: Supervised Learning (Classification)
        - **Algorithm Used**: Support Vector Machine (SVM)
        - **Training Dataset**: Publicly available dataset on Parkinson’s voice recordings
        - **Accuracy**: Over **90%** in testing
    """)

    st.success("🌟 This tool is designed to **support early detection** and raise **awareness** about Parkinson's disease!")

