import logging

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import FSInputFile, Message

from src.settings import settings

dp = Dispatcher()
logger = logging.getLogger(__name__)


@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        text="Hi! Enter '/report'",
    )


@dp.message(Command("report"))
async def report_handler(message: types.Message) -> None:
    logger.info(
        f"Request report by user id: "
        f"{str(message.from_user and message.from_user.id)}",
    )

    await message.answer_document(
        document=FSInputFile(
            path="export/result.xlsx",
            filename="result.xlsx",
        ),
    )


@dp.message()
async def echo_handler(message: types.Message) -> None:
    try:
        await message.answer("I know only '/report' ...")
    except TypeError:
        await message.answer("Nice try!")


async def bot_loop() -> None:
    bot = Bot(
        token=settings.TG_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await bot.set_my_commands(
        [
            types.BotCommand(command="start", description="Start"),
            types.BotCommand(command="report", description="Send the report"),
        ],
    )

    logger.info("Bot loop starting ...")
    await dp.start_polling(bot)
    logger.info("Bot loop finished.")
