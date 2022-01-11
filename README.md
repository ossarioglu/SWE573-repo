# SWE573-repo
Repository for works on SWE573 course study for 2021-22 semester.

This repo will be source for progress on my studies at SWE573 course at Bogazici University Master of Science degree on Software engineering.

This repo will be modified regularly for tracking tasks and issues while achieving assignments discussed weekly basis.

Project Name : socializeUs  
Project Topic: Web application for matching people for offering and getting service

## Instruction for installing the application

Applications below needs to be installed into your computer in order to run the system at your local computer:
-	Python: The code is written in Python using its frameworks for web development. Version 3.10.0 is installed during development of the product. You can install Python by following the instructions at https://www.python.org/downloads/ .
-	Django: Django framework is used to code front-end and back-end. Version 3.2.9 is used during development. In order to install Django into your local. You can install into to systemwide or to virtual environments. This is up to your choice. To install Django, at the terminal, you need to type command below 
    -	for Mac/Linux: `python -m pip install Django` 
    -	for Windows: `py -m pip install Django`
-	PostgreSQL : For keeping data, PostgreSQL is utilized. You can install PostgreSQL by following the instructions at https://www.postgresql.org/download/. 
-	Pillow: In order to add image processing capabilities, Pillow is installed. Pillow is the friendly PIL fork by Alex Clark and Contributors. PIL is the Python Imaging Library by Fredrik Lundh and Contributors. To install Pillow, at the terminal, you need to type command below 
    -	for Mac/Linux `python3 -m pip install --upgrade Pillow`
    -	for Windows: `python3 -m pip install --upgrade Pillow`

If you want to run dockerized version of the system, all the source code is available at GitHub repository with the link https://github.com/ossarioglu/SWE573-repo. You can clone a copy of this repository into your local pc, and dockerize it to run the system. Dockerfile, and docker-compose.yml files are available at repository.

Pleaser follow below instructions for installation process. At your terminal, apply commands below step by step:

1.	Choose selected folder to work: 
            `cd [foldername]`
2.	Clone Repository:  git clone 
            `git clone https://github.com/ossarioglu/SWE573-repo.git`
3.	Choose application folder (webapp):
            `cd webapp`
4.	Create docker images
            `docker-compose up -d --build`
5.	Make migrations for setting up the PostgreSQL database
            `docker-compose run socializeus  python manage.py migrate`
6.	Create a superuser by following the command and its instructions
            `docker-compose run socializeus  python manage.py createsuperuser`
7.	Containerize your images
            `docker-compose up`

After following these steps, your app will work on localhost with URL http://localhost
