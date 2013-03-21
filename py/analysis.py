#!/usr/bin/env python
'''
APPM 2360 Differential Equations Project Two
  |-Will Farmer
  |-Jeffrey Milhorn
  |-Patrick Harrington

This code takes the two given images and performs several
mathematical operations on them using matrix methods.
'''

import sys                       # Import system library
import scipy.misc                # Import image processing libraries
import numpy                     # Import matrix libraries
import matplotlib.pyplot as plt  # Import plotting libraries
import pp                        # Library for Parallel Processing

jobServer = pp.Server() # Create a new jobserver
jobs      = []          # List of jobs to complete

def main():
    # Open images for manipulation
    print('Opening Images')
    image1 = scipy.misc.imread('../img/photo1.jpg')
    image2 = scipy.misc.imread('../img/photo2.jpg')

    # Run manipulations on both images
    print('Generating Manipulations')
    manipulate(image1, '1')
    manipulate(image2, '2')

    # Visualize Determinants of DST Matrix
    print('Generating Determinant Graph')
    visualize_s()

    # Compress images using DST
    print('Compressing Images')
    jobs.append(
            jobServer.submit(compression,
                            (image1, '1', 0.5),
                            (create_grayscale, dst, create_S),
                            ('numpy', 'scipy.misc'))
            ) # Add a new job to compress our first image
    jobs.append(
            jobServer.submit(compression,
                            (image2, '2', 0.5),
                            (create_grayscale, dst, create_S),
                            ('numpy', 'scipy.misc'))
            ) # Add a new job to compress our second image

    # Analyze Compression Effectiveness
    print('Generating Compression Effectiveness')
    comp_effect(image1, image2)

    # Create Picture Grid
    print('Generating Picture Grid')
    mass_pics(image1, '1')
    mass_pics(image2, '2')

    for job in jobs:
        job() # Evaulate all current jobs

def manipulate(image, name):
    '''
    Manipulate images as directed
    1) Create grayscale image
    2) Produce horizontal shifts
    3) Produce Vertical/Horizontal Shifts
    4) Flip image vertically
    '''
    # Create grayscale
    g = create_grayscale(image.copy())
    scipy.misc.imsave('../img/gray%s.png' %name, g)

    # Shift Horizontally
    hs = shift_hort(g)
    scipy.misc.imsave('../img/hsg%s.png' %name, hs)

    # Shift Hort/Vert
    hs = shift_hort(g)
    vhs = shift_vert(hs.copy())
    scipy.misc.imsave('../img/vhsg%s.png' %name, vhs)

    # Flip
    flipped = flip(g)
    scipy.misc.imsave('../img/flip%s.png' %name, flipped)

def flip(image):
    '''
    flips an image
    Essentially just multiplies it by a flipped id matrix
    '''
    il = numpy.identity(len(image)).tolist()  # Creates a matching identity
    for row in il: # Reverses the identity matrix
        row.reverse()
    i       = numpy.array(il) # Turns it into a formal array
    return numpy.dot(i, image) # Dots them together

def shift_hort(image):
    '''
    Shift an image horizontally
    1) Create rolled identity matrix:
        | 0 0 1 |
        | 1 0 0 |
        | 0 1 0 |
    2) Dot with image
    '''
    i       = numpy.roll(numpy.identity(len(image[0])),
                    240, axis=0) # Create rolled idm
    shifted = numpy.dot(image, i) # dot with image
    return shifted

def shift_vert(image):
    '''
    Shift an image horizontally
    1) Create rolled identity matrix:
        | 0 0 1 |
        | 1 0 0 |
        | 0 1 0 |
    2) Dot with image
    '''
    i       = numpy.roll(numpy.identity(len(image)),
                    100, axis=0) # create rolled idm
    shifted = numpy.dot(i, image) # dot with image
    return shifted

def create_grayscale(image):
    '''
    Creates grayscale image from given matrix
    1) Create ratio matrix
    2) Dot with image
    '''
    ratio = numpy.array([30., 59., 11.])
    return numpy.dot(image.astype(numpy.float), ratio)

def shift_hort_color(image):
    '''
    Shift a color image horizontally
    1) Create identity matrix that looks as such:
        | 0 0 1 |
        | 1 0 0 |
        | 0 1 0 |
    2) Dot it with image matrix
    3) Return Transpose
    '''
    # Create an identity matrix and roll the rows
    i       = numpy.roll(
            numpy.identity(
                len(image[0]))
            , 240, axis=0)
    shifted = numpy.dot(i, image) # Dot with image
    return numpy.transpose(shifted) # Return transpose

def compression(image, name, p):
    '''
    Compress the image using DST
    '''
    g = create_grayscale(image.copy()) # Create grayscale image matrix copy
    t = dst(g)  # Acquire DST matrix of image
    (row_size, column_size) = numpy.shape(t) # Size of t
    for row in range(row_size):
        for col in range(column_size):
            if (row + col + 2) > (2 * p * column_size):
                t[row][col] = 0 # if the data is above a set line, delete it
    scipy.misc.imsave('../img/comp%s.png' %name, dst(t))

def dst(image):
    '''
    If given a grayscale image array, use the DST formula
    and return the result
    Uses this method:
        image = X
        DST   = S
        Y = S.(X.S)
    '''
    rows    = numpy.dot(image, create_S(len(image[0])))
    columns = numpy.dot(create_S(len(image)), rows)
    return columns

