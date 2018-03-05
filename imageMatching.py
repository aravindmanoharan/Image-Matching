import pandas as pd
import numpy as np
import itertools
from scipy import spatial
import csv

#	Calculating euclidean distances between two images
def euclideanDistance(x,y):
    return spatial.distance.cdist(x,y)

#	Extracts the keypoints, descriptors from the sift file of a particular image
def readingData(filename):
    data = pd.read_csv(filename, header = None) #	Using pandas to read the sift files
    data = data[0].str.split(" ")
    instance = data.iloc[0] #	The first line contains the total number of keypoints and the length of the descriptor vector for each keypoint
    instance = list(map(int, instance))
    data = data.drop(data.index[0])
    m = 0
    n = 8
    data_matrix = []
    for i in range(instance[0]):
        temp = []
        count = 0
        for j in range(m + 1,n): #	Extracting the descriptor vector for each keypoint which is given as a list of 128 integers in range [0,255]
            temp.append(data.iloc[j])
            del temp[count][-1]
            count += 1
        temp = list(itertools.chain(*temp))
        temp = list(map(int, temp))
        data_matrix.append(temp)
        m = n
        n = n + 8
    return data_matrix

#	To find the score between two images
def findingScore(sourceData,targetData):
    sourceData = np.array(sourceData)
    targetData = np.array(targetData)
    if np.array_equal(sourceData,targetData):
        return 0 #	Returns the score as 0 if both the images are same
    else:        
        euclDistance = euclideanDistance(sourceData,targetData)
        euclDistance = np.sort(euclDistance,axis = 1) #	  Sorting each rows to get the first two shortest distances
        euclDistance = euclDistance[:,[0,1]].T
        euclDistance = np.divide(euclDistance[0],euclDistance[1]) #	  Calculating the ration between the two shortest distances
        score = np.zeros((1,euclDistance.shape[0]))
        score = (euclDistance < 0.75).astype(float) #	It's a good match if the the ratio is less than 0.75
        return int(score.sum())

#	To find the first 5 closest match 
def closestMatch(matchScore,imageName,n):
    matchScore = np.array(matchScore)
    minIndex = matchScore.argsort()[-5:][::-1] #	Getting the indices of the first 5 maximum scores 
    closestMatch = matchScore[minIndex] #	Finding what are the scores of those 5 closest images
    imageName = np.array(imageName)
    closestImage = imageName[minIndex] #	Finding the image name of those 5 images
    normScore = [i*100/(max(closestMatch)+1) for i in closestMatch] #	Normalizing those 5 scores in the range of [0,100]
    newImage.append(imageName[n])
    for k in range(len(normScore)):
        newImage.append(closestImage[k])
        newImage.append(int(normScore[k]))
    return newImage 

filename = []
imageName = []
csvUpload = []
csvUpload.append(['ImageName','FirstMatchImage','FirstMatchScore','SecondMatchImage','SecondMatchScore','ThirdMatchImage','ThirdMatchScore','FourthMatchImage','FourthMatchScore','FifthMatchImage','FifthMatchScore'])
for i in range(1,151):
    name = "sift/IMG%03d.jpg.sift" % (i) #	  Creating a list which contains the directories to all the sift files
    filename.append(name)
    image = "IMG%03d.jpg" % (i) #	Creating a list which contains all the image names
    imageName.append(image)
    
for a,i in enumerate(filename):
    sourceData = readingData(i)
    matchScore = []
    newImage = []
    for b,j in enumerate(filename):
        targetData = readingData(j)
        matchScore.append(findingScore(sourceData,targetData))
        print(imageName[a],"comparing with",imageName[b],"...")
    csvUpload.append(closestMatch(matchScore,imageName,a))

with open("output.csv",'w') as dataUploading: #	Exporting the final output to a csv file
    wr = csv.writer(dataUploading)
    wr.writerows(csvUpload)
            
            