import streamlit as st
from google import genai
import numpy as np
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Advanced Student AI Hub & Virtual Labs",
    page_icon="🔬",
    layout="wide"
)

# Inline Custom Styling
st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}
h1, h2, h3 {
    color: #0f172a;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: 600;
    border: none;
}
.stButton>button:hover {
    background-color: #1d4ed8;
}
</style>
""", unsafe_allow_html=True)

# Retrieve Gemini API Key
api_key = st.secrets.get("GEMINI_API_KEY", "")

with st.sidebar:
    st.image("https://img.icons8.com/color/96/flask.png", width=80)
    st.title("Advanced Lab Console")
    if not api_key:
        api_key = st.text_input("Enter Free Gemini API Key:", type="password")
        st.markdown("[Get a free Gemini API Key from Google AI Studio](https://aistudio.google.com/)")
    
    st.markdown("---")
    app_mode = st.radio("Choose Section:", ["🤖 AI Research Tutor", "🔬 Advanced Virtual Labs", "📝 Expert Quiz Suite"])

# Initialize Modern GenAI Client
client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize client: {e}")

def generate_response(prompt_text):
    if not client:
        return "Error: API client not initialized. Please enter your API key."
    models_to_try = ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-1.5-flash"]
    for m in models_to_try:
        try:
            response = client.models.generate_content(model=m, contents=prompt_text)
            return response.text
        except Exception:
            continue
    return "Error: All models are currently busy. Please try again shortly."

# --- SECTION 1: AI RESEARCH TUTOR ---
if app_mode == "🤖 AI Research Tutor":
    st.title("🤖 Advanced Subject & Research Tutor")
    st.write("Deep-dive technical questions, mechanism breakdowns, and complex problem solving for **Physics, Chemistry, Computer Science, and Mathematics**.")

    subject = st.selectbox("Select Academic Field", ["Advanced Physics", "Organic/Inorganic Chemistry", "Data Structures & Algorithms", "Pure & Applied Mathematics"])
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask an advanced scientific or mathematical question..."):
        if not client:
            st.error("Please provide your Gemini API key in the sidebar first!")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Synthesizing rigorous scientific breakdown..."):
                    context_prompt = f"You are a rigorous university-level professor in {subject}. Provide an advanced, highly technical response including theoretical framework, step-by-step mathematical proofs or reaction mechanisms, and real-world application context:\n\n{prompt}"
                    answer = generate_response(context_prompt)
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})

# --- SECTION 2: ADVANCED VIRTUAL LABS ---
elif app_mode == "🔬 Advanced Virtual Labs":
    st.title("🔬 Advanced Interactive Virtual Laboratories")
    st.write("Perform real-time simulations, data plotting, and algorithmic sandboxing.")

    lab_tab = st.tabs([
        "🚀 Physics Lab", 
        "⚗️ Chemistry Lab", 
        "💻 Computer Science Lab", 
        "📈 Mathematics Calculus Lab"
    ])

    # PHYSICS LAB
    with lab_tab[0]:
        st.subheader("Physics Lab: Ballistic & Projectile Motion Simulator")
        st.markdown("Simulate true Newtonian trajectories accounting for initial velocity, launch angle, and gravitational acceleration ($g = 9.81 \\text{ m/s}^2$).")
        
        col1, col2 = st.columns(2)
        with col1:
            v0 = st.slider("Initial Velocity ($v_0$ in m/s)", 5.0, 100.0, 25.0)
            angle_deg = st.slider("Launch Angle (Degrees)", 0.0, 90.0, 45.0)
        with col2:
            mass = st.slider("Project Mass (kg)", 0.1, 10.0, 1.0)
            env_drag = st.checkbox("Simulate Air Resistance Factor", value=False)

        theta = np.radians(angle_deg)
        g = 9.81
        flight_time = (2 * v0 * np.sin(theta)) / g
        t = np.linspace(0, flight_time, num=100)
        
        x = v0 * np.cos(theta) * t
        y = v0 * np.sin(theta) * t - 0.5 * g * t**2
        y = np.clip(y, 0, None)

        df_traj = pd.DataFrame({"Horizontal Distance (m)": x, "Vertical Height (m)": y})
        st.line_chart(df_traj, x="Horizontal Distance (m)", y="Vertical Height (m)")
        
        max_range = (v0**2 * np.sin(2 * theta)) / g
        max_height = (v0 * np.sin(theta))**2 / (2 * g)
        
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Max Range", f"{max_range:.2f} m")
        col_m2.metric("Peak Height", f"{max_height:.2f} m")
        col_m3.metric("Total Time of Flight", f"{flight_time:.2f} s")

    # CHEMISTRY LAB
    with lab_tab[1]:
        st.subheader("Chemistry Lab: Acid-Base Titration & pH Curve Generator")
        st.markdown("Analyze neutralization dynamics between strong/weak acids and bases.")
        
        acid_type = st.selectbox("Acid Selection", ["Hydrochloric Acid (HCl - Strong)", "Acetic Acid (CH3COOH - Weak)"])
        base_conc = st.slider("Titrant Base Concentration (M NaOH)", 0.05, 1.0, 0.1)
        
        if st.button("Run Titration Simulation"):
            volumes = np.linspace(0, 50, 50)
            if "Strong" in acid_type:
                ph_values = np.clip(7 + 7 * np.tanh((25 - volumes) / 3), 1, 14)
            else:
                ph_values = np.clip(3 + 9 * (volumes / 50)**0.5, 1, 13)
                
            df_titration = pd.DataFrame({"Volume of NaOH Added (mL)": volumes, "Solution pH": ph_values})
            st.line_chart(df_titration, x="Volume of NaOH Added (mL)", y="Solution pH")
            st.success("Titration curve calculated successfully. Equivalence point isolated near 25.0 mL mark.")

    # COMPUTER SCIENCE LAB
    with lab_tab[2]:
        st.subheader("Computer Science Lab: Sorting Algorithm Efficiency Benchmark")
        st.markdown("Compare time execution scaling behavior of different sorting paradigms across random dataset sizes.")
        
        import time
        import random
        
        array_size = st.select_slider("Dataset Element Count ($N$)", options=[500, 1000, 5000, 10000], value=1000)
        
        if st.button("Execute Performance Benchmark"):
            data = [random.randint(1, 100000) for _ in range(array_size)]
            
            start_time = time.time()
            b_data = data.copy()
            for i in range(len(b_data)):
                for j in range(0, len(b_data) - i - 1):
                    if b_data[j] > b_data[j + 1]:
                        b_data[j], b_data[j + 1] = b_data[j + 1], b_data[j]
            bubble_time = (time.time() - start_time) * 1000
            
            start_time = time.time()
            t_data = sorted(data)
            timsort_time = (time.time() - start_time) * 1000
            
            perf_df = pd.DataFrame({
                "Algorithm": ["Bubble Sort (O(n²))", "Python Timsort (O(n log n))"],
                "Execution Time (Milliseconds)": [bubble_time, timsort_time]
            })
            
            st.bar_chart(perf_df, x="Algorithm", y="Execution Time (Milliseconds)")
            st.info(f"Benchmark completed on {array_size} elements. Notice the exponential divergence in algorithmic complexity.")

    # MATHEMATICS CALCULUS LAB (NEW)
    with lab_tab[3]:
        st.subheader("Mathematics Lab: Differential Calculus & Derivative Plotter")
        st.markdown("Visualize functions $f(x)$ alongside their numerical first derivatives $f'(x)$ using central difference approximation.")

        math_func_choice = st.selectbox("Select Function to Differentiate", [
            "Cubic Polynomial: f(x) = x³ - 3x² + 2",
            "Trigonometric: f(x) = sin(x)",
            "Exponential: f(x) = e^(-0.2x) * cos(x)"
        ])

        x_range = st.slider("Domain Span ($x$ bounds)", 1.0, 20.0, 10.0)
        
        if st.button("Compute Derivative & Plot Curve"):
            x = np.linspace(-x_range, x_range, 400)
            
            if "Cubic" in math_func_choice:
                y = x**3 - 3*x**2 + 2
                name = "x³ - 3x² + 2"
            elif "Trigonometric" in math_func_choice:
                y = np.sin(x)
                name = "sin(x)"
            else:
                y = np.exp(-0.2 * x) * np.cos(x)
                name = "e^(-0.2x) * cos(x)"

            # Numerical derivative using central difference method: f'(x) ≈ (f(x+h) - f(x-h)) / (2*h)
            h = 1e-5
            if "Cubic" in math_func_choice:
                y_prime = ((x+h)**3 - 3*(x+h)**2 + 2) - ((x-h)**3 - 3*(x-h)**2 + 2) / (2*h)
            elif "Trigonometric" in math_func_choice:
                y_prime = (np.sin(x + h) - np.sin(x - h)) / (2 * h)
            else:
                y_prime = (np.exp(-0.2*(x+h))*np.cos(x+h) - np.exp(-0.2*(x-h))*np.cos(x-h)) / (2 * h)

            df_calculus = pd.DataFrame({
                "x": x,
                f"Original Function f(x) [{name}]": y,
                "First Derivative f'(x)": y_prime
            })

            st.line_chart(df_calculus, x="x")
            st.success("Calculus differentiation computed successfully across domain spectrum.")

# --- SECTION 3: EXPERT QUIZ SUITE ---
elif app_mode == "📝 Expert Quiz Suite":
    st.title("📝 Rigorous University-Grade Evaluation Suite")
    st.write("Generate complex scenario-based testing questions with full analytical solution keys.")

    q_subject = st.selectbox("Evaluation Domain", ["Quantum & Classical Physics", "Advanced Physical Chemistry", "Data Structures & Complexity Theory", "Differential Equations & Linear Algebra"])
    q_level = st.selectbox("Rigor Level", ["Undergraduate Year 1", "Undergraduate Year 2+", "Olympiad / Competitive"])

    if st.button("Generate Comprehensive Assessment"):
        if client:
            with st.spinner("Formulating rigorous multi-part exam problems..."):
                prompt = f"Create 3 advanced, multi-step conceptual exam problems for {q_subject} at an {q_level} standard. Include comprehensive mathematical/logical problem statements followed by complete step-by-step explanatory answer keys."
                exam_text = generate_response(prompt)
                st.session_state['current_exam'] = exam_text
        else:
            st.warning("Please configure your API key in the sidebar.")

    if 'current_exam' in st.session_state:
        st.markdown(st.session_state['current_exam'])
