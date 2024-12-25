# Rasa Chatbot  

Rasa based chatbot, which is able to handle customers writing to the restaurant, looking for information and ordering the food. 

https://github.com/codete/oreilly-intelligent-bots/blob/master/Homework.ipynb

## Run rasa chatbot
To setup the enviroment you need to

```
python -m venv .venv
source .venv/bin/activate 
pip install -r requirements.txt
````

and set enviroment variable `DISCORD_TOKEN`
```
set DISCORD_TOKEN="your_token_number" # windows
export DISCORD_TOKEN="your_token_number" #linux/mac
```

Then to run chatbot
```
python discord_connector.py
```
and in different terminal
```
rasa run actions
```
and also run
```
rasa run
```

Now your chatbot is ready!
You can test it now on discord