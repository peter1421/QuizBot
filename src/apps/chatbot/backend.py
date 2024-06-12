from openai import OpenAI

from django.conf import settings



def get_threads_id(chapter):
    content = "HI"
    api_key = settings.API_KEY
    client = OpenAI(api_key=api_key)
    thread = client.beta.threads.create(
        messages=[
            {"role": "user", "content": content},
        ],
    )
    return thread.id


def find_api_by_id(chapter_id):
    # 通过书ID找到书名
    chapter_config = settings.CHATBOT_CONFIGS.get(chapter_id)
    if not chapter_config:
        return "Chapter config not found."
    return chapter_config
