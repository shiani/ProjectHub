# ToDo application

Todo application is a python backend with Django Framework
## Installation

Use Docker for run in your local 

first to build image use this line
```bash
sudo docker-compose build
```

Then if you have not create a superuser use this command (if you have one skip this):


```bash
sudo docker-compose up sh
```
then in the command line use this line to createsuperuser:
```bash
python manage.py createsuperuser
```
you can exit command line with exit()

Then You can run container
```bash
sudo docker-compose up
```

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)