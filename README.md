





https://github.com/user-attachments/assets/69ecddbf-3db9-43bb-9c0e-81497fb50600






# Road Accident Detection & Alert System

# Overview

### The Road Accident Detection & Alert System is a project designed to detect accidents on roads, trigger alerts, capture accident details, and enable emergency response. It utilizes computer vision, audio alerts, and communication technologies to improve response times and assist in emergency situations.

# Features

### Accident Detection: Utilizes computer vision algorithms to detect accidents based on visual cues.

### Alert System: Triggers an alert sound upon detecting an accident to notify nearby individuals.

### Screenshot Capture: Captures a screenshot of the accident scene along with date and time for documentation.

### Emergency Response: Allows authorized personnel to initiate emergency medical services by calling an ambulance.

# Technologies Used

### Computer Vision: OpenCV for image processing and object detection.

### Audio Alert: Integration with sound libraries for alert notifications.

### Communication: Integration with twilio for emergency response.

### Documentation: GitHub for version control and project sharing.

# Getting Started

## To use the Road Accident Detection & Alert System, follow these steps:

### Clone the repository to your local machine and open in an IDE . 
### Install the necessary dependencies listed in the requirements file.
### Before running the program, you need to run the accident-classification.ipynb file which create's the model_weights.keras file. Then, to run this python program, you need to execute the main.py python file. 

The accident detection works by training the model on labeled images of accidents and non-accidents. Once trained, the model learns to recognize patterns or features in the images that distinguish between the two categories. After training, it can predict whether new, unseen images contain an accident or not based on what it has learned from the training data.

The accuracy of this detection depends on the quality and quantity of the data used to train the model.

The file **accident-classification.ipynb** contains the images and data used to train the model, as well as the necessary code for the training process.

### Run the main application script to start monitoring for accidents (main.py) .
### In case of an accident, follow the on-screen instructions for emergency response actions.

# Usage
### The system is designed for use in surveillance and monitoring scenarios where quick detection and response to accidents are crucial. It can be deployed in traffic management systems, surveillance cameras, and other relevant environments.


