
import logging
import requests

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


#travel palces api code

url = "https://travel-places.p.rapidapi.com/"

payload = { "query": "{ getPlaces(categories:[\"NATURE\"],lat:37,lng:-122,maxDistMeters:50000) { name,lat,lng,abstract,distance,categories } }"}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "13f7c64447mshf93fbfc967b9920p119350jsn94528bf10f5f",
	"X-RapidAPI-Host": "travel-places.p.rapidapi.com"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)



def get_api_url(params):
    categories = params['categories']
    country = params['country']
    print(type(categories))
    print(country)
    payload = { "query": '{ getPlaces(categories: [f"{categories}"], country:f"{country}") { name,lat,lng,abstract,distance,categories,country } }'}

    return  requests.request("POST", url, json=payload, headers=headers).json()
    

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    cat = 'Available places categories - "CITY", "NATURE", "MAJOR", "POI", "PEAK", "THEMEPARK" \
     "CASTLE", "MUSEUM", "ZOO", "UNESCO", "HERITAGERAILWAY", "SKIAREA", "BEACH","AIRPORT","RAILSTATION"'
    await update.message.reply_html(
        f"Hi {user.mention_html()}!\n\n{cat}"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")



async def country_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_splited = update.message.text.split('/')
    print(message_splited)
    print(message_splited[0])
    q = {
        'categories': message_splited[0].strip(),
        'country': message_splited[1].strip()
    }

    response = get_api_url(q)
    print(response)
    
    if response.get('data', None) != None:
        place = ''
        places = response['data']["getPlaces"]
        print(places)
        if len(places) > 0:
            for item in places:
                place += f'Name: {item["name"]}\n'
            await update.message.reply_text(place)
        else:
            await update.message.reply_text('Data not found')
    else:
        await update.message.reply_text('Data not found')


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("1779735646:AAFoPa_0mMrsAdj7B7t9VLSzLeMeUlpk-E0").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    #application.add_handler(CommandHandler("find", country_command))
    

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, country_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()