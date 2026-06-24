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

**4. INVESTOR INSIGHTS & THESIS (Crucial - New Section)**
- What is the single biggest reason an investor would say YES to this deal?
- What is the single biggest reason an investor would say NO?
- What is the core investment thesis here? (e.g., "Betting on the team's execution in a massive market")
- How does this fit into a venture capital portfolio? (High-risk/high-reward? Safe bet? Niche player?)

**5. TOP 3 STRENGTHS** (Specific things that impressed you)

**6. TOP 3 WEAKNESSES** (Specific things that need work)

**7. TOP 3 INVESTOR RISKS** (What concerns you as an investor)

**8. OVERALL VERDICT** (Would you invest? Why or why not? What would make you say YES?)

Pitch deck text:
{text[:8000]}

Format your response with clear headings and bullet points. Be specific and actionable. Make sure the INVESTOR INSIGHTS section is distinct and insightful.
"""
    
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Free, powerful model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2500  # Increased for the new section
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# If file uploaded
if uploaded_file is not None:
    # Read the PDF using pypdf
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
        
        # Show a preview
        with st.expander("Preview extracted text"):
            st.write(text[:1000])
        
        # Show full text for debugging
        with st.expander("Full extracted text (for debugging)"):
            st.text(text[:5000])
        
        # Evaluate button
        if st.button("Evaluate My Pitch Deck"):
            if not api_key:
                st.error("Please enter your Groq API key in the sidebar first!")
            else:
                with st.spinner("Analyzing your pitch deck like a real VC investor..."):
                    feedback = evaluate_pitch_deck(text)
                    
                    # Display results
                    st.divider()
                    st.header("Evaluation Results")
                    st.markdown(feedback)
                    
                    # Download button for results
                    st.download_button(
                        label="Download Evaluation Report",
                        data=feedback,
                        file_name="pitch_deck_evaluation.txt",
                        mime="text/plain"
                    )
    else:
        st.warning("No text could be extracted from this PDF. The file may be image-based or scanned. Please upload a PDF with selectable text.")
        
        # Add a text input option as backup
        st.divider()
        st.subheader("Or paste your pitch deck text directly")
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