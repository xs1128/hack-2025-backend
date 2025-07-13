import requests
import schedule
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# API configurations using schedule package
API_CONFIGS = {
    "conclude_streak": {
        "url": "http://localhost:8000/internal/conclude-streak",
        "method": "POST",
        "schedule_type": "daily_time",
        "schedule_value": "00:00",  # 12:00 AM daily
        "enabled": True,
        "time_range": None,
    },
    "morning_email": {
        "url": "http://localhost:8000/internal/morning-mail",
        "method": "GET",
        "schedule_type": "daily_time",
        "schedule_value": "09:00",  # 9:00 AM daily
        "enabled": True,
        "time_range": None,
    },
    "evening_email_1": {
        "url": "http://localhost:8000/internal/night-mail",
        "method": "GET",
        "schedule_type": "daily_time",
        "schedule_value": "22:30",  # 10:30 PM daily
        "enabled": True,
        "time_range": None,
    },
    "evening_email_2": {
        "url": "http://localhost:8000/internal/night-mail",
        "method": "GET",
        "schedule_type": "daily_time",
        "schedule_value": "23:00",  # 11:00 PM daily
        "enabled": True,
        "time_range": None,
    },
    "evening_email_3": {
        "url": "http://localhost:8000/internal/night-mail",
        "method": "GET",
        "schedule_type": "daily_time",
        "schedule_value": "23:30",  # 11:30 PM daily
        "enabled": True,
        "time_range": None,
    },
    "conclude_league": {
        "url": "http://localhost:8000/internal/conclude-league",
        "method": "POST",
        "schedule_type": "weekly_day_time",
        "schedule_value": ("sunday", "20:00"),  # Sunday 8:00 PM
        "enabled": True,
        "time_range": None,
    },
}


def is_within_time_range(time_range):
    """Check if current time is within the specified time range"""
    if not time_range:
        return True  # No time range means always active

    start_time, end_time = time_range
    current_time = datetime.now().time()

    start = datetime.strptime(start_time, "%H:%M").time()
    end = datetime.strptime(end_time, "%H:%M").time()

    # Handle time ranges that cross midnight
    if start <= end:
        # Normal case: start < end (e.g., 08:00 to 18:00)
        return start <= current_time <= end
    else:
        # Crosses midnight: start > end (e.g., 22:00 to 06:00)
        return current_time >= start or current_time <= end


def call_api(name, config):
    """Make a simple API call"""
    try:
        method = config.get("method", "GET").upper()
        url = config["url"]

        if method == "POST":
            response = requests.post(url, timeout=30)
        else:
            response = requests.get(url, timeout=30)

        if response.ok:
            logger.info(f"✅ {name}: Success (Status: {response.status_code})")
        else:
            logger.warning(f"⚠️ {name}: Failed (Status: {response.status_code})")
    except Exception as e:
        logger.error(f"❌ {name}: Error - {str(e)}")


def api_worker(name, config):
    """Worker function for a single API"""
    try:
        # Check if current time is within the allowed time range
        time_range = config.get("time_range")
        if is_within_time_range(time_range):
            call_api(name, config)
        else:
            logger.info(f"⏰ {name}: Outside time range, skipping")
    except Exception as e:
        logger.error(f"Worker error for {name}: {e}")


def start_scheduler():
    """Start all API workers using the schedule package"""
    logger.info("🚀 Starting API Scheduler...")

    # Log enabled APIs and set up schedules
    enabled_apis = []
    for name, config in API_CONFIGS.items():
        if config.get("enabled", True):
            enabled_apis.append(name)

            # Set up schedule based on configuration
            schedule_type = config["schedule_type"]
            schedule_value = config["schedule_value"]

            if schedule_type == "interval_minutes":
                schedule.every(schedule_value).minutes.do(api_worker, name, config)
                logger.info(f"✅ Scheduled {name}: every {schedule_value} minutes")
            elif schedule_type == "interval_seconds":
                schedule.every(schedule_value).seconds.do(api_worker, name, config)
                logger.info(f"✅ Scheduled {name}: every {schedule_value} seconds")
            elif schedule_type == "daily_time":
                schedule.every().day.at(schedule_value).do(api_worker, name, config)
                logger.info(f"✅ Scheduled {name}: daily at {schedule_value}")
            elif schedule_type == "weekly_day_time":
                day, time_str = schedule_value
                if day == "sunday":
                    schedule.every().sunday.at(time_str).do(api_worker, name, config)
                elif day == "monday":
                    schedule.every().monday.at(time_str).do(api_worker, name, config)
                elif day == "tuesday":
                    schedule.every().tuesday.at(time_str).do(api_worker, name, config)
                elif day == "wednesday":
                    schedule.every().wednesday.at(time_str).do(api_worker, name, config)
                elif day == "thursday":
                    schedule.every().thursday.at(time_str).do(api_worker, name, config)
                elif day == "friday":
                    schedule.every().friday.at(time_str).do(api_worker, name, config)
                elif day == "saturday":
                    schedule.every().saturday.at(time_str).do(api_worker, name, config)
                logger.info(f"✅ Scheduled {name}: {day} at {time_str}")

    logger.info(f"📈 Running {len(enabled_apis)} API workers with schedule package")

    # Main scheduler loop
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down...")
        schedule.clear()


if __name__ == "__main__":
    start_scheduler()
