import json
import os
import chromadb
from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings
from chroma_utils import CourseKnowledgeBase

load_dotenv()

os.environ['USER_AGENT'] = 'myagent'

llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0.0,
    groq_api_key="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"
)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

urls=['https://courses.analyticsvidhya.com/courses/coding-a-chatgpt-style-language-model-from-scratch-in-pytorch', 'https://courses.analyticsvidhya.com/courses/mastering-multilingual-genai-open-weights-for-indic-languages', 'https://courses.analyticsvidhya.com/courses/learning-autonomous-driving-behaviors-with-llms-and-rl', 'https://courses.analyticsvidhya.com/courses/genai-applied-to-quantitative-finance-for-control-implementation', 'https://courses.analyticsvidhya.com/courses/navigating-llm-tradeoffs-techniques-for-speed-cost-scale-and-accuracy', 'https://courses.analyticsvidhya.com/courses/creating-problem-solving-agents-using-genai-for-action-composition', 'https://courses.analyticsvidhya.com/courses/improving-real-world-rag-systems-key-challenges', 'https://courses.analyticsvidhya.com/courses/choosing-the-right-LLM-for-your-business', 'https://courses.analyticsvidhya.com/courses/building-smarter-llms-with-mamba-and-state-space-model', 'https://courses.analyticsvidhya.com/courses/genai-a-way-of-life', 'https://courses.analyticsvidhya.com/courses/building-llm-applications-using-prompt-engineering-free', 'https://courses.analyticsvidhya.com/courses/building-your-first-computer-vision-model', 'https://courses.analyticsvidhya.com/courses/bagging-boosting-ML-Algorithms', 'https://courses.analyticsvidhya.com/courses/midjourney_from_inspiration_to_implementation', 'https://courses.analyticsvidhya.com/courses/free-understanding-linear-regression', 'https://courses.analyticsvidhya.com/courses/The%20Working%20of%20Neural%20Networks', 'https://courses.analyticsvidhya.com/courses/free-unsupervised-ml-guide', 'https://courses.analyticsvidhya.com/courses/building-first-rag-systems-using-llamaindex', 'https://courses.analyticsvidhya.com/courses/data-preprocessing', 'https://courses.analyticsvidhya.com/courses/exploring-stability-ai']


def extract_details(document, url):
    prompt_reply = PromptTemplate.from_template(
        """
### HTML_Document:{document}
#### url:{url}
           For HTML Document, extract the following details in JSON format:

1. **course_title**: The full title of the course.
2. **course_description**: A brief description or overview of what the course covers.
3. **curriculum**: A list of main topics, modules, or lessons included in the course.
4. **eligibility**: A string description of who should enroll.
5. **apply_link**: fetch the url to apply the course.

Return the results in this valid JSON format:
        """
    )
    chain_email = prompt_reply | llm
    res = chain_email.invoke(input={"document": document, "url": url})
    json_parser = JsonOutputParser()
    res = json_parser.parse(res.content)
    return res

def update_course_details():
    main_list = []
    for url in urls:
        loader = WebBaseLoader(web_path=url)
        document = loader.load().pop().page_content
        main_list.append(extract_details(document=document, url=url))
    
    # with open("data.json", "w") as f:
    #     json.dump(main_list, f, indent=4)
    knowledge_base = CourseKnowledgeBase()
    knowledge_base.delete_all_courses()
    return main_list