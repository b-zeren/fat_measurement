import pydicom
import cv2 
import numpy as np
import matplotlib.pyplot as plt
import os
        

def load_slices(path,adjust_thickness=0):
    slices = [pydicom.read_file(path + '/' + s) for s in os.listdir(path)]
    print("Read files")
    slices.sort(key = lambda x: int(x.InstanceNumber))
    print("Sorted slices")
    if adjust_thickness:
        try:
            slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
        except:
            slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
        print("calculated thickness", slice_thickness)
        print("found thickness",slices[0].SliceThickness)
        print("adjusted thickness")
        for s in slices:
            s.SliceThickness = slice_thickness
    return slices

def load_singular_slice(path):
    slice=pydicom.read_file(path)
    return slice

def get_pixels_hu(scans):
    image = np.stack([s.pixel_array for s in scans])
    image = image.astype(np.int16)    # Set outside-of-scan pixels to 0
    # The intercept is usually -1024, so air is approximately 0
    image[image == -2000] = 0
    
    # Convert to Hounsfield units (HU)
    intercept = scans[0].RescaleIntercept
    slope = scans[0].RescaleSlope
    
    if slope != 1:
        image = slope * image.astype(np.float64)
        image = image.astype(np.int16)
        
    image += np.int16(intercept)
    
    return np.array(image, dtype=np.int16)

def convert_to_hu(slice):
    '''
    take a raw slice, return a numpy array containing pixel intensities in Hounsfield Units
    '''
    hu_slice=slice.RescaleSlope*slice.pixel_array+slice.RescaleIntercept
    return hu_slice

def display_scans(scans):
    '''
    takes list of pixel_arrays, displays them using matplotlib
    '''
    if len(scans)==1:
        plt.imshow(scans[0],cmap=plt.cm.gray)
        plt.show()
    else:
        plt.imshow(np.concatenate((scans),axis=1),cmap=plt.cm.gray)
        plt.show()

def filter_intensities(image,min_val,max_val):
    filtered=image.copy()
    default_value=image.min()
    filtered[filtered<min_val]=default_value
    filtered[filtered>max_val]=default_value
    return filtered

def show_hist(image):
    hist,bins=np.histogram(image,bins=200)
    plt.plot(bins[:-1],hist)
    plt.show()

def convert_to_grayscale(hu_scan):
    pixels=hu_scan
    img_2d = pixels.astype(float)
    img_2d_scaled = img_2d*(1/(pixels.max()-pixels.min())*255)
    img_2d_scaled = np.uint8(img_2d_scaled)
    return img_2d_scaled