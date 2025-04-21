import pytesseract
import keras
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from PIL import Image
import cv2

image = cv2.imread("C:\Users\AbinayasreeSomakumar\Downloads\pdf2png.zip\CALAINV-004")
greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)




