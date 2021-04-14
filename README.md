# This is a repo for CSCI3100 Project. We are team E2 working on *Alpha Bet*

Dear TA(s) who is visiting this repo please read the following to learn the places of our code.

Our team decided to use Django as the development framework and native Django include a lot of its original own code. We distributed the work into different sub tasks that are assigned to different team members.

Currently our work can be divided into three main parts, namely: **Frontend**, **Strategy Analyzer** and **Stock Floor**

For final code and commented code, we have merge them all into 1 single branch *elon*.

---

To view the initial code of Strategy Analyzer, please visit branch *elon*

Under ./strategy urls.py, views.py contain our own code on partial routing of this version of the website

Under ./strategy/templates/strategy contain a few html files but there is not much to see, it is added just to make the website work

Under ./strategy/dash_apps contain the core application of strategy analyzer created by Django_Dash

Under ./stock_floor forms.py, models.py, urls.py, views.py contain our own code on partial routing of this version of the website as well as the design for user forms and database model.

Under ./stock_floor/templates/stock_floor, all the .html files contain our own code for frontend.

To run the code, you may create a virtual environment using conda and install all the library from the environment.yml, then simply type

    python manage.py runserver

---