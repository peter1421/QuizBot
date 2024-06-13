import time

from django.conf import settings
from openai import OpenAI
from django.contrib import messages

# 全局初始化 OpenAI 客戶端
client = OpenAI(api_key=settings.API_KEY)


def create_threads_id(content = "HI"):
    thread = client.beta.threads.create(
        messages=[
            {"role": "user", "content": content},
        ],
    )
    return thread.id


def find_assistant_by_id(chapter_id):
    # 通过书ID找到书名
    chapter_config = settings.CHATBOT_CONFIGS.get(chapter_id)
    if not chapter_config:
        return "Chapter config not found."
    return chapter_config


def continue_conversation(user_input, thread_id, chapter):
    """繼續對話並處理用戶的新輸入"""
    chapter_id = chapter.id
    assistant_id = find_assistant_by_id(chapter_id)['assistant_id']
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input,
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id)
    run = wait_for_completion(thread_id, run.id)
    return run.status == "completed"


def wait_for_completion(thread_id, run_id):
    """等待對話運行完成."""
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    while run.status != "completed":
        time.sleep(1)
        message=f"{thread_id}-{run_id}提交成功，正在處理中，請稍後...{run.status}"
        print(message)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id, run_id=run_id)
    message=f"{thread_id}-{run_id}提交成功，處理完成，請查看結果。{run.status}"
    return run


def get_threads_message(thread_id):
    """獲取對話線程中的所有消息"""
    message_response = client.beta.threads.messages.list(thread_id=thread_id)
    return message_response.data


def get_latest_message(thread_id):
    """獲取對話線程中的最新消息"""
    messages = get_threads_message(thread_id)
    if messages:
        latest_message = messages[0].content[0].text.value
        return latest_message
    return "No messages found."


def get_chatbot_response(user_input, thread_id, chapter):
    state = continue_conversation(user_input, thread_id, chapter)
    if state:
        chatbot_response = get_latest_message(thread_id)
    else:
        chatbot_response = "出現錯誤，請稍後再試。"
    return chatbot_response
