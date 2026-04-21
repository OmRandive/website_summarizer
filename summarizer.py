from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"

def summarize(content, style, custom):
    style_map = {
        "Short": "Summarize briefly in 3-4 lines.",
        "Detailed": "Provide a detailed explanation.",
        "Bullet Points": "Summarize in clear bullet points.",
        "Beginner Friendly": "Explain in simple terms."
    }

    instruction = style_map.get(style, "")

    if custom:
        instruction += f" Also follow: {custom}"

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You summarize websites clearly."},
            {"role": "user", "content": instruction + "\n\n" + content}
        ]
    )

    return response.choices[0].message.content
