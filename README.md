# Intelligent-Laptop
## A personal facial recognition model auto building program
### CS4200 - Project
---
<br>


## Dependency
> A device with camera or webcam <br>
> Python >= 3.7 (The develope version is 3.7.9) <br>
> All needed packages are listed in ```requirements.txt```
<br>

## Getting Started
### Installation
> Be sure that you are in the root directory of this repo
```
pip install -r requirements.txt
```
<br>

## Check installation

### run ```main.py```
```
python main.py
# or python3 main.py
```

### skip dataset download first
> It's optional because the downloading will cost about few minutes

![](https://i.imgur.com/Jb6Uux6.png)

### choose sign up and enter your name and email address
> I recommend you to enter your real email address because we can check it later.

![](https://i.imgur.com/z8dJIrR.png)

### choose ```3 - protect laptop```
![](https://i.imgur.com/GJ7fC0x.png)

### choose ```3 - demo mode```
![](https://i.imgur.com/XMY0g7T.png)


### if you get this message from the camera window
> Congratulations! It means all packages can work properly on your device. The model used in the demo mode is my personal recognition model (recognized model for Jet). Therefore, it is normally for your face to be recognized as a stranger via the demo model.

![](https://i.imgur.com/Wt7V0UB.png)

### Go to check your email while you signed in before
> This program is disgned for protect your laptop. When the device detect a stranger face in the protect mode, it will send the suspicious face to the user's email.
<br>

## Use Face Distant to recognize faces
### Record at least 20 faces first
```
Jet, what do you want do?
1 - record master data
2 - update model
3 - protect laptop
q - exit

>>> 1

# after recording master data

Jet, what do you want do?
1 - record master data
2 - update model
3 - protect laptop
q - exit

>>> 3

which mode do you want to use?
1 - face distance
2 - face model
3 - demo mode
b - back

>>> 1
```
<br>

## Build your own model
### Download the dataset
```
Seems like you have not download the artist dataset yet. 
Do you want to download it? (y/n)

>>> y
```

### Make sure your master data is more than 200 images

### Update the model
```
Jet, what do you want do?
1 - record master data
2 - update model
3 - protect laptop
q - exit

>>> 2
```

### Try your model
> The accuracy of your model is base on the amount of master data
```
Jet, what do you want do?
1 - record master data
2 - update model
3 - protect laptop
q - exit

>>> 3

which mode do you want to use?
1 - face distance
2 - face model
3 - demo mode
b - back

>>> 2
```
<br>

## Model Selection
> The result is in the jupyter notebook file - ```Model Selection.ipynb```
<br>

## DATA
### billboard Artist Data
-  The size of our dataset is ```194 MB```, contains ```10422``` images of faces.
-  The execute script is ```build_dataset.py```, it will call the crawler in ```data_updater.py``` to fetch the artist names on [Billboard Hot 100](https://www.billboard.com/charts/hot-100) and [Billborad Artist 100](https://www.billboard.com/charts/artist-100). And use the [Bings Search API](https://docs.microsoft.com/en-us/azure/cognitive-services/bing-web-search/) to search the images of the artists.
-  [Google Drive download link](https://drive.google.com/file/d/1TCha0-JlGMeuBoMgL0kehK_SsjQ1QKb7/view?usp=sharing)


### Master Data
-  The face data of the laptop owner.
- The demo model was trained by the face data of [@jet-chien](https://github.com/jet-chien) and our billboard artist data
- This data is not uploaded because it is the personal data
<br>

## Demo Video
[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/eVziLxWSmTo/0.jpg)](http://www.youtube.com/watch?v=eVziLxWSmTo)
<br>

## More Information

### File information
> More detail are written in the ```README.md``` in each folder
- ```face_ult``` : all of the main src code of image processing, face recoginize, data collection and model training are in this folder
- ```service/app``` : the src code for the execution of the program
- ```ult``` : some code of the utility function
- ```test``` : some useful script for testing the user's device
- ```gd_dataset.py``` : an api for downloading and unzip our billboard artist dataset
- ```build_dataset.py``` : an executed script for downloading and unzip our billboard artist dataset
- ```main.py``` : an executed script for running the whole program


### Laptop Protect Mode 1 - Face Distance
> The method of face recognition in this mode is using the api ```face_encodings()``` and ```compare_faces()``` in [face_recognition](https://github.com/ageitgey/face_recognition) by computing the difference between the encodings of faces. But this method is very inefficient in extracting the encoding of face through the laptop camera. Therefore, this mode is not good to use.

### Laptop Protect Mode 2 - Face Model
- High efficiency
- use the api ```cv2.dnn.readNetFromTorch()``` in [opencv-contrib-python](https://github.com/skvark/opencv-python) to get the encodings of faces
- Need great amount of face data to build a verbose SVC classifier model without overfitting

