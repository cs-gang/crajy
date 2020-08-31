import os
import dotenv
dotenv.load_dotenv(dotenv.find_dotenv())
#API URL and headers as lists
FANCY = ["https://ajith-fancy-text-v1.p.rapidapi.com/text", {'x-rapidapi-host': "ajith-Fancy-text-v1.p.rapidapi.com",'x-rapidapi-key': os.environ.get("RAPIDAPI_KEY")}]
LOVE_CALC = ["https://love-calculator.p.rapidapi.com/getPercentage", {'x-rapidapi-host': "love-calculator.p.rapidapi.com", 'x-rapidapi-key': os.environ.get("RAPIDAPI_KEY")}]