import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from memes_service.logger import configure_logging
from memes_service.services.queue_service import QueueService

queue_service = QueueService()


async def run_job():

    await queue_service.process_queues_all_users()


if __name__ == "__main__":
    configure_logging()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_job, "interval", seconds=60)
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
