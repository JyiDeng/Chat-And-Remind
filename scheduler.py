from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from config import (
    CRON_MINUTE, CRON_HOUR, CRON_DAY, CRON_MONTH, CRON_DAY_OF_WEEK,
    SCHEDULED_MESSAGE_PROMPT
)
import threading

# 全局锁，防止任务重复执行
_task_lock = threading.Lock()
_last_execution_time = None


def init_scheduler(chat_service, history_manager):
    """
    初始化定时任务调度器
    
    Args:
        chat_service: ChatService实例
        history_manager: ChatHistoryManager实例
        
    Returns:
        调度器实例
    """
    scheduler = BackgroundScheduler()
    
    def scheduled_task():
        """定时任务：每N分钟触发一次"""
        global _last_execution_time
        
        # 使用锁防止并发执行
        if not _task_lock.acquire(blocking=False):
            print("任务正在执行中，跳过本次触发")
            return
        
        try:
            current_time = datetime.now()
            
            # 防止短时间内重复执行（精确到秒，至少间隔20秒）
            if _last_execution_time is not None:
                time_diff = (current_time - _last_execution_time).total_seconds()
                if time_diff < 20:  # 至少间隔20秒
                    print(f"距离上次执行仅 {time_diff:.1f} 秒，跳过本次触发")
                    return
            
            print(f"\n{'='*50}")
            print(f"定时任务触发时间: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*50}")
            
            # 获取助手在此时间点应该说的话
            assistant_message = chat_service.get_scheduled_message(SCHEDULED_MESSAGE_PROMPT)
            
            print(f"助手消息: {assistant_message}")
            
            # 保存定时消息到历史记录
            history_manager.save_message('assistant', assistant_message, is_scheduled=True)
            
            # 更新最后执行时间
            _last_execution_time = current_time
            
            print(f"{'='*50}\n")
            
        except Exception as e:
            print(f"定时任务执行错误: {e}")
        finally:
            _task_lock.release()
    
    # 使用cron触发器，支持完全自定义的cron表达式
    scheduler.add_job(
        scheduled_task,
        'cron',
        minute=CRON_MINUTE,
        hour=CRON_HOUR,
        day=CRON_DAY,
        month=CRON_MONTH,
        day_of_week=CRON_DAY_OF_WEEK,
        id='scheduled_reminder',
        name='定时提醒任务',
        replace_existing=True,
        max_instances=1  # 确保同一时间只有一个实例运行
    )
    
    cron_expression = f"{CRON_MINUTE} {CRON_HOUR} {CRON_DAY} {CRON_MONTH} {CRON_DAY_OF_WEEK}"
    print(f"定时任务已配置: Cron表达式 = '{cron_expression}'")
    
    return scheduler
