import streamlit as st
import streamlit.components.v1 as components
from scraper import fetch_website_contents
from summarizer import summarize
import time
from fpdf import FPDF

# --- Initialize session state ---
if "history" not in st.session_state:
    st.session_state.history = []

if "metrics" not in st.session_state:
    st.session_state.metrics = None

# --- Create PDF from text ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # remove unsupported unicode chars
    clean_text = text.encode("latin-1", "ignore").decode("latin-1")

    for line in clean_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    return pdf.output(dest="S").encode("latin-1")

# --- Page setup ---
st.set_page_config(page_title="Website Summarizer AI", layout="wide")

st.title("🌐 Website Summarizer AI")

# --- User inputs ---
url = st.text_input("Enter website URL")

style = st.selectbox(
    "Choose summary style",
    ["Short", "Detailed", "Bullet Points", "Beginner Friendly"]
)

custom = st.text_input(
    "Optional instruction",
    placeholder="e.g., make it funny, focus on key points..."
)

# --- Generate summary ---
if st.button("Summarize"):
    if url:
        start_time = time.time()

        with st.spinner("Processing..."):
            content = fetch_website_contents(url)
            summary = summarize(content, style, custom)

        end_time = time.time()

        # compute metrics
        original_len = len(content)
        summary_len = len(summary)
        compression = round((summary_len / original_len) * 100, 2)
        processing_time = round(end_time - start_time, 2)

        # store metrics annd history
        st.session_state.metrics = {
            "original_len": original_len,
            "summary_len": summary_len,
            "compression": compression,
            "processing_time": processing_time
        }

        st.session_state.history.append({
            "url": url,
            "summary": summary
        })

        # --- Output layout ---
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Summary")
            st.markdown(summary)

            # download options
            st.download_button(
                "📄 Download as TXT",
                data=summary,
                file_name="summary.txt",
                mime="text/plain"
            )

            pdf_data = create_pdf(summary)

            st.download_button(
                "📕 Download as PDF",
                data=pdf_data,
                file_name="summary.pdf",
                mime="application/pdf"
            )

        with col2:
            st.subheader("Preview")
            components.iframe(url, height=500, scrolling=True)

    else:
        st.warning("Enter a URL")

# --- Metrics display ---
if st.session_state.metrics:
    st.subheader("📊 Analysis")

    colA, colB, colC, colD = st.columns(4)

    colA.metric("Original Length", st.session_state.metrics["original_len"])
    colB.metric("Summary Length", st.session_state.metrics["summary_len"])
    colC.metric("Compression %", f"{st.session_state.metrics['compression']}%")
    colD.metric("Time Taken", f"{st.session_state.metrics['processing_time']}s")

# --- History section ---
st.divider()
st.subheader("🕘 History")

if st.session_state.history:
    for i, item in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"{i}. {item['url']}"):
            st.markdown(item["summary"])
else:
    st.write("No history yet.")

# --- Clear history ---
if st.button("Clear History"):
    st.session_state.history = []
    st.session_state.metrics = None
