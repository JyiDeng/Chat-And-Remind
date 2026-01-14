from app import app, scheduler
import os

# 只在主进程中启动调度器（避免多worker重复执行）
# gunicorn的主进程PPID为1或特定值
def is_main_process():
    """检查是否为主进程或单进程模式"""
    # 如果是gunicorn worker，检查是否为第一个worker
    worker_id = os.environ.get('GUNICORN_WORKER_ID')
    if worker_id is not None:
        return worker_id == '0'
    # 如果不是gunicorn环境，则启动调度器
    return True

if is_main_process() and not scheduler.running:
    scheduler.start()
    print("定时任务已启动（主进程）")

if __name__ == "__main__":
    app.run()
