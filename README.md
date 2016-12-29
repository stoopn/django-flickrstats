# django-flickrstats

A Django app to permanently store and analyze daily flickr photo stats (work in progress)

## Installation

django-flickrstats requires a running django installation, Javascript frameworks d3 and nvd3, as well as the python wrappers python-nvd3 and django-nvd3 (to visualize access statistics).

### Installing dependencies:

To install django:
```
pip install django
```

We use [bower](http://bower.io) to manage the JavaScript libraries. bower can be installed via npm, which requires installation of node.js first. On OSX, the easiest way is using Homebrew:  

```
brew install node.js
```
This will also install the npm command. Next, install bower (the -g option installs bower globally)

```
npm install -g bower
```

Add the file .bowerrc to the top level of the django site with the following contents:
```
{
    "directory": "flickrstats/static/"
}
```

This instructs bower to store static JS to the flickrstats/static directory (which I assume you obtained from this repo in the meantime). Now we are ready to install d3 and nvd3 into the flickrstats/static directory. Make sure you are in the django site top level directory and execute

```
bower install d3#4.4.0
bower install nvd3#1.8.5
```

Unfortunately, the stable version of python-nvd3 is not anymore compatible with the current d3/nvd3 branches. We thus have to install the fixed version (thanks, aniketmaithani, for fixing the chart.tooltip function!):

```
pip install git+git://github.com/stoopn/python-nvd3.git
pip install django-nvd3
```

This should get you all required dependencies to use this django app. Install the flickrstats app using the usual python manage.py routines and migrate the DB to add necessary tables.

## Using aggregator.py

The script flickrstats/aggregator.py is used to aggregate daily access statistics into the django DB. To use it, you need to have a flickr API key (and a flickr account). You can get the flickr API [here](https://www.flickr.com/services/api/misc.api_keys.html). Once you obtained it, write down the API key and secret from the flickr website. Create the file flickrstats/flickrsecret.py with contents:
```
api_key = 'MY API KEY'
api_secret = 'MY API SECRET'
```
Now you should be ready to start aggregation by calling
```
python aggregation.py```
```
