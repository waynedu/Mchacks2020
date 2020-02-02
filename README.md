# Mchacks2020
#Inspiration


While on our way to McHacks, we watched the movie Lion (2016). This showed us the huge problems refugees and their families experience when they are constantly separated with little to no way of reconnecting with one another.

Past data depicts that a lot of kids get lost and are separated from the family for a very long time.There are amber alerts but the success rate is not that high.

#What it does


Web-app that takes a photograph of a user using the computers webcam. It then uses the facial recognition API to find the potential or similar faces stored in our database.

If it finds a match, it will output the known information of the individual in the photo, if not, then it will create a prompt for the user to input information about the person in the picture which will then be stored in the database for future use.The app is open to public, not only restricted for government to help find the lost ones.

#How I built it

The program uses the computers webcam and KAIROS facial recognition API to train the dataset in the KAIROS database to recognise various faces. It then runs ML algorithms using the KAIROS API to detect similarities in between different photos. On the back end we used django MVC framework to fetch the results from the database and store the information in mySql. Front end part we used javascript and ajax to send the images and required data to be stored in the database.

#Challenges I ran into

Initially the application was hard to architect.Most of the debugging took place while taking a photo from webcam from the browser and send it to the Kairos Api database for recognition.Hard to get the concept of base64 encoding and decoding for the image verification and sending it to database. Learnt ajax on spot to send the image and required data on the server.

#Accomplishments that I'm proud of

We made an app that can help reduce a big problem and help save some lives. We were able to teach ourselves various different frameworks and technologies over a short period of time, to be able to make this project work. We learnt team management and how to cooperate with team members for the success of the project.Got more exposure in the field of Machine learning.

#What I learned

We learned Rest API, JSON , Kairos facial recognition API , mySQL Database,Django MVC framework. And most importantly learned DEBUGGING.

#What's next for Find.ai

Use of other API to help fetch the data as more data more lives can be saved like Facebook Graph API to increase the possible scope of the ML training as well as the overall usefulness of the app.

Use of the Twilio SMS API to send reports and updates over SMS to potential parents or guardians of the lost ones.

#Requirements
pip install django

pip install django-bootstrap4

pip install mysql

