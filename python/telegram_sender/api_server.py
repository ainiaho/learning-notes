from quart import Quart, request, jsonify
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
import uuid

from bot_sender import TelegramBotSender
from config import SESSION_STRING

app = Quart(__name__)

# 初始化 sender 和调度器
sender = TelegramBotSender(SESSION_STRING)
scheduler = AsyncIOScheduler()

# 存储定时任务
scheduled_jobs = {}


@app.before_serving
async def startup():
    """服务启动前初始化"""
    scheduler.start()
    print("调度器已启动")


@app.after_serving
async def shutdown():
    """服务关闭时清理"""
    scheduler.shutdown()
    print("调度器已关闭")


# ==================== 路由 ====================

@app.route("/health", methods=["GET"])
async def health():
    """健康检查"""
    try:
        me = await sender.get_me()
        return jsonify({"status": "ok", "user": me})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/send", methods=["POST"])
async def send_message():
    """发送消息给单个目标

    Body:
    {
        "target": "@BotUsername",  // 机器人用户名或用户ID
        "text": "/start"
    }
    """
    data = await request.get_json()

    if not data:
        return jsonify({"error": "缺少请求体"}), 400

    target = data.get("target") or data.get("bot")  # 兼容旧参数
    text = data.get("text")

    if not target or not text:
        return jsonify({"error": "缺少 target 或 text 参数"}), 400

    result = await sender.send_message(target, text)

    if result["success"]:
        return jsonify(result)
    else:
        return jsonify(result), 500


@app.route("/send-batch", methods=["POST"])
async def send_batch():
    """批量发送消息

    Body:
    {
        "messages": [
            {"target": "@bot1", "text": "hello"},
            {"target": "@bot2", "text": "hi"},
            {"target": "user_id_or_username", "text": "test"}
        ]
    }
    """
    data = await request.get_json()

    if not data:
        return jsonify({"error": "缺少请求体"}), 400

    messages = data.get("messages")

    if not messages or not isinstance(messages, list):
        return jsonify({"error": "缺少 messages 数组参数"}), 400

    results = await sender.send_batch(messages)
    success_count = sum(1 for r in results if r["success"])

    return jsonify({
        "total": len(messages),
        "success": success_count,
        "failed": len(messages) - success_count,
        "results": results
    })


@app.route("/send-and-wait", methods=["POST"])
async def send_and_wait():
    """发送消息并等待回复

    Body:
    {
        "target": "@BotUsername",
        "text": "/start",
        "timeout": 10
    }
    """
    data = await request.get_json()

    if not data:
        return jsonify({"error": "缺少请求体"}), 400

    target = data.get("target") or data.get("bot")
    text = data.get("text")
    timeout = data.get("timeout", 10.0)

    if not target or not text:
        return jsonify({"error": "缺少 target 或 text 参数"}), 400

    result = await sender.get_bot_response(target, text, timeout)

    return jsonify(result)


# ==================== 定时任务路由 ====================

@app.route("/schedule", methods=["POST"])
async def schedule_message():
    """创建定时发送任务

    Body:
    {
        "target": "@BotUsername",
        "text": "定时消息",
        "schedule": {
            "type": "once",        // once: 一次, interval: 间隔, cron: cron表达式
            "datetime": "2026-03-29 15:00:00",  // type=once 时使用
            "interval": 60,        // type=interval 时使用，单位秒
            "cron": "0 9 * * *"    // type=cron 时使用，cron表达式
        }
    }
    """
    data = await request.get_json()

    if not data:
        return jsonify({"error": "缺少请求体"}), 400

    target = data.get("target") or data.get("bot")
    text = data.get("text")
    schedule = data.get("schedule")

    if not target or not text:
        return jsonify({"error": "缺少 target 或 text 参数"}), 400

    if not schedule:
        return jsonify({"error": "缺少 schedule 参数"}), 400

    job_id = str(uuid.uuid4())[:8]
    schedule_type = schedule.get("type", "once")

    # 创建触发器
    if schedule_type == "once":
        dt_str = schedule.get("datetime")
        if not dt_str:
            return jsonify({"error": "once 类型需要 datetime 参数"}), 400
        try:
            run_date = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return jsonify({"error": "datetime 格式错误，应为 YYYY-MM-DD HH:MM:SS"}), 400
        trigger = DateTrigger(run_date=run_date)

    elif schedule_type == "interval":
        interval = schedule.get("interval")
        if not interval:
            return jsonify({"error": "interval 类型需要 interval 参数"}), 400
        trigger = IntervalTrigger(seconds=interval)

    elif schedule_type == "cron":
        cron_expr = schedule.get("cron")
        if not cron_expr:
            return jsonify({"error": "cron 类型需要 cron 参数"}), 400
        trigger = CronTrigger.from_crontab(cron_expr)

    else:
        return jsonify({"error": f"不支持的 schedule type: {schedule_type}"}), 400

    # 添加任务
    job = scheduler.add_job(
        sender.send_message,
        trigger=trigger,
        args=[target, text],
        id=job_id,
        name=f"Send to {target}"
    )

    scheduled_jobs[job_id] = {
        "job_id": job_id,
        "target": target,
        "text": text,
        "schedule_type": schedule_type,
        "next_run": str(job.next_run_time) if job.next_run_time else None,
        "status": "active"
    }

    return jsonify({
        "success": True,
        "job_id": job_id,
        "next_run": str(job.next_run_time) if job.next_run_time else None
    })


