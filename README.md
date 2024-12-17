# Rasa Chatbot  

Rasa based chatbot, which is able to handle customers writing to the restaurant, looking for information and ordering the food. 

https://github.com/codete/oreilly-intelligent-bots/blob/master/Homework.ipynb

## Run rasa chatbot
To setup the enviroment you need to

```
python -m venv .venv
source .venv/bin/activate 
pip install requirements.txt
````

Then to run chatbot
```
rasa run actions
```
and in different terminal
```
rasa run
```
and also run
```
python discord_connector.py
```

Now your chatbot is ready!