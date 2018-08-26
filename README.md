# Brute Force Image Matching with SIFT Descriptors and Ratio Test

This project is about matching images and finding the closest pairs. There are 150 images and their corresponding sift [1] features for each images. The goal is to find 5 closest images for each images.

###### Why do we need matches in pair?
<img width="696" alt="screen shot 2018-03-02 at 11 45 24 am" src="https://user-images.githubusercontent.com/35612880/36915829-4ab511d2-1e0f-11e8-906d-527b03bd1c7d.png">
From the Figure, we can see that if we have closest pair of images, we can triangulate the 3D points from the image pairs.

## Structure of SIFT files
The file structure starts with 2 integers giving the total number of keypoints and the length of the descriptor vector for each keypoint (128). Then the location of each keypoint in the image is specified by 4 floating point numbers giving subpixel row and column location, scale, and orientation (in radians from -PI to PI).  Obviously, these numbers are not invariant to viewpoint, but can be used in later stages of processing to check for geometric consistency among matches. Finally, the invariant descriptor vector for the keypoint is given as a list of 128 integers in range [0,255]. To read more about the structure of SIFT files and how to read them, please download [SIFT demo](http://www.cs.ubc.ca/~lowe/keypoints/siftDemoV4.zip).

## Implementation
When comparing two images, the matches are identified by finding the 2 nearest neighbors (using euclidean distance) of each keypoint from the first image among those in the second image, and only accepting a match if the distance to the closest neighbor is less than 0.75 of that to the second closest neighbor. The threshold of 0.75 can be adjusted up to select more matches or down to select only the most reliable. We need to find all the matches for all the keypoints of the first image. The total number of matches gives the score between those two images. So comparing one image with all the other images, the image which has the maximum score is the most reliable match. Since the goal is to find 5 closest images, the top 5 images which has the maximum scores are considered to be the 5 closest images.

## Output
The output file is a CSV file. It has exactly 151 rows and 11 columns. First row is a header and rest 150 rows are reserved for the 150 input images.
Column headers:
1. **ImageName**: Name of image file.
2. **FirstMatchImage:** Name of the image which is the first match.
3. **FirstMatchScore:** The score of the first match in range [0,100].
4. **SecondMatchImage:** Name of the image which is the second match.
5. **SecondMatchScore:** The score of the second match in range [0,100].
6. **ThirdMatchImage:** Name of the image which is the third match.
7. **ThirdMatchScore:** The score of the third match in range [0,100].
8. **FourthMatchImage:** Name of the image which is the forth match.
9. **FourthMatchScore:** The score of the fourth match in range [0,100].
10. **FifthMatchImage:** Name of the image which is the fifth match.
11. **FifthMatchScore:** The score of the fifth match in range [0,100].

## Reference
[1] David G Lowe. Distinctive image features from scale-invariant keypoints. *International journal of computer vision*, 60(2):91–110, 2004.
