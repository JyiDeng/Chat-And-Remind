from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from chat_service import ChatService, ChatHistoryManager
from scheduler import init_scheduler
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# 初始化服务
chat_service = ChatService()
history_manager = ChatHistoryManager()

# 初始化定时任务
scheduler = init_scheduler(chat_service, history_manager)


@app.route('/')
def index():
    """返回主页面"""
    return send_from_directory('static', 'index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    处理聊天请求
    
    请求体:
        {
            "message": "用户消息"
        }
    
    响应:
        {
            "success": true,
            "reply": "助手回复"
        }
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'success': False, 'error': '消息不能为空'}), 400
        
        # 保存用户消息
        history_manager.save_message('user', user_message)
        
        # 获取助手回复
        assistant_reply = chat_service.call_api(user_message)
        
        # 保存助手回复
        history_manager.save_message('assistant', assistant_reply)
        
        return jsonify({
            'success': True,
            'reply': assistant_reply
        })
        
    except Exception as e:
        print(f"聊天处理错误: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """
    获取聊天历史
    
    响应:
        {
            "success": true,
            "messages": [...]
        }
    """
    try:
        messages = history_manager.get_all_messages()
        return jsonify({
            'success': True,
            'messages': messages
        })
    except Exception as e:
        print(f"获取历史记录错误: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """健康检查接口"""
    return jsonify({
        'status': 'ok',
        'scheduler_running': scheduler.running
    })


if __name__ == '__main__':
    # 启动定时任务
    scheduler.start()
    print("定时任务已启动")
    
    # 启动Flask应用
    app.run(host='0.0.0.0', port=1342, debug=False)
