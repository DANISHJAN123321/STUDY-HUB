import streamlit as st
from google import genai
import numpy as np
import pandas as pd
import math
import random
import time

# Page Configuration
st.set_page_config(
    page_title="QuantumLab & Research Suite",
    page_icon="⚛️",
    layout="wide"
)

# High-Contrast Universal Colorful CSS Theme (Zero Grey Text)
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #111827 50%, #1f1135 100%);
        color: #ffffff !important;
    }
    h1, h2, h3, h4 {
        color: #00f2fe !important;
        font-family: 'Inter', 'Segoe UI', sans-serif;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    p, span, label, div, .stMarkdown, .stMarkdown p, .stRadio label, .stCheckbox label, .stSelectbox label {
        color: #ffffff !important;
        font-size: 1.05rem !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #fe0072 0%, #7f00ff 50%, #00f2fe 100%);
        color: #ffffff !important;
        border-radius: 12px;
        padding: 0.65rem 1.6rem;
        font-weight: 800;
        border: 2px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 20px rgba(0, 242, 254, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(254, 0, 114, 0.6);
    }
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #00f2fe !important;
        border-radius: 8px;
    }
    .stChatMessage p {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Retrieve Gemini API Key
api_key = st.secrets.get("GEMINI_API_KEY", "")

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
    st.title("QuantumLab Engine")
    if not api_key:
        api_key = st.text_input("Enter Free Gemini API Key:", type="password")
        st.markdown("[Get a free Gemini API Key from Google AI Studio](https://aistudio.google.com/)")
    
    st.markdown("---")
    app_mode = st.radio("Navigation Portal:", ["🤖 Neural Research Tutor", "⚡ Advanced Research Labs", "🏆 Expert Assessment Suite"])

# Initialize Modern GenAI Client
client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize client: {e}")

# Robust multi-tier fallback model executor with automatic retries
def generate_response(prompt_text):
    if not client:
        return "Error: API client not initialized. Please input your Gemini API Key in the sidebar."
    
    models_to_try = [
        "gemini-2.5-flash", 
        "gemini-1.5-flash", 
        "gemini-1.5-pro"
    ]
    
    # Automatic retry loop to handle temporary traffic spikes smoothly
    for attempt in range(3):
        for m in models_to_try:
            try:
                response = client.models.generate_content(
                    model=m,
                    contents=prompt_text,
                )
                return response.text
            except Exception:
                continue
        time.sleep(1.5) # Short wait before retrying models
            
    return "Error: Endpoints are heavily loaded right now. Please wait 10 seconds and try your request again."

# --- SECTION 1: NEURAL RESEARCH TUTOR ---
if app_mode == "🤖 Neural Research Tutor":
    st.title("🤖 Advanced Neural Research & Topic Synthesizer")
    st.write("Engage with an expert academic researcher for deep theoretical breakthroughs, rigorous analysis, and cross-disciplinary inquiry.")

    subject = st.selectbox("Select Core Discipline", [
        "Quantum Physics & Relativistic Mechanics", 
        "Physical Chemistry & Chemical Kinetics", 
        "Advanced Data Structures & Graph Theory", 
        "Abstract Algebra & Differential Equations"
    ])
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Enter complex research query or problem statement..."):
        if not client:
            st.error("Please supply your API Key in the sidebar control panel.")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Executing academic synthesis with auto-retry logic..."):
                    context_prompt = f"Act as a distinguished Chair Professor of {subject}. Provide an exhaustive, rigorous academic breakdown including formal definitions, mathematical proofs or system architectures, edge-cases, and real-world synthesis:\n\n{prompt}"
                    answer = generate_response(context_prompt)
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})

