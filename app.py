import streamlit as st
from google import genai

# Page Configuration
st.set_page_config(
    page_title="Student AI Hub & Virtual Labs",
    page_icon="🎓",
    layout="wide"
)

# Load Custom CSS
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Configure Gemini Client using modern google-genai SDK
api_key = st.secrets.get("GEMINI_API_KEY", "")

with st.sidebar:
    st.image("https://img.icons8.com/color/96/student-male.png", width=80)
    st.title("Student Control Panel")
    if not api_key:
        api_key = st.text_input("Enter Free Gemini API Key:", type="password")
        st.markdown("[Get a free Gemini API Key from Google AI Studio](https://aistudio.google.com/)")
    
    st.markdown("---")
    app_mode = st.radio("Choose Section:", ["🤖 AI Study Tutor", "🧪 Virtual Labs", "📝 Quiz Zone"])

client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize client: {e}")

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
                    try:
                        context_prompt = f"You are an expert tutor in {subject}. Answer the student's question clearly with examples, formulas, or code snippets if necessary:\n\n{prompt}"
                        
                        # Updated to use the standard Gemini Flash model
                        response = client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=context_prompt,
                        )
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                    except Exception as e:
                        st.error(f"API Error: {e}")

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
                    try:
                        res = client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=f"Provide details about this chemical compound/reaction (molecular weight, properties, uses, safety): {compound_query}"
                        )
                        st.success(res.text)
                    except Exception as e:
                        st.error(f"API Error: {e}")
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
                try:
                    prompt = f"Create 3 multiple-choice questions for {quiz_subject} at a {difficulty} level. Include options A, B, C, D and provide the correct answers at the very bottom."
                    quiz_res = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )
                    st.session_state['current_quiz'] = quiz_res.text
                except Exception as e:
                    st.error(f"API Error: {e}")
        else:
            st.warning("Please add your API key first.")

    if 'current_quiz' in st.session_state:
        st.markdown(st.session_state['current_quiz'])
