import streamlit as st
from google import genai

# Page Configuration
st.set_page_config(
    page_title="Student AI Hub & Virtual Labs",
    page_icon="🎓",
    layout="wide"
)

# Inline Custom Styling
st.markdown("""
<style>
.main {
    background-color: #f4f7f6;
}
h1, h2, h3 {
    color: #1f2937;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.stButton>button {
    background-color: #4f46e5;
    color: white;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: 600;
    border: none;
}
.stButton>button:hover {
    background-color: #4338ca;
}
</style>
""", unsafe_allow_html=True)

# Retrieve Gemini API Key from Streamlit Secrets or Sidebar Input
api_key = st.secrets.get("GEMINI_API_KEY", "")

with st.sidebar:
    st.image("https://img.icons8.com/color/96/student-male.png", width=80)
    st.title("Student Control Panel")
    if not api_key:
        api_key = st.text_input("Enter Free Gemini API Key:", type="password")
        st.markdown("[Get a free Gemini API Key from Google AI Studio](https://aistudio.google.com/)")
    
    st.markdown("---")
    app_mode = st.radio("Choose Section:", ["🤖 AI Study Tutor", "🧪 Virtual Labs", "📝 Quiz Zone"])

# Initialize Modern GenAI Client
client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize client: {e}")

# Robust generation function handling model fallbacks
def generate_response(prompt_text):
    if not client:
        return "Error: API client not initialized. Please enter your API key."
    
    # Modern available flash models
    models_to_try = ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-1.5-flash"]
    for m in models_to_try:
        try:
            response = client.models.generate_content(
                model=m,
                contents=prompt_text,
            )
            return response.text
        except Exception:
            continue
            
    return "Error: All models are currently unavailable or busy. Please try again shortly."

# --- SECTION 1: AI STUDY TUTOR ---
if app_mode == "🤖 AI Study Tutor":
    st.title("🤖 AI Subject Expert Tutor")
    st.write("Ask any question related to **Physics, Chemistry, Computer Science, or Mathematics**!")

    subject = st.selectbox("Select Subject", ["General / All Subjects", "Physics", "Chemistry", "Computer Science", "Mathematics"])
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is your question?"):
        if not client:
            st.error("Please provide your Gemini API key in the sidebar first!")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    context_prompt = f"You are an expert tutor in {subject}. Answer the student's question clearly with examples, formulas, or code snippets if necessary:\n\n{prompt}"
                    answer = generate_response(context_prompt)
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})

# --- SECTION 2: VIRTUAL LABS ---
elif app_mode == "🧪 Virtual Labs":
    st.title("🧪 Interactive Virtual Labs")
    st.write("Perform simulated experiments and coding sandboxes right in your browser.")

    lab_tab = st.tabs(["⚡ Physics Lab", "🔬 Chemistry Lab", "💻 Computer Lab"])

    with lab_tab[0]:
        st.subheader("Physics Lab: Ohm's Law Calculator & Simulator")
        st.markdown("Test the relationship between Voltage ($V$), Current ($I$), and Resistance ($R$). Formula: $V = I \\times R$")
        
        col1, col2 = st.columns(2)
        with col1:
            voltage = st.slider("Voltage (Volts)", 1.0, 50.0, 12.0)
            resistance = st.slider("Resistance (Ohms)", 1.0, 100.0, 10.0)
        with col2:
            current = voltage / resistance
            st.metric(label="Calculated Current (Amperes)", value=f"{current:.2f} A")
            st.info("💡 Try increasing resistance to see current drop!")

    with lab_tab[1]:
        st.subheader("Chemistry Lab: Reaction & Compound Analyzer")
        compound_query = st.text_input("Enter a chemical formula or reaction (e.g., H2O, NaCl, Photosynthesis):")
        if st.button("Analyze Compound"):
            if client and compound_query:
                with st.spinner("Analyzing chemical properties..."):
                    ans = generate_response(f"Provide details about this chemical compound/reaction (molecular weight, properties, uses, safety): {compound_query}")
                    st.success(ans)
            else:
                st.warning("Please enter a query and ensure your API key is active.")

    with lab_tab[2]:
        st.subheader("Computer Lab: Python Code Sandbox")
        code_snippet = st.text_area("Write Python code to test logic:", "print('Hello, Student!')")
        if st.button("Run Code"):
            try:
                local_vars = {}
                exec(code_snippet, {}, local_vars)
            except Exception as e:
                st.error(f"Error: {e}")

# --- SECTION 3: QUIZ ZONE ---
elif app_mode == "📝 Quiz Zone":
    st.title("📝 Student Practice Quiz")
    st.write("Test your knowledge and get instant AI feedback!")

    quiz_subject = st.selectbox("Select Quiz Subject", ["Physics", "Chemistry", "Computer Science", "Mathematics"])
    difficulty = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])

    if st.button("Generate Quiz"):
        if client:
            with st.spinner("Generating custom quiz..."):
                prompt = f"Create 3 multiple-choice questions for {quiz_subject} at a {difficulty} level. Include options A, B, C, D and provide the correct answers at the very bottom."
                quiz_text = generate_response(prompt)
                st.session_state['current_quiz'] = quiz_text
        else:
            st.warning("Please add your API key first.")

    if 'current_quiz' in st.session_state:
        st.markdown(st.session_state['current_quiz'])
