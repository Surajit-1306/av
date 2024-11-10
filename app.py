import streamlit as st
from utils import format_filters
from update_course_list import update_course_details
from chroma_utils import CourseKnowledgeBase
from llm_utils import get_response
import logging

logging.basicConfig(filename='app.log', filemode='a', level=logging.INFO, \
                    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(lineno)d- %(message)s')
# Setup logger
logger = logging.getLogger(__name__)


# Dictionary of questions
questions = {
    "current_role_or_field": "What is your current role or field of study? (e.g., software developer, data scientist, student)",
    "experience_level": "How would you describe your experience level in AI and machine learning? (Beginner, Intermediate, Advanced)",
    "learning_interests": "What topics are you most interested in learning about? (e.g., NLP, multilingual AI, reinforcement learning, financial modeling, etc.)",
    "preferred_learning_style": "Do you prefer hands-on projects, theoretical knowledge, or a mix of both?",
    "career_goals": "How do you plan to use the skills you learn from the course? (e.g., advancing in current job, career switch, starting a new project)"
}



# Streamlit app with a form
st.title("Course Recommendation System")

# Sidebar option to update course details
if st.sidebar.button("Update Course Details"):
    st.sidebar.write("Updating course details...")
    course_data = update_course_details()
    logger.info(f"Course details: {course_data}")

    knowledge_base = CourseKnowledgeBase()
    # Insert new course details
    knowledge_base.insert_courses(course_data)
    st.sidebar.write("Course details updated successfully!")

with st.form("user_input_form"):
    st.write("Please fill out the form below to help us recommend the best courses for you.")

    # Input fields for each question
    current_role_or_field = st.text_input(questions["current_role_or_field"])
    experience_level = st.selectbox(questions["experience_level"], ["Beginner", "Intermediate", "Advanced"])
    learning_interests = st.text_input(questions["learning_interests"])
    preferred_learning_style = st.selectbox(questions["preferred_learning_style"], ["Hands-on projects", "Theoretical knowledge", "Mix of both"])
    career_goals = st.text_area(questions["career_goals"])

    # Submit button
    submitted = st.form_submit_button("Submit")

    # Process the form data after submission
    if submitted:
        # Collect responses in a dictionary
        filters = {
            "current_role_or_field": current_role_or_field,
            "experience_level": experience_level,
            "learning_interests": learning_interests,
            "preferred_learning_style": preferred_learning_style,
            "career_goals": career_goals
        }
        
        # Format the dictionary into a string
        formatted_string = format_filters(filters)
        
        results = get_response(formatted_string)
        
        # Display the results
        st.write("### Recommended Courses")
        for course in reversed(results['courses']):
            st.markdown(f"**Title:** {course['title']}")
            st.markdown(f"**Relevance:** {float(course['relevance'])*100}%")
            st.markdown(f"**Summary:** {course['summary']}")
            st.markdown(f"[Apply Link]({course['apply_link']})")
            st.markdown("---")