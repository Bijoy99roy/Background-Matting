# Background-Matting

Here i'm providing a solution that can do realtime background matting, that means
it can remove background/blur background/change backgound

## 📜 DataSet

I have used a library for segmentation after my previous solution was very slow.
In previous solution i used mask rcnn but the end product was very slow.
But i have the dataset that i created, and i have uploaded it to kaggle.

The images were annotated using labelmeV3.16.7
Find it from below link incase if it any use for you

```URL
  https://www.kaggle.com/bijoyroy/human-segmentation-dataset
```

## 🚀 Deployed App
[Launch App](https://background-matting1.herokuapp.com)

## Demo

![App Screenshot](/gif/systemdemo.gif)


  
## 🛠 Requirements to run project

- python 3.7.11
- Numpy
- Flask
- flask_socketio
- mediapipe
- opencv

  
## Tech Stack

**Client:** HTML, CSS, JS

**Server:** Python, Flask

- SocketIo for realtime data transfer
  
## ⚙ Installation

Install all the requirements by running requirements.txt

```cmd
  pip install -r requirements.txt
```