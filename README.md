# Newspaper Agency

## Overview
The Newspaper Agency Project ("Project") allows you to track Newspapers with assigned to them Redactor(s) and Topic. 
So you will always know, who were the Publishers of each Newspaper and of which Topic is Newspaper.

## Check it out

[Newspaper Agency Project deployed to Render](https://newspapers-agency-gsg6.onrender.com)

## Installing / Getting started
```shell
git clone https://github.com/andriy-md/newspaper_agency.git
cd newspaper_agency
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver      # Starts Django Server
```
settings.py use load_dotenv from dotenv
Sample of how to fill .env is provided in .env.sample

## Features
* You cant watch list of all newspapers with the ability to search specific Newspaper by its title.
* You may create new Newspaper as well as update information concerning the existing one or delete it.
* Authentication functionality for Redactor/User


## Demo

![Website Interface](demo.png)

##  Acknowledgements
Project was developed with the use of templates created by © Creative Tim.
