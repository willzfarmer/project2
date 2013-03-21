function [vshifted_image] = vshift(image)

% r is the number of rows we want to shift by
r = 100;

% read in the image and make it a nice little matrix
image_matrix=double(imread(image));

% get the dimensions of the matrix
[rows, cols] = size(image_matrix);

% get the largest dimension for the identity matrix
n = min(rows, cols);

% Preallocate for the id matrix:
T = zeros(n,n);

% generate a generic identity matrix
id = eye(n);

%fill in the first c cols of T with the last c cols of id
T(1:r,:)=id(n-(r-1):n,:);
%fill in the rest of T with the first part of id
T(r+1:n,:) = id(1:n-r,:);

vshifted_image=uint8(T*image_matrix);

imwrite(vshifted_image,'vshifted.jpg');
    
    
