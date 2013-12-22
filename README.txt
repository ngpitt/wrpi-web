Live demo: http://wrpi.iecfusor.com

Overview - A drop-in replacement website for wrpi.org. We will targeting the public facing site and members area, including DJ clearance, scheduling, work hours, and meeting attendance.

Goal - The goal of this project is to develop a modular framework to ease in the deployment of private members area style sites by employing the model-view-controller architecture. Each module will include a html file following a template, a python file that will retrieve and process data from a MySQL database, and a JavaScript file with the necessary methods for communicating with the web server via JSON.

Tasks - (1) Setup an Apache/MySQL web server with WSGI support and Django. (2) Create a MySQL schema that will fit the needs of the site. (3) Create a generic ajax loader in JavaScript capable of loading in modules for the public site and member's area. (4) Create the necessary templates. (4) Delegate different modules (private and public) to different group members.