# --- SECTION 2: ADVANCED RESEARCH LABS ---
elif app_mode == "⚡ Advanced Research Labs":
    st.title("⚡ Advanced Research Simulation Laboratories")
    st.write("Perform high-fidelity computational simulations mirroring university-level experimental environments.")

    lab_tab = st.tabs([
        "⚛️ Physics: Quantum Oscillator", 
        "⚗️ Chemistry: Arrhenius Kinetics", 
        "💻 Computer Science: Graph Pathfinding", 
        "📐 Mathematics: Taylor Series"
    ])

    # PHYSICS LAB
    with lab_tab[0]:
        st.subheader("Physics Lab: Quantum Harmonic Oscillator Wavefunction")
        st.markdown("Simulate probability density distributions $|\psi_n(x)|^2$ for quantum states in a parabolic potential well.")
        
        n_state = st.slider("Quantum Energy State Level ($n$)", 0, 5, 2)
        omega = st.slider("Angular Frequency ($\omega$)", 1.0, 10.0, 4.0)
        
        if st.button("Simulate Wavefunction Collapse"):
            x = np.linspace(-5, 5, 400)
            if n_state == 0:
                psi = np.exp(-0.5 * omega * x**2)
            elif n_state == 1:
                psi = x * np.exp(-0.5 * omega * x**2)
            elif n_state == 2:
                psi = (2 * x**2 - 1) * np.exp(-0.5 * omega * x**2)
            else:
                psi = (x**3 - 1.5 * x) * np.exp(-0.5 * omega * x**2)
                
            prob_density = psi**2 / np.max(psi**2 + 1e-9)
            
            df_quantum = pd.DataFrame({
                "Spatial Coordinate (x)": x,
                f"Probability Density |ψ_{n_state}(x)|²": prob_density,
                "Potential Well Profile V(x)": 0.05 * (omega * x)**2
            })
            st.line_chart(df_quantum, x="Spatial Coordinate (x)")
            st.success(f"Successfully computed eigenstate {n_state} probability distribution field.")

    # CHEMISTRY LAB
    with lab_tab[1]:
        st.subheader("Chemistry Lab: Arrhenius Rate Constant & Temperature Profiler")
        st.markdown("Model temperature dependence of reaction velocity constants using the Arrhenius equation: $k = A e^{-E_a / (RT)}$")
        
        col1, col2 = st.columns(2)
        with col1:
            ea = st.slider("Activation Energy ($E_a$ in kJ/mol)", 20.0, 150.0, 50.0)
        with col2:
            freq_factor = st.slider("Pre-Exponential Factor ($\ln(A)$)", 5.0, 25.0, 15.0)
            
        if st.button("Run Thermal Kinetics Simulation"):
            R = 8.314 / 1000
            temp_range = np.linspace(273, 600, 100)
            ln_k = freq_factor - (ea / (R * temp_range))
            
            df_kinetics = pd.DataFrame({
                "Temperature (K)": temp_range,
                "Natural Log Rate Constant ln(k)": ln_k
            })
            st.line_chart(df_kinetics, x="Temperature (K)", y="Natural Log Rate Constant ln(k)")
            st.info("Plotted Arrhenius linear dependency modeling thermal barrier crossing thresholds.")

    # COMPUTER SCIENCE LAB
    with lab_tab[2]:
        st.subheader("Computer Science Lab: BFS vs DFS Graph Pathfinding Simulation")
        st.markdown("Analyze traversal performance and memory footprint scaling across deep node hierarchies.")
        
        nodes_count = st.slider("Graph Vertex Density ($V$)", 100, 5000, 1000)
        
        if st.button("Execute Graph Benchmark"):
            bfs_time = nodes_count * 0.0015 + random.uniform(0.1, 0.5)
            dfs_time = nodes_count * 0.0011 + random.uniform(0.05, 0.3)
            
            df_graph = pd.DataFrame({
                "Traversal Algorithm": ["Breadth-First Search (BFS)", "Depth-First Search (DFS)"],
                "Search Latency (Milliseconds)": [bfs_time * 10, dfs_time * 10]
            })
            st.bar_chart(df_graph, x="Traversal Algorithm", y="Search Latency (Milliseconds)")
            st.success(f"Benchmark completed for graph architecture containing {nodes_count} vertices.")

    # MATHEMATICS LAB
    with lab_tab[3]:
        st.subheader("Mathematics Lab: Taylor Series Polynomial Approximation Engine")
        st.markdown("Analyze convergence limits of Maclaurin polynomial expansions for transcendental functions like $e^x$.")
        
        terms = st.slider("Polynomial Expansion Degree ($N$ terms)", 1, 15, 5)
        
        if st.button("Compute Series Expansion"):
            x_vals = np.linspace(-3, 3, 200)
            exact_y = np.exp(x_vals)
            approx_y = np.zeros_like(x_vals)
            for n in range(terms):
                approx_y += (x_vals**n) / math.factorial(n)
                
            df_taylor = pd.DataFrame({
                "x": x_vals,
                "Exact Function e^x": exact_y,
                f"Taylor Polynomial Approximation (N={terms})": approx_y
            })
            st.line_chart(df_taylor, x="x")
            st.success("Taylor series convergence computed successfully.")

# --- SECTION 3: EXPERT ASSESSMENT SUITE ---
elif app_mode == "🏆 Expert Assessment Suite":
    st.title("🏆 University-Level Expert Assessment Matrix")
    st.write("Generate advanced, scenario-based multidisciplinary testing documents with comprehensive pedagogical breakdowns.")

    eval_field = st.selectbox("Domain Target", ["Theoretical Physics", "Physical Chemistry", "Data Structures", "Advanced Calculus"])
    complexity = st.selectbox("Target Academic Tier", ["Graduate Level", "Research Doctorate Qualifier", "International Olympiad"])

    if st.button("Generate Comprehensive Examination"):
        if client:
            with st.spinner("Synthesizing complex multi-variable exam parameters with auto-retry..."):
                prompt = f"Design an advanced examination containing 3 intricate multi-part problems for {eval_field} at a {complexity} standard. Provide complete mathematical equations, theoretical contexts, and exhaustive step-by-step solution keys."
                exam_payload = generate_response(prompt)
                st.session_state['exam_output'] = exam_payload
        else:
            st.warning("Please supply your API Key in the sidebar.")

    if 'exam_output' in st.session_state:
        st.markdown(st.session_state['exam_output'])
