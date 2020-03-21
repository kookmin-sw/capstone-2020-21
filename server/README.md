- ## API Server

  Assumes that you have Python 3.8

  ### Install `virtualenv`

  ~~~shell
  pip install virtualenv
  ~~~

  ### Create `virtualenv`

  ~~~shell
  # server/
  virtualenv venv
  ~~~

  ### Activate `virtualenv`

  ~~~shell
  # server/venv/Scripts
  activate
  ~~~

  ### Install Packages

  ~~~shell
  # server/
  pip install -Ur requirements/local.txt
  ~~~

  ### Migrate Database(if using local settings)

  ~~~shell
  # server
  python manage.py migrate
  ~~~

  ### `runserver`

  ~~~shell
  python manage.py runserver
  ~~~

  

  

  

  