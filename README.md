# Vlad-AI
The psychopathic image captioner, inspired by MIT's [Norman](http://norman-ai.mit.edu/).

This project is currently under construction. 

# Data Wrangling
To obtain horrifying enough captions, I am  creating a pipeline to source image/caption pairs from reddit threads then 
save them in a MySQL database.

To run the current pipeline follow these instructions:

1. create an app in reddit by going [here](https://old.reddit.com/prefs.apps).
2. create a mysql database locally. [this may help](https://dev.mysql.com/doc/workbench/en/wb-getting-started-tutorial-create-connection.html)
3. create a file 'server/config.py'
4. in config.py create two dictionaries 'reddit_data' and 'mysql_data' with the following formats:
```python
reddit_data = {
  'username': <YOUR_REDDIT_USERNAME>,
  'password': <YOUR_REDDIT_PASSWORD>,
  'app_name': <REDDIT_APP_NAME>,
  'app_id': <REDDIT_APP_ID>,
  'app_secret': <REDDIT_APP_SECRET_KEY>
}

mysql_data = {
  'username': <MYSQL_DB_USERNAME>,
  'password': <MYSQL_DB_PASSWORD>,
  'database': <MYSQL_SCHEMA_NAME>
}
```
5. run server/datascraper.py

Note: I assume that the database is on localhost port 3306.