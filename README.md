# My Life in Music Blog Post Generator

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## About <a name = "about"></a>

A stupid GPT-3 experiment to generate blog posts to accompany the weekly Spotify playlists for my music blog, [My Life in Music](https://mylifeinmusic.me).

## Getting Started <a name = "getting_started"></a>

What? You want to run this? Why?? It basically amounts to an AI shitposting on my blog. But if you really want to, here's how.

### Prerequisites

* Python 3.8+
* A GPT-3 API key
* Spotify API Credentials


### Installing

#### Without Docker

Clone the repo:

`git clone https://github.com/BoxingOctopusCreative/mlim-gpt`

Install the requirements via pipenv:

`pipenv install`

Run the app using gunicorn:

`gunicorn --bind 0.0.0.0:5000 app:app`

#### With Docker

Clone the repo:

`git clone https://github.com/BoxingOctopusCreative/mlim-gpt`

Build the docker image:

`docker build -t mlim-gpt .`

Run the docker image:

`docker run -p 5000:5000 mlim-gpt`

## Usage <a name = "usage"></a>

Once the service is running, it should be accessible on port 5000. For a full list of API endpoints, you can access the Swagger UI at `http://app_host:5000/apidocs`.
