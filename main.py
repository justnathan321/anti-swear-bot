import discord
import random

# Discord Bot Token
TOKEN = 'YOUR-TOKEN'

# Command related stuff
PREFIX = 'ASB '
ADD_COMMAND = PREFIX + 'add ['
HELP_COMMAND = PREFIX + 'help'
SHOW_WORDS_COMMAND = PREFIX + 'show all'

# Censored words related stuff
words_per_guilds = list((list(), list()))
stop_swearing_msg = list(
    ("stop swearing!", "no swearing in this server!", "please behave yourself.", "be nice, stop swearing"))

# Bot client stuff
client = discord.Client()


@client.event
async def on_ready():
    words_per_guilds.__getitem__(0).append(client.guilds)
    print(f'{client.user} has connected to Discord!')

    for x in words_per_guilds.__getitem__(0).__getitem__(0):
        words_per_guilds.__getitem__(1).append(list(('fuck', 'shit')))

    await client.change_presence(activity=discord.Game('"' + HELP_COMMAND + '" for more info'))


@client.event
async def on_message(message):
    message_guild = message.channel.guild

    if message.author == client.user:
        return

    lower_message = message.content.lower()
    words = lower_message.split()

    # Check if there is a bad word in the sentence
    for word in words:
        if word in get_swear_words_for_guild(message_guild):
            await message.channel.send(
                "Hey! " + message.author.mention + " " + stop_swearing_msg.__getitem__(random.randrange(0,
                                                                                                        len(
                                                                                                            stop_swearing_msg) - 1)))
            await message.channel.send(
                "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Italian_traffic_signs_-_fermarsi_e_dare_precedenza_-_stop.svg/1200px-Italian_traffic_signs_-_fermarsi_e_dare_precedenza_-_stop.svg.png")
            return

    # Respond to Add message, add a message
    if message.content.startswith(ADD_COMMAND):
        add_message = message.content.lower()
        word_to_add = find_between(add_message, '[', ']')
        if word_to_add == -1:
            await message.channel.send(
                'Something went wrong. Make sure to pass a word and to end the command with **]**')
            await message.channel.send(f'For example: **{ADD_COMMAND}dummy]**')
        else:
            add_swear_words_for_guild(message_guild, word_to_add)
            await message.channel.send('The word **' + word_to_add + '** has been added to the list of censored words!')

    # Respond to Help message
    if message.content == HELP_COMMAND:
        await message.channel.send(
            f'The bot that prevents users from swearing!\n{ADD_COMMAND}**word**] to add a word that should be censored.'
            f'\n{SHOW_WORDS_COMMAND}.'
            f'\nAll swearing words are case insensitive.')

    # # Respond to Show All Words message
    if message.content == SHOW_WORDS_COMMAND:
        await message.channel.send('Censored words:\n' + get_swear_words_for_guild(message_guild).__str__())


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return -1


def get_position_of_guild_in_list(guild):
    return words_per_guilds.__getitem__(0).__getitem__(0).index(guild)


def get_swear_words_for_guild(guild):
    list_position = get_position_of_guild_in_list(guild)
    return words_per_guilds.__getitem__(1).__getitem__(list_position)


def add_swear_words_for_guild(guild, word):
    list_position = get_position_of_guild_in_list(guild)
    return words_per_guilds.__getitem__(1).__getitem__(list_position).append(word)


client.run(TOKEN)
