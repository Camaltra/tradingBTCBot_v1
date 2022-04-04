<h1>First version of my BTC crypto trading bot</h1>

<h2>How it's work | Strategy used</h2>
<p>After backtesting two strategies, the SMA200/SMA600 trend (also the SMA300/SMA600, but don't get beautiful results) and the MACD signal, I chose th use the frst one and implemented into the bot. It also got a stop loss risk, at 7% after my backtesting strat with the BTC to get the better results</br>
So the bot, every our, gonna make API call to get last 624 candles of the BTC market, and check if it's a good hour to buy, or good hour to sell all our BTC.</br>
</p>

<h2>How to use</h2>

<p>First, make sure that pandas, numpy, matplotlib and regex are install in your computer</p>

<p>Then, you have to create a file, named API_KEY.py, with your public and private API key from youre binance account (api_key and api_secret var name).</br>
Then, from a server, just run the program (traidingBot.py file). Be sure that the server will never stop</p>

<h3>backtestingStrategies</h3>
<p>File that regroup the backtesting strat that I use for my final bot, run on jupyter</p>

<h3>tradingBot</h3>
<p>The source code of the trading bot</p>

<h2>What I learned from this project</h2>
<p>At the end, this bot will not be the most efficient that you could find, and also, it may not working as the result of the backtesting | IT'S NOT A FINNANCIAL ADVISE, IF YOU USE IT TO INVEST, IT'S ON YOURE ONW RISK | But this allow me to discover <b>pandas</b>, <b>Jupyter</b>, <b>matplotlib</b> and <b>work with an API</b>. It also put me into financial analyse, and see how create indicators and use it.</br>
For now, I will not uptade it, since I didn't got a lot of free time, and wanna focus on other programming project. But I know that in a year, I will create a v2, with AI, to predict stock price, and not only for BTC, but also for other crypto, and why not shares ?
</p>
