from openai import OpenAI
import sqlite3
import json

# ==========================
# GROQ CLIENT
# ==========================
client = OpenAI(
    api_key="Here you api key",
    base_url="https://api.groq.com/openai/v1"
)

# ==========================
# SAFE SQL FUNCTION
# ==========================
def run_sql(query):

    blocked_words = [
        "DROP",
        "DELETE",
        "TRUNCATE",
        "ALTER",
        "UPDATE",
        "INSERT",
        "CREATE"
    ]

    query_upper = query.upper()

    for word in blocked_words:
        if word in query_upper:
            return {
                "error": f"Blocked dangerous command: {word}"
            }

    try:

        conn = sqlite3.connect("employees.db")
        cursor = conn.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()

        conn.close()

        return {
            "result": rows
        }

    except Exception as e:

        return {
            "error": str(e)
        }

# ==========================
# TOOL DEFINITION
# ==========================
tools = [
    {
        "type": "function",
        "function": {
            "name": "run_sql",
            "description": "Execute safe SELECT queries on employee database",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL query"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# ==========================
# CHAT LOOP
# ==========================
while True:

    user_input = input("\nAsk Database > ")

    if user_input.lower() == "exit":
        break

    messages = [
        {
            "role": "system",
            "content": """
You are a database assistant.

Convert user requests into SQL.

Rules:
1. Only generate SELECT statements.
2. Never generate DELETE.
3. Never generate DROP.
4. Never generate UPDATE.
5. Never generate ALTER.
6. Never generate INSERT.
7. Table name is employees.
8. Columns:
   empid
   name
   department
"""
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    try:

        # ==========================
        # FIRST AI CALL
        # ==========================
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        if assistant_message.tool_calls:

            tool_call = assistant_message.tool_calls[0]

            args = json.loads(
                tool_call.function.arguments
            )

            sql_query = args["query"]

            print("\nGenerated SQL:")
            print(sql_query)

            # ==========================
            # EXECUTE SQL
            # ==========================
            result = run_sql(sql_query)

            print("\nDatabase Result:")
            print(result)

            # ==========================
            # SEND RESULT BACK TO AI
            # ==========================
            messages.append({
                "role": "assistant",
                "content": None,
                "tool_calls": assistant_message.tool_calls
            })

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": "run_sql",
                "content": json.dumps(result)
            })

            final_response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages
            )

            print("\nAI Response:")
            print(final_response.choices[0].message.content)

        else:

            print("\nAI:")
            print(assistant_message.content)

    except Exception as e:

        print("\nError:")
        print(e)