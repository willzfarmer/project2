function [flipped_image] = flipped(image)

% read in the image and make a matrix
image_matrix=double(imread(image));

% get the dimensions of the matrix
[rows, cols] = size(image_matrix);

% get the largest dimension for the identity matrix
n = min(rows, cols);

% Preallocate for the id matrix:
T = zeros(n,n);

% generate an 'upside down' identity matrix
T = flipud(eye(n));

flipped_image=uint8(T*image_matrix); 
imwrite(flipped_image,'flipped.jpg');