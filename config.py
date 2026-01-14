import os
from dotenv import load_dotenv

load_dotenv()

# SiliconFlow API配置
API_KEY = os.getenv("API_KEY", "YOUR_API_KEY")
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
MODEL = "deepseek-ai/DeepSeek-V3.2"

# 聊天助手配置
SYSTEM_PROMPT = "你是用户的可爱伴学姐妹，你要做的是每一段时间提醒用户认真学习、打起精神，一定能学会。同时，作为自律的硕士生，你也应该和用户汇报你现在做什么，具体到：在某一个学科（计算机学科、体育锻炼、逻辑提升），做某件事（学习知识、练习题目、写代码；有氧、力量练习、腹部练习，等等）。最好可以具体到第五层的内容，比如在计算机学科-AI领域-表征学习方向-阅读论文-学到了某个具体的知识；体育锻炼-有氧-跑步-30分钟-有具体的感受。"

# 定时任务配置（使用cron表达式）
# Cron表达式格式: minute hour day month day_of_week
# 规则详见 apscheduler.triggers.cron — APScheduler 3.11.2.post1 documentation: https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html#introduction
# minute: 分钟 (0-59)
# hour: 小时 (0-23)
# day: 日期 (1-31)
# month: 月份 (1-12)
# day_of_week: 星期几 (0-6，0表示星期日)
# 
# 示例:
# "*/15 * * * *" - 每15分钟执行一次
# "0 * * * *" - 每小时的第0分钟执行
# "0 9 * * *" - 每天早上9点执行
# "0 9,18 * * *" - 每天9点和18点执行
# "0 9 * * 1-5" - 每周一到周五的9点执行
CRON_MINUTE = "*/15"  # 每15分钟
CRON_HOUR = "*"      # 每小时
CRON_DAY = "*"       # 每天
CRON_MONTH = "*"     # 每月
CRON_DAY_OF_WEEK = "*"  # 每周

SCHEDULED_MESSAGE_PROMPT = "时间到啦，请提醒用户认真学习，并且高兴地告诉用户你刚才干了些什么。"

# 聊天数据保存路径
CHAT_HISTORY_FILE = "chat_history.json"
