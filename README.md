

# Britecore Sample Project

This is a sample risk management application for insurers built with Django, Vue.js, Vuekit, and Webpack

## Usage

Try the app here, link to Amazon Zappa deployment

OR to run it locally

- Clone this repository: [link](https://github.com/SombiriX/bCoSub.git)
- Install dependencies  
    - With Anaconda use `conda env create -f requirements.txt`
    - Otherwise use pip to install the listed packages `pip install-r requirements-pip.txt` which *should* work
- Configure Django Run the following to stand up a local server
    -  `./manage.py makemigrations`
    - `./manage.py migrate`
    - `./manage.py runserver 0:8001`
- You should now have a server running and accessible at http://localhost:8001 or http://127.0.0.1:8001  
## Directions
- Use the interface to add risks and risk types using the Risk Manager
- Then go to the Risk Viewer and try adding data into the Risk Types you've created