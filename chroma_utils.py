import os
import time
import logging
from uuid import uuid4
from sentence_transformers import SentenceTransformer
import chromadb
from dotenv import load_dotenv
from utils import create_context_string


# Setup logger
logger = logging.getLogger(__name__)

directory_path = "chromadb_course_index"
collection_name = "analytics_course_index"


class CourseKnowledgeBase:
    def __init__(self):
        try:
            # Initialize ChromaDB client and collection
            self.client = chromadb.PersistentClient(path=directory_path)
            self.collection = self.client.get_or_create_collection(collection_name)
            
            # Initialize embedding model
            self.model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
            
            logger.info("Initialization successful for Course Knowledge Base")
        except Exception as e:
            logger.error(f"Error during initialization: {str(e)}")
            raise e
        finally:
            logger.info("Initialization complete")
    
    def insert_courses(self, courses):
      """Insert courses into ChromaDB with metadata."""
      try:
          start_time = time.time()
          ids, embeddings, metadatas = [], [], []
          
          logger.info("Starting course insertion into knowledge base")

          for course in courses:
              course_description = course.get("course_description", "")
              # Convert the curriculum list to a single string
              curriculum = "; ".join(course.get("curriculum", []))
              metadata = {
                  "title": course.get("course_title", ""),
                  "apply_link": course.get("apply_link", ""),
                  "course_description": course.get("course_description", ""),
                  "curriculum": curriculum,
                  "eligibility": course.get("eligibility", "")
              }

              # Create a unique ID for each course
              course_id = str(uuid4())
              ids.append(course_id)
              
              # Generate embeddings for the course description
              embeddings.append(self.model.encode(course_description).tolist())
              
              # Add metadata
              metadatas.append(metadata)

          # Upsert to collection
          self.collection.upsert(ids=ids, embeddings=embeddings, metadatas=metadatas)

          end_time = time.time()
          elapsed_time = end_time - start_time
          logger.info(f"Course insertion successful. Time taken: {elapsed_time} seconds.")

      except Exception as e:
          logger.error(f"Failed to insert courses. Error: {str(e)}")
          raise e


    def find_relevant_courses(self, query, top_k=3):
        """Retrieve relevant courses based on a query."""
        try:
            start_time = time.time()
            query_embedding = self.model.encode(query).tolist()

            # Query ChromaDB collection
            result = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            logger.info(f"Query result from ChromaDB: {result}")
            context = create_context_string(result)
            return context

        except Exception as e:
            logger.error(f"Error in find_relevant_courses: {str(e)}")
            raise e

    def delete_all_courses(self):
        """Delete all courses from the collection."""
        try:
            self.client.delete_collection(collection_name)
            logger.info("All courses deleted from the knowledge base.")
        except Exception as e:
            logger.error(f"Error in delete_all_courses: {str(e)}")
            raise e

    def print_all_courses(self):
        """Print all courses in the knowledge base."""
        try:
            result = self.collection.get()
            logger.info(f"All courses data: {result}")
            print(result)
        except Exception as e:
            logger.error(f"Error in print_all_courses: {str(e)}")
            raise e
