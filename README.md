# sHEMO: Smartphone Spectroscopy for Blood Hemoglobin Level Monitoring in Smart Anemia-Care

# Concepts Involved
Computer Vision, Medical Imaging, Machine Learning, Software Programming

# Requirements
Python 3.6, OpenCV 4.0, Microsoft Excel 2013

# A Brief Overview
Anemia occurs due to low blood hemoglobin levels, and for its mass screening, both invasive and smart anemia-care techniques are used. However, significant drawbacks include high costs, lack of state-of-the-art facilities, invasive techniques, and lack of smartphone implementation, using additional equipment and non-autonomous functioning, for smart anemia-care techniques. The paper proposes a novel, autonomous, smart anemia-care technique to address these problems in the form of a spectroscopy based blood hemoglobin level monitoring model. This approach uses a smartphone camera as a sensor. It quantifies the hemoglobin level based on the region of interest’s color spectroscopy, which is the conjunctival pallor, extracted autonomously. Anemia is diagnosed if the predicted hemoglobin level is < 11.5 g dL−1. For easy smartphone implementation, the proposed model uses image analysis techniques to estimate the hemoglobin level. Our model reports an accuracy of ±0.32 g dL−1, sensitivity of 89% compared to the actual blood hemoglobin levels (n = 65 participants). Also, the model remains robust to a wide range of illumination and the type of device used. It thereby establishes itself as a reliable and suitable replacement for the blood-based laboratory hemoglobin tests by leveraging the feature of at-home diagnosis of anemia.
<p align="center">
  <img width="860" height="400" src="https://user-images.githubusercontent.com/59502132/143024441-880bf7ec-4a72-4710-9ec0-bc70f9500059.png">
</p>

# Process Flow of sHEMO
There are three main phases involved: Phase 1: Extracting the Region of Interest (ROI), Phase 2: Performance Measure, and Phase 3: sHEMO Smartphone Application. In Phase 2, a novel and efficient algorithm called FANIAD (Fully Autonomous Non-Invasive Anemia Detection) is proposed. In the following we explain each phase in detail along with the smart
anemia-care.
<p align="center">
  <img width="660" height="500" src="https://user-images.githubusercontent.com/59502132/143020787-48b8aee6-398f-4de5-b765-ff6ea1f54631.png">
</p>

# Step-wise explanation of the functioning of sHEMO
## Step 1:
Capture an image of an eye with the conjunctiva area visible. A good snapshot is preferred for the code to detect the eye, preferably at a distance of 10 – 12cm. The room should be normally lighted.

## Step 2:
The “haarcascade eye detector” detects the eye and encloses it within a rectangle. If the haarcascade detector fails to detect an eye, it displays “No eye detected” message and prompts the user to take another image.
<p align="center">
  <img width="150" height="150" src="https://user-images.githubusercontent.com/59502132/143018173-34df4550-a345-4b49-8bf1-7d6fda573195.jpg">
</p>

## Step 3:
For getting the centre of the pupil, the SimpleBlobDetector() from OpenCV library is used.
<p align="center">
  <img width="150" height="150" src="https://user-images.githubusercontent.com/59502132/143018509-83709711-b5f9-40d8-8ef0-cfd3a447a730.jpg">
</p>

## Step 4:
The top 25% of the image is removed, since it is mostly comprised of the eyebrows.g. We obtain our required point ~3mm down from centroid (Let us say (cX, cY)). Now, we remove the part of the image above the row cX and are left with only the focused conjunctiva region.
<p align="center">
  <img width="150" height="150" src="https://user-images.githubusercontent.com/59502132/143018522-eb7365db-8ccb-43be-a5a8-c246613f568d.jpg">
</p>

## Step 5:
Now, once we have the above reduced ROI region, we use the Modified Canny Edge detection technique to get the edges of the above image (The Modified Canny Edge detection used here is explained below).
<p align="center">
  <img width="150" height="150" src="https://user-images.githubusercontent.com/59502132/143018946-cb5ce120-d6ab-4406-8e7a-df5711b6a775.png">
</p>

## Step 6:
We then loop through each row and each column of the above image (starting from the top left corner and iterating downwards) and every time a white pixel is detected, the entire column is filled with white. The advantage is we get the total upper portion of the edge as complete white and lower portion as black. And after we obtain it we have simply converted the white region into black region and black region to white region (because computer treats black as an object).
<p align="center">
  <img width="150" height="150" src="https://user-images.githubusercontent.com/59502132/143019405-4f309a48-dbee-4510-ad0e-2a6af7ea4493.png">
</p>

## Step 7:
This if we observe carefully is actually our mask. So we just subtract the mask from the original RGB image to get our required Region of Interest (ROI).
<p align="center">
  <img width="150" height="150" src="https://user-images.githubusercontent.com/59502132/143019506-573c8461-aa53-48cd-945d-6a3e67f08be1.jpg">
</p>

## Step 8:
Small rectangles from the obtained ROI are extracted and the RGB values from them are extracted and fed into a logistic regression formula, which extracts the required blood Hgb value.
<p align="center">
  <img width="760" height="400" src="https://user-images.githubusercontent.com/59502132/143025469-b0993f7d-7e7f-4280-b366-d75d70ecca2a.png">
</p>


# Results:
## Some extracted conjunctiva images
<p align="center">
  <img width="860" height="300" src="https://user-images.githubusercontent.com/59502132/143023932-5df3b70c-febd-49ff-9020-b0addc290109.png">
</p>

## Analytical Results
<p align="center">
  <img width="760" height="400" src="https://user-images.githubusercontent.com/59502132/143020640-d373ef0a-77de-4665-bc9c-381228b5a35a.png">
</p>

## Robustness to Light, Distance and Device Platform
<p align="center">
  <img width="760" height="400" src="https://user-images.githubusercontent.com/59502132/143020707-9b3dc196-bc91-48dd-ac49-1bc4d6f91a03.png">
</p>

## Effectiveness of the Proposed Modified Canny Edge  Detection Technique
We have compared all the edge detection techniques namely Canny Edge, Modified Canny Edge, Holistically Nested Edge Detection, Sobel X, Sobel Y. The best results have been given by Modified Canny Edge Detection. Following shows the comparison between traditional canny edge and our proposed modified canny edge.
<p align="center">
  <img width="460" height="300" src="https://user-images.githubusercontent.com/59502132/143023062-e200f6f8-ea1b-4df6-97aa-f13ee3fb385a.png">
</p>

# Citation
If you find this work useful, use the code or the results in your research and academic work, consider citing the following:
```
@ARTICLE{9293134,
author={Ghosal, Sagnik and Das, Debanjan and Udutalapally, Venkanna and Talukder, Asoke K. and Misra, Sudip},
journal={IEEE Sensors Journal},
title={sHEMO: Smartphone Spectroscopy for Blood Hemoglobin Level Monitoring in Smart Anemia-Care},
year={2021},
volume={21},
number={6},
pages={8520-8529},
doi={10.1109/JSEN.2020.3044386}}
```
