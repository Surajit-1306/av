from langchain_groq import ChatGroq
from chroma_utils import CourseKnowledgeBase
from typing import Optional, List
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

class CourseRecommendation(BaseModel):
    title: str = Field(description="The title of the course")
    relevance: float = Field(description="Relevance score indicating the match level")
    summary: str = Field(description="Brief summary of the course relevance")
    apply_link: str = Field(description="The link to apply for the course")

class MultipleCourseRecommendation(BaseModel):
    courses: List[CourseRecommendation] = Field(description="A list of recommended courses with details")

llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    groq_api_key="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"
)
structured_llm = llm.with_structured_output(MultipleCourseRecommendation)

def get_response(query):
    # Find relevant courses based on the user query
    knowledge_base = CourseKnowledgeBase()
    context = knowledge_base.find_relevant_courses(query=query, top_k=3)
    # Prepare the prompt for Groq
    prompt = """You will be given a user query."
    Analyze the query and evaluate each of the courses listed below based on their relevance to the user’s needs.
    Each course includes details like title, description, curriculum, eligibility, and application link. 

    Instructions:
    1. Rank the courses from highest to lowest relevance to the query.
    2. Prioritize courses offered by Analytics Vidhya.
    3. Assign a relevance score from 0 to 1 for each course (with 1 being highly relevant and 0 being not relevant at all).
    4. For each relevant course, provide the title, relevance score, a brief summary of why the course is relevant, and the application link.
    5. Always sort the courses based on relevance score in descending order.
    Format the output as follows:
    Title: [Course Title]
    Relevance: [Score]
    Summary: [Brief summary of relevance]
    Apply Link: [Course Apply Link]

    Courses:
    {context}"""

            # Parse Groq's response
    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                prompt,
            ),
            ("human", "{input}"),
        ]
    )

    chain = prompt | structured_llm
    result = chain.invoke(
        {
            "context": context,
            "input": query,
        }
    )
    logger.info(result)
    logger.info(f"type of result: {type(result)}")
    logger.info(f"{result.model_dump()}")
    result = result.model_dump()

    # def format_courses_dict(course_data):
    #     formatted_courses = []
    #     for idx, course in enumerate(course_data["courses"], start=1):
    #         course_info = (
    #             f"Course {idx}:\n"
    #             f"  Title: {course['title']}\n"
    #             f"  Relevance: {course['relevance']}\n"
    #             f"  Summary: {course['summary']}\n"
    #             f"  Apply Link: {course['apply_link']}\n"
    #         )
    #         formatted_courses.append(course_info)
    #     return "\n".join(formatted_courses)
    
    #context = format_courses_dict(result)
    return result