# Poker Vision (YOLOv8 Branch)


Poker Vision (YOLOv8 Branch) is a computer vision project that uses YOLOv8 Object Detection Model to identify the cards shown at a poker table. The project can be used to develop a poker bot that can play the game automatically, or to provide players with real-time information about their hand and the hands of their opponents.

## Differences And Issues:
The card identification in this branch is more consistent compared to the main branch. The only issue in this version is that it fails to detect cards with a rank of '10'.

## How it works:

Poker Vision takes a video feed from a camera and utilizes the YOLOv8 Object Detection Model to identify the cards on the table, including their suit and rank. Once the cards have been identified, the information is used to recognize the players and the dealer, and to determine the type of hand each player has.

## Installation and usage:

Poker Vision is written in Python and uses the OpenCV library for image processing and YOLOv8 for detecting suit and rank of cards. To install Poker Vision, you will need to install Python, OpenCV, and YOLOv8. Once you have installed the necessary dependencies, you can clone the Poker Vision repository from GitHub and run the following command to start the project:

python poker_vision.py
Poker Vision will start by identifying the cards on the table. Once the cards have been identified, the project will display the following information:

- The cards of the dealer
- The cards of each player
- The type of hand each player has

## Example:

The following image shows an example of the output of Poker Vision:

![](https://i.imgur.com/zlhqGOA.jpg)

## Contributing:

If you are interested in contributing to the Poker Vision project, please fork the repository and submit a pull request. We welcome any contributions that can improve the project.