import aiohttp
import random
import discord



async def get_random_word(bot):
    alphabet = random.choice("abcdefghijklmnopqrstuvwxyz") + '*'
    params = {"sp": alphabet, "max": "1000", "md": "dp"}

    async with bot.session.get("https://api.datamuse.com/words", params=params) as response:
        words = await response.json()
        filter_words(words)
        word_index = random.randint(1,len(words)-1)
        return words[word_index]


def filter_words(words):
    for i in words:
        if 'tags' not in i.keys() or 'defs' not in i.keys():
            words.remove(i)
        elif 'prop' in i['tags']:
            words.remove(i)
    return words

#hangman data
HANGMANPICS = [r'''
          +---+
          |   |
          |    
          |    
          |    
          |    
        =========''', r'''
          +---+
          |   |
          |   O
          |    
          |    
          |    
        =========''', r'''
          +---+
          |   |
          |   O
          |   |
          |    
          |    
        =========''', r'''
          +---+
          |   |
          |   O
          |   |\
          |    
          |    
        =========''', r'''
          +---+
          |   |
          |   O
          |  /|\
          |     
          |  
        =========''', r'''
          +---+
          |   |
          |   O
          |  /|\
          |    \
          |    
        =========''', r'''
          +---+
          |   |
          |   O
          |  /|\
          |  / \
          |    
        =========''']