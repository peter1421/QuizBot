import time
from datetime import datetime

import pytz
from apps.chapter.models import Chapter
from apps.chatbot.models import ChatMessage
from django.conf import settings
from django.utils import timezone
from openai import OpenAI

# 全局初始化 OpenAI 客戶端
client = OpenAI(api_key=settings.API_KEY)


def create_threads_id(content="HI"):
    thread = client.beta.threads.create()
    return thread.id


def find_assistant_by_id(chapter_id):
    # 通过书ID找到书名
    chapter_config = Chapter.objects.get_first_assistant_id(chapter_id)
    if chapter_config:
        return chapter_config
    else:
        return "Chapter not found or no assistants associated."


def continue_conversation(messages, chatbot):
    """繼續對話並處理用戶的新輸入"""
    chapter_id = chatbot.chapter.id
    thread_id = chatbot.now_thread
    assistant_id = find_assistant_by_id(chapter_id)
    # 逐一創建所有訊息
    for message in messages:
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role=message["role"],
            content=message["content"],
        )
    run = client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id)
    run = wait_for_completion(thread_id, run.id)
    return run.status == "completed"


def wait_for_completion(thread_id, run_id, timeout=60):
    """等待對話運行完成，設定超時限制，並處理可能的錯誤."""
    start_time = time.time()
    try:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id, run_id=run_id)
        while run.status != "completed":
            if (time.time() - start_time) > timeout:
                print(
                    f"處理超時，請檢查後台或重新提交。Thread ID: {thread_id}, Run ID: {run_id}")
                break
            print(f"{thread_id}-{run_id}提交成功，正在處理中，請稍後...{run.status}")
            # 等待時間不超過剩餘的超時時間
            time.sleep(min(5, timeout - (time.time() - start_time)))
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id, run_id=run_id)

    except Exception as e:
        print(
            f"在獲取執行狀態時發生錯誤：{str(e)}。Thread ID: {thread_id}, Run ID: {run_id}")

    if run.status == "completed":
        print(f"{thread_id}-{run_id}提交成功，處理完成，請查看結果。{run.status}")
    return run


def get_threads_message(thread_id):
    """獲取對話線程中的所有消息"""
    message_response = client.beta.threads.messages.list(thread_id=thread_id)
    return message_response.data


def get_latest_message(messages):
    """獲取對話線程中的最新消息"""
    if messages:
        latest_message = messages[0].content[0].text.value
        return latest_message
    return "No messages found."


def get_chatbot_response(messages, chatbot):
    print(f"使用settings.API_KEY:{settings.API_KEY}")
    thread_id = chatbot.now_thread
    oringinal_message = get_threads_message(thread_id)
    oringinal_message_length = len(oringinal_message)
    state = continue_conversation(messages, chatbot)
    chatbot_response = []
    try:
        if state:
            messages = get_threads_message(thread_id)
            messages_length = len(messages)
            # oringinal_message_length+=1 # 已經預先推送消息
            while messages_length > oringinal_message_length:
                oringinal_message_length +=1
                last_message = create_chat_message(messages[messages_length-oringinal_message_length], chatbot)
                chatbot_response.append(last_message)
        else:
            messages = "對不起我不太清楚，請稍後再試，或是聯繫管理員。"
            chatbot_response = create_error_message(messages, chatbot)
    except Exception as e:
        messages = f"在獲取最新消息時發生錯誤：{str(e)}"
        chatbot_response = create_error_message(messages, chatbot)
    return chatbot_response


def create_chat_message(message, chatbot):
    timezone = pytz.timezone(settings.TIME_ZONE)
    content_text = message.content[0].text.value
    role = message.role
    tag = "測試"  # 可以根據實際情況動態決定
    # 確保 'created_at' 存在並且是有效的時間戳
    created_at_timestamp = message.created_at
    if created_at_timestamp is not None:
        created_at = datetime.fromtimestamp(created_at_timestamp, tz=timezone)
    else:
        created_at = None  # 或者給一個默認值

    thread_id = message.thread_id

    # 呼叫 create_message 儲存訊息
    created_message = ChatMessage.objects.create(
        chatbot=chatbot,
        role=role,
        content=content_text,
        tag=tag,
        created_at=created_at,
        thread_id=thread_id
    )
    return created_message


def create_error_message(content_text, chatbot):
    timezone = pytz.timezone(settings.TIME_ZONE)
    created_at = datetime.fromtimestamp(datetime.now(), tz=timezone)

    # 呼叫 error_message 儲存訊息
    error_message = ChatMessage.objects.create(
        chatbot=chatbot,
        role='assistant',
        content=content_text,
        tag="錯誤",
        created_at=created_at,
        thread_id=chatbot.now_thread
    )
    return error_message