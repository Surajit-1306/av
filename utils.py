# Format function
def format_filters(filters):
    formatted_string = "\n".join(
        f"{key.replace('_', ' ').capitalize()}: {value}" for key, value in filters.items() if value
    )
    return formatted_string


def create_context_string(results):
    # Check if 'metadatas' field has relevant course data
    if results.get("metadatas"):
        context = "Relevant Course Information:\n\n"
        
        for i, metadata in enumerate(results["metadatas"][0]):
            course_title = metadata.get("title", "N/A")
            course_description = metadata.get("course_description", "N/A")
            curriculum = metadata.get("curriculum", "N/A")
            eligibility = metadata.get("eligibility", "N/A")
            apply_link = metadata.get("apply_link", "N/A")
            
            # Append each course information to the context
            context += (
                f"Course {i + 1}:\n"
                f"Title: {course_title}\n"
                f"Description: {course_description}\n"
                f"Curriculum: {curriculum}\n"
                f"Eligibility: {eligibility}\n"
                f"Apply Link: {apply_link}\n\n"
            )
        
        return context
    else:
        return "No relevant course information found."