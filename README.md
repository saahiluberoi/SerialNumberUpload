# README #
The application inputs CSV files from the user and sends the serial numbers to M3 via API: SOS100MI/AddIndItem/

### What is this repository for? ###
The application inputs CSV files from the user, wrangles the data and sends the serial numbers over to Movex.
* To send data to via M3 API: SOS100MI/AddIndItem/. 
* The item description is retrieved from m3 via API: MMS200MI/GetItmBasic/
* There is a config.py file with all the configurations used in the application.

### Backend Framework ###
The application is built using Flask Framework and deployed using gUnicorn. A gUnicorn_config.py file holds all the deployment configurations and commands.

### Frontend Framework ###
The front-end is developed using HTML/CSS and Vanilla JS. 
* A template folder is created with all the required HTML files.
* Static folder is there with all the css files. For styling materialize css has been used.
* All the JS is stored under the folder scripts.

### Version ###	
* Version V1.0: For Continuous Gas Flow

### How do I get set up? ###
* sudo apt-get upgrade -y
* Create a virtual environment. python3 -m venv <**name_of_virtualEnv**>
* Start the virtual environment. source **name_ov_virtualEnv**/bin/activate
* cd SerialNumberUpload
* pip install -r requirement.txt
* export FLASK_APP=app.py
* export FLASK_ENV=development/production (based on env)
* flask run

### Contribution guidelines ###
* For checking all the connections, go to test.py and check all the connections
* Code review: Author

### Who do I talk to? ###
* Repo owner: Dux Manufacturing Limited
* Author: Saahil Uberoi 