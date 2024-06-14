import time
from datetime import datetime
from django.conf import settings
from apps.chatbot.models import ChatMessage
from django.conf import settings
from openai import OpenAI
import pytz

# 全局初始化 OpenAI 客戶端
client = OpenAI(api_key=settings.API_KEY)


def create_threads_id(content="HI"):
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


def continue_conversation(user_input, chatbot):
    """繼續對話並處理用戶的新輸入"""
    chapter_id = chatbot.chapter.id
    thread_id = chatbot.now_thread
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


def get_chatbot_response(user_input, chatbot):
    print(f"使用settings.API_KEY:{settings.API_KEY}")
    state = continue_conversation(user_input, chatbot)
    thread_id = chatbot.now_thread
    try:
        if state:
            messages = get_threads_message(thread_id)
            chatbot_response = load_chat_message(messages, chatbot)
        else:
            chatbot_response = "對不起我不太清楚，請稍後再試，或是聯繫管理員。"
    except Exception as e:
        chatbot_response = f"在獲取最新消息時發生錯誤：{str(e)}"
    return chatbot_response


def load_chat_message(messages, chatbot):
    """保存聊天訊息"""
    latest_user_message = messages[1]
    latest_assistant_message = messages[0]
    create_chat_message(latest_user_message, chatbot)
    latest_assistant_response=create_chat_message(latest_assistant_message, chatbot)
    return latest_assistant_response


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
