import time
from datetime import datetime

import pytz
from apps.chapter.models import Chapter
from apps.chatbot.models import ChatMessage
from django.conf import settings
from openai import OpenAI

client = OpenAI(api_key=settings.API_KEY)

class ChatbotHelper:
    def __init__(self, chatbot):
        self.chatbot = chatbot

    def create_threads_id(self, content="HI"):
        thread = client.beta.threads.create(
            messages=[
                {"role": "user", "content": content},
            ],
        )
        return thread.id
    def get_chatbot_asscistant(self):
        chapter_id = self.chatbot.chapter.id
        asscistant_id = Chapter.objects.get_first_assistant_id_of_chapter(chapter_id)
        print(f"asscistant_id:{asscistant_id}")
        return asscistant_id
    
    def find_assistant_by_id(self, chapter_id):
        chapter_config = settings.CHATBOT_CONFIGS.get(chapter_id)
        if not chapter_config:
            return "Chapter config not found."
        return chapter_config

    def continue_conversation(self, user_input):
        chapter_id = self.chatbot.chapter.id
        thread_id = self.chatbot.now_thread
        assistant_id = self.find_assistant_by_id(chapter_id)['assistant_id']
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input,
        )
        run = client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=assistant_id)
        run = self.wait_for_completion(thread_id, run.id)
        return run.status == "completed"

    def wait_for_completion(self, thread_id, run_id, timeout=60):
        start_time = time.time()
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id, run_id=run_id)
        while run.status != "completed":
            if (time.time() - start_time) > timeout:
                print(f"處理超時，請檢查後台或重新提交。Thread ID: {thread_id}, Run ID: {run_id}")
                break
            print(f"{thread_id}-{run_id}提交成功，正在處理中，請稍後...{run.status}")
            time.sleep(min(5, timeout - (time.time() - start_time)))
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id, run_id=run_id)
        if run.status == "completed":
            print(f"{thread_id}-{run_id}提交成功，處理完成，請查看結果。{run.status}")
        return run

    def get_threads_message(self, thread_id):
        message_response = client.beta.threads.messages.list(thread_id=thread_id)
        return message_response.data

    def get_latest_message(self, messages):
        if messages:
            latest_message = messages[0].content[0].text.value
            return latest_message
        return "No messages found."

    def get_chatbot_response(self, user_input):
        print(f"使用settings.API_KEY:{settings.API_KEY}")
        state = self.continue_conversation(user_input)
        thread_id = self.chatbot.now_thread
        try:
            if state:
                messages = self.get_threads_message(thread_id)
                chatbot_response = self.load_chat_message(messages)
            else:
                chatbot_response = "對不起我不太清楚，請稍後再試，或是聯繫管理員。"
        except Exception as e:
            chatbot_response = f"在獲取最新消息時發生錯誤：{str(e)}"
        return chatbot_response

    def load_chat_message(self, messages):
        latest_user_message = messages[1]
        latest_assistant_message = messages[0]
        self.create_chat_message(latest_user_message)
        latest_assistant_response = self.create_chat_message(latest_assistant_message)
        return latest_assistant_response

    def create_chat_message(self, message):
        timezone = pytz.timezone(settings.TIME_ZONE)
        content_text = message.content[0].text.value
        role = message.role
        tag = "測試"
        created_at_timestamp = message.created_at
        if created_at_timestamp is not None:
            created_at = datetime.fromtimestamp(created_at_timestamp, tz=timezone)
        else:
            created_at = None
        thread_id = message.thread_id
        created_message = ChatMessage.objects.create(
            chatbot=self.chatbot,
            role=role,
            content=content_text,
            tag=tag,
            created_at=created_at,
            thread_id=thread_id
        )
        return created_message
