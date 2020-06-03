This project contains source code for Auto Grade.

Downlod the project.

#1 To Build and run containers
docker-compose up -d --build

Then you can access the Lab Solution upload and Lab submissions by following links:

1. Lab Solution Key -  http://localhost:5000/upload_key

Click the Choose File button and Select the Lab Key jupyter notebook. Click on Submit button. 
After successful upload of solution key, success message is displayed on the screen.  

2. Lab Submission - http://localhost:5000/upload_lab

Click the Choose File button and Select the Lab Solutions jupyter notebook. Click on Submit button. 
After successful upload of solution submission , success message is displayed on the screen.


#2 To stop containers
docker-compose down -v


#4 To exec web container (example run python manage.py)
docker-compose exec web python manage.py seed_db
