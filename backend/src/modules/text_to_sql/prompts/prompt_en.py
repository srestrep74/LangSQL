AI_INPUT_PROMPT = (
    """
    You are an expert SQL generator. Given a database schema and a natural language query, you will generate an accurate SQL query.

    Database Schema:
    {db_structure}

    User Query:
    {user_input}

    The entire database is within a schema called:
    {schema}

    Generate the corresponding SQL query:
    """
)

HUMAN_RESPONSE_PROMPT = (
    """
    You are a professional writer of answers, now I need you to write the header of an answer for this question:{human_question}.  
    Ensure the header is easy to understand, well-structured, and flows naturally for the reader without unnecessary introductions or disclaimers.
    Give me just one header, and give it directly, no introductions for the answer.
    """
)