def create_S(n):
    '''
    Discrete Sine Transform
    1) Initialize variables
    2) For each row and column, create an entry
    '''
    new_array = []  # What we will be filling
    size      = n
    for row in range(size):
        new_row = []    # New row for every row
        for col in range(size):
            S = ((numpy.sqrt(2.0 / size)) * # our equation
                 (numpy.sin((numpy.pi * ((row + 1) - (1.0/2.0)) *
                     ((col + 1) - (1.0/2.0)))/(size))))
            new_row.append(S) # Append entry to row list
        new_array.append(new_row) # append row to array
    return_array = numpy.array(new_array)
    return return_array

def mass_pics(image, name):
    '''
    Create a lot of compressed Pictures
    '''
    answer = raw_input('Create .gif Images? (y/n) ')
    if answer == 'n':
        return None # It takes a while, so it's optional
    domain = numpy.arange(0, 1.01, 0.01) # Range of p vals
    for p in domain:
        jobs.append(
                jobServer.submit(compression,
                    (image, 'array_%s_%f' %(name, p), p),
                    (create_grayscale, dst, create_S),
                    ('numpy', 'scipy.misc'))
                ) # For each value of p, add a new compression job

def visualize_s():
    '''
    DST
    Visualize the discrete sine transform equation implemented below.
    Uses matplotlib to create graph
    '''
    nrange   = numpy.arange(1, 33, 1) # Create values range [1,32] stepsize 1
    det_plot = plt.figure() # New matplotlib class instance for a figure
    det_axes = det_plot.add_axes([0.1, 0.1, 0.8, 0.8]) # Add axes to figure
    yrange   = [] # Create an empty y range (we'll be adding to this)
    for number in nrange:
        array = create_S(number)    # Get a new array with size n
        yrange.append(numpy.linalg.det(array)) # append determinant to yrange
    det_axes.plot(nrange, yrange, label='Set of determinants') # Create line
    det_axes.plot(nrange, nrange*0, 'k:')   # Also create line at y=0
    det_axes.legend(loc=4) # Place legend
    plt.xlabel('Size of Discrete Sine Transform Matrix') # Label X
    plt.ylabel('Determinant of Matrix') # Label Y
    plt.title('Size of Matrix vs. its Determinant') # Title
    plt.savefig('../img/dst_dets.png') # Save as a png

def comp_effect(image1, image2):
    '''
    Analyzes compression effectiveness
    If the image already exists, it will not run this
    '''
    try:
        open('../img/bitcount.png', 'r')
        open('../img/bitrat.png', 'r')
        print('	|-> Graphs already created, skipping.\
                (Delete existing graphs to recreate)')
        # If it already exists, don't create it. (It takes a while)
    except IOError:
        g1 = create_grayscale(image1.copy()) # Create grayscale from copy of 1
        g2 = create_grayscale(image2.copy()) # Create grayscale from copy of 2

        domain1 = numpy.arange(0.0, 1.01, 0.01) # Range of p values
        domain2 = numpy.arange(0.0, 1.01, 0.01) # Range of p values

        # Parallelize System and generate range
        count_y1, rat_y1 = jobServer.submit(get_yrange,
                        (domain1, g1),
                        (dst, clear_vals, create_S),
                        ('numpy', 'scipy.misc'))()
        count_y2, rat_y2 = jobServer.submit(get_yrange,
                        (domain2, g2),
                        (dst, clear_vals, create_S),
                        ('numpy', 'scipy.misc'))()

        count_plot = plt.figure() # New class instance for a figure
        count_axes = count_plot.add_axes([0.1, 0.1, 0.8, 0.8]) # Add axes
        count_axes.plot(domain1, count_y1, label='Image 1')
        count_axes.plot(domain2, count_y2, label='Image 2')
        count_axes.legend(loc=4)
        plt.xlabel("Value of p")
        plt.ylabel("Number of Non-Zero Bytes")
        plt.title("Compression Effectiveness")
        plt.savefig("../img/bitcount.png")

        ratio_plot = plt.figure() # New class instance for a figure
        ratio_axes = ratio_plot.add_axes([0.1, 0.1, 0.8, 0.8]) # Add axes
        ratio_axes.plot(domain1, rat_y1, label='Image 1')
        ratio_axes.plot(domain2, rat_y2, label='Image 2')
        ratio_axes.legend(loc=4)
        plt.xlabel("Value of p")
        plt.ylabel("Ratio of Non-Zero Bytes to Total Bytes")
        plt.title("Compression Effectiveness")
        plt.savefig("../img/bitrat.png")

def get_yrange(domain, g):
    bit_count = [] # Range for image
    bit_ratio = []
    for p in domain:
        t = dst(g.copy()) # Transform 1
        initial_count = float(numpy.count_nonzero(t))
        clear_vals(t, p) # Strip of high-freq data
        final_count = float(numpy.count_nonzero(t))
        bit_count.append(final_count) # Append number of non-zero entries
        bit_ratio.append(final_count / initial_count)
    return bit_count, bit_ratio

def clear_vals(transform, p):
    '''
    Takes image and deletes high frequency
    '''
    (row_size, column_size) = numpy.shape(transform) # Size of t
    for row in range(row_size):
        for col in range(column_size):
            if (row + col + 2) > (2 * p * column_size):
                transform[row][col] = 0 # if the data is above line, delete it
    return transform

if __name__ == '__main__':
    sys.exit(main())
