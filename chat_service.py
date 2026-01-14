import json
import os
from datetime import datetime
import requests
from config import API_KEY, API_URL, MODEL, SYSTEM_PROMPT, CHAT_HISTORY_FILE


class ChatService:
    """聊天服务类，负责与SiliconFlow API交互"""
    
    def __init__(self):
        self.api_key = API_KEY
        self.api_url = API_URL
        self.model = MODEL
        self.system_prompt = SYSTEM_PROMPT
        
    def call_api(self, user_message):
        """
        调用SiliconFlow API获取聊天响应
        
        Args:
            user_message: 用户输入的消息
            
        Returns:
            assistant的回复内容
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # 从响应中提取assistant的回复
            if data.get("choices") and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            else:
                return "抱歉，我无法生成回复。"
                
        except requests.exceptions.RequestException as e:
            print(f"API调用错误: {e}")
            return f"API调用失败: {str(e)}"
    
    def get_scheduled_message(self, prompt):
        """
        获取定时任务的消息
        
        Args:
            prompt: 定时任务的提示词
            
        Returns:
            assistant的回复内容
        """
        return self.call_api(prompt)


class ChatHistoryManager:
    """聊天历史管理类"""
    
    def __init__(self, history_file=CHAT_HISTORY_FILE):
        self.history_file = history_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """确保历史记录文件存在"""
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def load_history(self):
        """加载聊天历史"""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载历史记录失败: {e}")
            return []
    
    def save_message(self, role, content, is_scheduled=False):
        """
        保存消息到历史记录
        
        Args:
            role: 'user' 或 'assistant'
            content: 消息内容
            is_scheduled: 是否为定时任务消息
        """
        history = self.load_history()
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "is_scheduled": is_scheduled
        }
        history.append(message)
        
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史记录失败: {e}")
    
    def get_all_messages(self):
        """获取所有消息"""
        return self.load_history()
