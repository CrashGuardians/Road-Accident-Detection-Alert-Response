# Front-End
![Screenshot (97)](https://github.com/user-attachments/assets/4fd0120b-d0bf-4a90-b577-14d149ff0aeb)

# Start-Detection
![Screenshot (98)](https://github.com/user-attachments/assets/010f2a25-46f2-4f10-afdc-b716e42db8fd)

# Screenshot
![Screenshot (99)](https://github.com/user-attachments/assets/36bddbe2-ccc3-48c9-82f9-9a03a0720915)





-------






# Road Accident Detection & Alert System

# Overview

### The Road Accident Detection & Alert System is a project designed to detect accidents on roads, trigger alerts, capture accident details, and enable emergency response. It utilizes computer vision, audio alerts, and communication technologies to improve response times and assist in emergency situations.

# Features

### Main Features : Beep Sound at time of crash + Screenshot of crash + Automatic Call and SMS with Google Map Link for Location.

### Accident Detection: Utilizes computer vision algorithms to detect accidents based on visual cues.

### Alert System: Triggers an alert sound upon detecting an accident to notify nearby individuals.

### Front-End contains Start and Stop Detection feature and also an option to see the crash screenshots.

### Screenshot Capture: Captures a screenshot of the accident scene along with date and time for documentation.

### Emergency Response: Allows authorized personnel to initiate emergency medical services by calling an ambulance.

### Automatically calls the emergency authority and also sents a messege with google map link for location.


# Technologies Used

### Computer Vision: OpenCV for image processing and object detection.

### Audio Alert: Integration with sound libraries for alert notifications.

### Communication: Integration with twilio for emergency response.

### Documentation: GitHub for version control and project sharing.

# Getting Started

## To use the Road Accident Detection & Alert System, follow these steps:

### Clone the repository to your local machine and open in an IDE . 
### Install the necessary dependencies listed in the requirements file.
### Before running the program, you need to run the accident-classification.ipynb file which create's the model_weights.keras file. Then, to run this python program, you need to execute the app.py python file. 

The file **accident-classification.ipynb** contains the images and data used to train the model, as well as the necessary code for the training process.

The accident detection works by training the model on labeled images of accidents and non-accidents. Once trained, the model learns to recognize patterns or features in the images that distinguish between the two categories. After training, it can predict whether new, unseen images contain an accident or not based on what it has learned from the training data.

It is a deep learning model pipeline for image classification using TensorFlow and Keras. It set's up a Convolutional Neural Network (CNN) to classify images in two categories: "Accident" and "Non Accident" based on your training, validation, and test datasets.

The accuracy of this detection depends on the quality and quantity of the data used to train the model.
The output or accident detection efficiency may vary each time you train the model, as the model's performance is influenced by many factors.  It's important to experiment and train the model multiple times to fine-tune it and improve the results. You should try training the model several times, until you achieve a satisfactory result. Each training cycle may yield different outcomes.

### Run the main application script to start monitoring for accidents (app.py) .
### In case of an accident, follow the on-screen instructions for emergency response actions.

# Usage
### The system is designed for use in surveillance and monitoring scenarios where quick detection and response to accidents are crucial. It can be deployed in traffic management systems, surveillance cameras, and other relevant environments.


