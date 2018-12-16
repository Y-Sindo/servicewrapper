## Service Wrapper

With the development of the Internet, service providers tend to present their service data through web pages. However, various convenient web pages have placed great restrictions on developers' use
of web pages' source data. The service wrapper system is designed to encapsulate data in the web pages, wrap it up as a service, and provide RESTful APIs to invoke the service for developers during development.

We use [a web segment algorithm](https://github.com/liaocyintl/WebSegment), which converts a HTML document into structured data,  to get the metadata location description information，and  then  wrap it up as a service.

![未标题-1](http://cmsci.net/lvxy/servicewrapper/tree/master/FrontEnd/main_page.png)

## Getting Started

Service Wrapper adopts a front-end separation architecture, as you can see, the folder `BackEnd` is the back-end code, while the folder `FrontEnd` is the front-end code.

Service Wrapper  has been tested on many flavors of Linux, MacOS, and Windows, so you can run Service Wrapper on any OS or in the cloud. We provide two different configurations for development and production environments. 

#### clone

```git clone git@www.cmsci.net:lvxy/servicewrapper.git```

#### Development Environment

To run the back end code:

```shell
cd servicewrapper/BackEnd
# install required libraries
pip install -r requirement.txt

# run by python
python run.py
# or you can also run by gunicorn
gunicorn -w 4 -b :8000 run:app false
```

To run the front end code:

```shell
cd servicewrapper/FrontEnd

# run by http-server
http-server --cors  ./ index.html  # index.html is the start page

```

#### Production Environment

You can run Service Wrapper in the production environment that has Docker 1.11+ and Docker compose installed.

```shell
cd servicewrapper/BackEnd/docker

sudo docker-compose build
sudo docker-compose up -d
```

Because the production environment is driven by **docker** and uses **nginx** as a WEB resource server and a reverse proxy server, You have to place the front-end code in the location specified by `servicewrapper/BackEnd/docker/nginx.conf`.





#### 