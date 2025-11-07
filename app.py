import streamlit as st
from ats_enhancer import ATSEnhancer
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

st.set_page_config(
    page_title="ATS Resume Enhancer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

@st.cache_resource
def get_ats_enhancer(api_key):
    return ATSEnhancer(api_key=api_key)

def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {file_name}. Make sure it's in the .streamlit folder.")

load_css(".streamlit/style.css")

if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY not found.")


else:
    st.title("Bullet Points Paraphraser and Enhancer for ATS")
    st.info("This tool rewrites each bullet point to improve your ATS score and align them with the job description.")

    col1, col2 = st.columns(2)
    default_jd = '''Senior Machine Learning Engineer (AI Discovery & Recommendations).\nAbout Us: We are building the next generation of AI-driven products. Our team works on the core intelligence that shapes user experience, tackling challenges in large-scale recommendations, content understanding, and generative AI.
                    \n*The Role:* We are seeking an expert Machine Learning Engineer to design, build, and deploy the deep learning models that power our core discovery engines. You will work with petabyte-scale data and state-of-the-art infrastructure to build systems that serve billions of requests.
                    \n*What You'll Do:* Design, train, and deploy large-scale models (GNNs, Transformers, Multimodal) for our real-time recommendation and content moderation systems. \n2.Develop and optimize end-to-end production ML pipelines, from feature engineering (using Spark/Kafka) to distributed training (using PyTorch/JAX/TensorFlow).\n3.Run and analyze A/B tests to validate model improvements and their impact on user engagement.\n4.Lead technical projects and mentor junior engineers, driving best practices in code, design, and research.
                    \n*Who You Are:* 1.MS or PhD in Computer Science (or related) with a specialization in AI/ML.\n2. 5+ years of experience shipping production ML models at scale.\n3.Expert in Python, SQL, and one or more deep learning frameworks (PyTorch, TensorFlow, JAX).\n4.Proven experience with large-scale data systems (e.g., Spark, Kafka, Kubernetes, GCP/AWS).
                    \n*Bonus Points:* Experience with Graph Neural Networks (GNNs), generative models, or high-frequency feature engineering.'''
    default_resume = '''•Played a key role in developing innovative AI models that improved user engagement by 15%.
                  \n•Worked on improving model training pipelines with modern deep learning frameworks by 40%.
                  \n•Developed advanced neural network models for recommendation tasks used by 1 billion users.
                  \n•Collaborated with team members and contributed to improving code quality and model design.'''

    with col1:
        job_description = st.text_area("Job Description",value=default_jd,height=400)
    with col2:
        resume_lines = st.text_area("Resume",value=default_resume,height=400)
    if st.button("Enhance Resume", use_container_width=True):
        if not job_description or not resume_lines:
            st.warning("Please fill in both fields.")
        else:
            try:
                with st.spinner("Enhancing your points... This may take a moment."):
                    ats_enhancer = get_ats_enhancer(GOOGLE_API_KEY)
                    enhanced_points = ats_enhancer.enhance_resume(job_description=job_description,resume_lines=resume_lines)
                    enhanced_points = enhanced_points.replace("•", "\n•")
                    original_points = [line.strip() for line in resume_lines.split('\n') if line.strip()]
                    original_points_formatted = "\n".join(original_points)

                    original_scores = sum(ats_enhancer.evaluate_lines(original_points,job_description))/len(original_points) if len(original_points) > 0 else 0
                    enhanced_points_list = [line.strip() for line in enhanced_points.split('\n') if line.strip()]
                    enhanced_scores = sum(ats_enhancer.evaluate_lines(enhanced_points_list,job_description))/len(enhanced_points_list) if len(enhanced_points_list) > 0 else 0
                    st.header("Comparison of Original and Enhanced Bullet Points")
                    res_col1, res_col2 = st.columns(2)
                    with res_col1:
                        st.header("Original Bullet Points")
                        st.subheader(f"Average ATS Score - Original Bullet Points: {original_scores:.2f}/100")
                        st.text_area("Original Resume Bullet Points", value=original_points_formatted, height=400)
                    with res_col2:
                        st.header("Enhanced Bullet Points")
                        st.subheader(f"Average ATS Score - Enhanced Bullet Points: {enhanced_scores:.2f}/100")
                        st.text_area("Enhanced Resume Bullet Points", value=enhanced_points.lstrip(), height=400)
                    st.success("Enhancement complete!")
            except Exception as e:
                print(f"An exception occurred: {e}")
                st.error(f"An error occurred during enhancement: {e}")