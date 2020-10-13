# English Premier League (EPL) Salary Prediction

Let us look into how performances on field can affect football players salaries.

I chose this particular subject knowing that the data is not direclty avaiblable on the internet, and will certainly be messy ! That is basically the occasion for me to make my hands dirty with data !

I implemented two webscrappers to scrap the websites I will need to gather my data :
* Players statistics : www.whoscored.com
* Salaries : www.spotrac.com  

  


# Configuration

To recreate the environement, run this command in your terminal :  
`$ conda env create -f environment.yaml`

# Credits
The WhoScored Web Scraper is inspired by a solution available [here](https://github.com/cboutaud/whoscraped). The structure of the website's pages has changed since then (2006), we had to ajust some features and add an exception management mechanism to handle errors when pages are not proprely charged.