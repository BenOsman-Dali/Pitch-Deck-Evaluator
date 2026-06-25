import streamlit as st
from pypdf import PdfReader
from groq import Groq

# Page configuration
st.set_page_config(page_title="AI Pitch Deck Evaluator", page_icon="🤖")

st.title("AI Pitch Deck Evaluator")
st.write("Upload your pitch deck PDF and get feedback like a real VC investor")

# Sidebar for API key
with st.sidebar:
    st.header("API Key")
    api_key = st.text_input("Enter your Groq API Key:", type="password")
    st.markdown("[Get your free Groq API key here](https://console.groq.com)")
    
    if api_key:
        st.success("API Key set!")

# File upload
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Function to evaluate using Groq (FREE)
def evaluate_pitch_deck(text):
    prompt = f"""
You are a professional venture capitalist investor with 20 years of experience. 
You've reviewed thousands of pitch decks and invested in dozens of successful startups.
You are tough, honest, and look for venture-scale opportunities.

Analyze this pitch deck and provide feedback in EXACTLY these sections:

**1. INVESTOR COMMUNICATION & CLARITY (Score 0-10)**
- Check for grammar, spelling, and professionalism
- Is the language clear and concise?
- Are slides overloaded with text?
- Provide specific examples of what's good and what needs improvement

**2. NARRATIVE & STORYTELLING (Score 0-10)**
- Does it follow the standard structure: Problem → Solution → Product → Market → Business Model → Team?
- Is the story logical and compelling?
- Are there missing or weak sections?
- Does it build a convincing investment case?

**3. PROBLEM-SOLUTION FIT (Score 0-10)**
- Is the problem clearly defined and painful?
- Does the solution directly and logically solve the problem?
- Is this a venture-scale opportunity worth investing in?

**4. INVESTOR INSIGHTS & THESIS**
- What is the single biggest reason an investor would say YES to this deal?
- What is the single biggest reason an investor would say NO?
- What is the core investment thesis here?
- How does this fit into a venture capital portfolio?

**5. TOP 3 STRENGTHS** (Specific things that impressed you)

**6. TOP 3 WEAKNESSES** (Specific things that need work)

**7. TOP 3 INVESTOR RISKS** (What concerns you as an investor)

**8. OVERALL VERDICT** (Would you invest? Why or why not?)

Pitch deck text:
{text[:8000]}

Format your response with clear headings and bullet points. Be specific and actionable.
"""
    
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Initialize session state for sample text
if 'sample_text' not in st.session_state:
    st.session_state.sample_text = ""

# Quick Test Section
st.divider()
st.subheader("Quick Test (No PDF Needed)")

if st.button("Load Sample Pitch Deck"):
    st.session_state.sample_text = """
Company Name: TechFlow Automation

The Problem:
Small businesses waste 20+ hours per week on manual data entry and invoice processing. 
This costs the US economy $50 billion annually in lost productivity.

Our Solution:
AI-powered automation software that extracts data from invoices, receipts, and documents 
with 99% accuracy. Saves businesses 15 hours per week per employee.

Market Size:
Total Addressable Market: $50 billion
Serviceable Addressable Market: $15 billion
Target Market: 2 million US small businesses

Business Model:
SaaS subscription - $99/month per user
Average customer has 5 users = $495/month
Current customers: 500

Traction:
- $50,000 MRR
- 20% month-over-month growth
- 4.9/5 star rating on G2
- Featured in TechCrunch

Competition:
- Competitor A: Limited to invoicing only
- Competitor B: Expensive enterprise solution
- Our Advantage: All-in-one platform at 1/3 the cost

Team:
- CEO: John Smith - Ex-Google, Stanford MBA
- CTO: Jane Doe - Ex-Microsoft, 10 patents
- Head of Sales: Bob Johnson - Scaled 2 startups to $10M ARR

The Ask:
Seeking $2.5M seed round to expand engineering and sales teams.
"""
    st.success("Sample pitch deck loaded! Scroll down to the 'Paste Text' section and click Evaluate.")

# If file uploaded
if uploaded_file is not None:
    with st.spinner("Reading your pitch deck..."):
        try:
            pdf_reader = PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            text = ""
    
    if text.strip():
        st.success(f"PDF uploaded successfully! Extracted {len(text)} characters of text")
        
        with st.expander("Preview extracted text"):
            st.write(text[:1000])
        
        if st.button("Evaluate My Pitch Deck"):
            if not api_key:
                st.error("Please enter your Groq API key in the sidebar first!")
            else:
                with st.spinner("Analyzing your pitch deck like a real VC investor..."):
                    feedback = evaluate_pitch_deck(text)
                    
                    st.divider()
                    st.header("Evaluation Results")
                    st.markdown(feedback)
                    
                    st.download_button(
                        label="Download Evaluation Report",
                        data=feedback,
                        file_name="pitch_deck_evaluation.txt",
                        mime="text/plain"
                    )
    else:
        st.warning("No text could be extracted from this PDF. Please use the 'Paste Text' option below.")

# Text input section (always visible)
st.divider()
st.subheader("Or paste your pitch deck text directly")

# Auto-fill with sample text if loaded
if st.session_state.sample_text:
    manual_text = st.text_area("Paste your pitch deck text here:", value=st.session_state.sample_text, height=200)
else:
    manual_text = st.text_area("Paste your pitch deck text here:", height=200)

if st.button("Evaluate Pasted Text"):
    if not api_key:
        st.error("Please enter your Groq API key in the sidebar first!")
    elif manual_text.strip():
        with st.spinner("Analyzing your pitch deck like a real VC investor..."):
            feedback = evaluate_pitch_deck(manual_text)
            st.divider()
            st.header("Evaluation Results")
            st.markdown(feedback)
    else:
        st.error("Please paste some text first!")

# Footer
st.divider()
st.caption("Built for V3 Factory Internship Challenge | AI Pitch Deck Evaluator")