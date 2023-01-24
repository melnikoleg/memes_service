import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from memes_service.logger import configure_logging
from memes_service.services.queue_service import QueueService
from memes_service.services.telegram_parser_service import TelegramChannelParserService

queue_service = QueueService()
telegram_channel_parser_service = TelegramChannelParserService()


async def process_queues_all_users_job():
    await queue_service.process_queues_all_users()


async def process_new_memes_job():
    await telegram_channel_parser_service.process_new_memes()


if __name__ == "__main__":
    configure_logging()

    scheduler = AsyncIOScheduler()
    # scheduler.add_job(process_queues_all_users_job, "interval", seconds=60)
    scheduler.add_job(process_new_memes_job, "interval", seconds=60)
    # scheduler.add_job(process_new_memes_job, "interval", hours=24)
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
