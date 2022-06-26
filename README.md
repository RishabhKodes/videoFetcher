# videoFetcher
An API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.
<br>
<br>

<h3> Pre-installation steps: </h3>

  * Start the redis-server locally (in a seperate terminal):
    <p>If you are using Linux, type the below command for running the redis server:<p>

    ``` $ redis-cli ```

<br>
<h3> Steps to run locally: </h3>

   1. Clone the Repository <br>

    $ git clone https://github.com/RishabhKodes/videoFetcher.git

   2. Move into root directory.

    $ cd videoFetcher/

   3. Install the required packages.

    $ pip install -r requirements.txt


   4. Make all the migrations
 
    $ python manage.py migrate

   5. Run the following command for starting the server

    $ python manage.py runserver

   6. Run and configure the celery apps (in 2 seperate terminals):

    $ celery -A videoFetcher worker --loglevel=info 
    
<br>

    $ celery -A videoFetcher beat -l info


<br><h4>
  10. To access the dashboard go to http://127.0.0.1:8000/video (the respective pages can be accessed as params in the url -> /videos/?page=2)
<br>