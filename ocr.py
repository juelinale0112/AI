import streamlit as st
import ollama
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="Engineering Drawing OCR with Llama Vision",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description in main area
st.title("📐 Engineering Drawing OCR with Llama Vision")

# Add clear button to top right
col1, col2 = st.columns([6,1])
with col2:
    if st.button("Clear 🗑️"):
        if 'ocr_result' in st.session_state:
            del st.session_state['ocr_result']
        st.rerun()

st.markdown('<p style="margin-top: -20px;">Extract engineering labels, dimensions, and text from images using Llama Vision!</p>', unsafe_allow_html=True)

st.markdown("---")
# Move upload controls to sidebar
with st.sidebar:
    st.header("Upload Engineering Drawing Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")
        
        if st.button("Extract Engineering Info 🔍", type="primary"):
            with st.spinner("Processing image..."):
                try:
                    response = ollama.chat(
                        model='llama3.2-vision',
                        messages=[{
                            'role': 'user',
                            'content': """Analyze the engineering drawing in the provided image and extract any labels, dimensions, or text annotations.
                            Here are some guidelines you MUST follow or you will be penalized:
                            - Extract only textual information relevant to the drawing (dimensions, labels, annotations).
                            - DO NOT extract unnecessary explanations or extra information.
                            - Do NOT include any irrelevant data.
                            - Output only text relevant to engineering drawings (labels, measurements, etc.).""",
                            'images': [uploaded_file.getvalue()]
                        }]
                    )
                    st.session_state['ocr_result'] = response.message.content
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")

# Main content area for results
if 'ocr_result' in st.session_state:
    st.markdown("### Extracted Engineering Information")
    st.text_area("OCR Output", st.session_state['ocr_result'], height=300)
    
    # Optionally, you can clean up the text if there is unnecessary information
    cleaned_text = st.session_state['ocr_result'].strip()
    if cleaned_text:
        st.subheader("Cleaned Extracted Information")
        st.write(cleaned_text)
    
else:
    st.info("Upload an image and click 'Extract Engineering Info' to see the results here.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Llama Vision Model2 | [Report an Issue](https://github.com/patchy631/ai-engineering-hub/issues)")
