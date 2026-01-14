// API配置
const API_BASE_URL = window.location.origin;

// DOM元素
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    loadHistory();
    setupEventListeners();
});

// 设置事件监听器
function setupEventListeners() {
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

// 加载历史消息
async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/history`);
        const data = await response.json();
        
        if (data.success && data.messages) {
            chatMessages.innerHTML = ''; // 清空现有消息
            data.messages.forEach(msg => {
                displayMessage(msg.role, msg.content, msg.is_scheduled, false);
            });
            scrollToBottom();
        }
    } catch (error) {
        console.error('加载历史消息失败:', error);
    }
}

// 发送消息
async function sendMessage() {
    const message = messageInput.value.trim();
    
    if (!message) {
        return;
    }
    
    // 禁用输入和按钮
    setInputState(false);
    
    // 显示用户消息
    displayMessage('user', message);
    
    // 清空输入框
    messageInput.value = '';
    
    // 显示加载状态
    const loadingId = showLoadingMessage();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message })
        });
        
        const data = await response.json();
        
        // 移除加载消息
        removeLoadingMessage(loadingId);
        
        if (data.success) {
            // 显示助手回复
            displayMessage('assistant', data.reply);
        } else {
            displayMessage('assistant', `错误: ${data.error || '未知错误'}`);
        }
        
    } catch (error) {
        removeLoadingMessage(loadingId);
        displayMessage('assistant', `发送失败: ${error.message}`);
        console.error('发送消息失败:', error);
    } finally {
        // 重新启用输入和按钮
        setInputState(true);
        messageInput.focus();
    }
}

// 显示消息
function displayMessage(role, content, isScheduled = false, shouldScroll = true) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    if (isScheduled) {
        messageDiv.classList.add('scheduled');
    }
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';
    bubbleDiv.textContent = content;
    
    // 添加时间戳
    const timeSpan = document.createElement('span');
    timeSpan.className = 'message-time';
    timeSpan.textContent = new Date().toLocaleTimeString('zh-CN', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    bubbleDiv.appendChild(timeSpan);
    
    messageDiv.appendChild(bubbleDiv);
    chatMessages.appendChild(messageDiv);
    
    if (shouldScroll) {
        scrollToBottom();
    }
}

// 显示加载消息
function showLoadingMessage() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    messageDiv.id = 'loading-message';
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';
    bubbleDiv.innerHTML = '<span class="loading">正在思考中</span>';
    
    messageDiv.appendChild(bubbleDiv);
    chatMessages.appendChild(messageDiv);
    
    scrollToBottom();
    
    return 'loading-message';
}

// 移除加载消息
function removeLoadingMessage(loadingId) {
    const loadingMessage = document.getElementById(loadingId);
    if (loadingMessage) {
        loadingMessage.remove();
    }
}

// 设置输入状态
function setInputState(enabled) {
    messageInput.disabled = !enabled;
    sendButton.disabled = !enabled;
}

// 滚动到底部
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 定期刷新历史消息以获取定时任务的消息
setInterval(() => {
    loadHistory();
}, 30000); // 每30秒刷新一次
