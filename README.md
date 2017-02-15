# C42-Assignment
create a simple API Proxy in Python that combines and caches multiple calls to the C42 API into one single call with a lightweight response.

## Outline
My plan is to create a lightweight, single threaded server to talk to. Single threaded, because there is no requirement for any rate or performance. In my mind that means; keep it simple and small, worry about optimalisation later. I plan to use a small lightweight library / framework like for instance web.py or tornado and not go full django/nginx/whatever. 
For caching I want to use memcached.
I'm using python3.

My first steps will be to get the call to the C42 Api up and running. 
Then get my proxy running and accepting requests.
Then to tie the two together.

## Dependencies
* Python 3.5.x
* Memcached
* https://github.com/yyuu/pyenv-virtualenv
* https://github.com/yyuu/pyenv-virtualenvwrapper

## Setup
```
# skip this if your local version is python 3.5 or better
$ pyenv install 3.5.2
# carry on.
$ pyenv virtualenv 3.5.2 <virtualenv-name>
$ pyenv activate <virtualenv-name>
$ pip install -r requirements.txt
$ cp settings.default.py settings.py
<edit settings.py add the C42 token>
```

## Run the proxy
```
$ python proxy.py
```

## Run the test (in another terminal window)
```
$ python test.py
```