@app.route("/schedule-batch", methods=["POST"])
async def schedule_batch():
    """创建批量定时任务

    Body:
    {
        "messages": [
            {"target": "@bot1", "text": "hello"},
            {"target": "@bot2", "text": "hi"}
        ],
        "schedule": {
            "type": "once",
            "datetime": "2026-03-29 15:00:00"
        }
    }
    """
    data = await request.get_json()

    if not data:
        return jsonify({"error": "缺少请求体"}), 400

    messages = data.get("messages")
    schedule = data.get("schedule")

    if not messages or not isinstance(messages, list):
        return jsonify({"error": "缺少 messages 数组参数"}), 400

    if not schedule:
        return jsonify({"error": "缺少 schedule 参数"}), 400

    job_ids = []

    for msg in messages:
        target = msg.get("target")
        text = msg.get("text")
        schedule_type = schedule.get("type", "once")
        job_id = str(uuid.uuid4())[:8]

        if schedule_type == "once":
            dt_str = schedule.get("datetime")
            run_date = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
            trigger = DateTrigger(run_date=run_date)
        elif schedule_type == "interval":
            trigger = IntervalTrigger(seconds=schedule.get("interval"))
        elif schedule_type == "cron":
            trigger = CronTrigger.from_crontab(schedule.get("cron"))
        else:
            continue

        job = scheduler.add_job(
            sender.send_message,
            trigger=trigger,
            args=[target, text],
            id=job_id
        )

        scheduled_jobs[job_id] = {
            "job_id": job_id,
            "target": target,
            "text": text,
            "schedule_type": schedule_type,
            "next_run": str(job.next_run_time) if job.next_run_time else None,
            "status": "active"
        }

        job_ids.append(job_id)

    return jsonify({
        "success": True,
        "job_ids": job_ids,
        "count": len(job_ids)
    })


@app.route("/schedule/list", methods=["GET"])
async def list_scheduled():
    """获取所有定时任务"""
    return jsonify({
        "jobs": list(scheduled_jobs.values()),
        "total": len(scheduled_jobs)
    })


@app.route("/schedule/<job_id>", methods=["DELETE"])
async def cancel_scheduled(job_id):
    """取消定时任务"""
    if job_id not in scheduled_jobs:
        return jsonify({"error": "任务不存在"}), 404

    scheduler.remove_job(job_id)
    scheduled_jobs[job_id]["status"] = "cancelled"
    del scheduled_jobs[job_id]

    return jsonify({"success": True, "message": f"任务 {job_id} 已取消"})


@app.route("/dialogs", methods=["GET"])
async def get_dialogs():
    """获取对话列表"""
    limit = request.args.get("limit", 20, type=int)
    dialogs = await sender.get_dialogs(limit)
    return jsonify({"dialogs": dialogs})


@app.route("/me", methods=["GET"])
async def get_me():
    """获取当前用户信息"""
    me = await sender.get_me()
    return jsonify(me)


if __name__ == "__main__":
    print("启动 Telegram Bot Sender API...")
    print()
    print("接口文档:")
    print("  消息发送:")
    print("    POST /send           - 发送单条消息")
    print("    POST /send-batch     - 批量发送消息")
    print("    POST /send-and-wait  - 发送并等待回复")
    print()
    print("  定时任务:")
    print("    POST /schedule       - 创建定时任务")
    print("    POST /schedule-batch - 批量定时任务")
    print("    GET  /schedule/list  - 获取任务列表")
    print("    DEL  /schedule/<id>  - 取消任务")
    print()
    print("  其他:")
    print("    GET  /health         - 健康检查")
    print("    GET  /me             - 用户信息")
    print("    GET  /dialogs        - 对话列表")
    print()

    app.run(host="0.0.0.0", port=5000, debug=False)
