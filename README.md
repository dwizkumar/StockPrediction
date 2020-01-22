# StockPrediction
Stock prediction application setup steps:
Download StockPrediction.zip file

Unzip the directory
 
Download visual studio code
https://code.visualstudio.com/download

Download python(3.7.2 version)
https://www.python.org/downloads/release/python-372/
 

After installation open visual studio code and run in the terminal 
python --version

If it gives error as ‘python’ not recognized as internal or external command. Please set the path of python in the environmental variable path. Also add script directory in the path variable.

Install libraries
python -m pip install --upgrade pip
pip install GetOldTweets3
pip install nltk
pip install pandas
pip install -U scikit-learn
pip install xgboost
pip install tweepy 
pip install pandas_datareader
pip install flask

Go to visual studio’s terminal and run app.py 
python app.py

Open the browser and run http://127.0.0.1:5000/

Select the organization name for prediction has to be made and click on predict stock.
After few seconds predicted results will be displayed in the same window.
