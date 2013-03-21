function [hshifted_image] = hshift(image)

% c is the number of cols we want to shift by
c = 240;

% read in the image and make it a nice little matrix
image_matrix=double(imread(image));

% get the dimensions of the matrix
[rows, cols] = size(image_matrix);

% get the largest dimension for the identity matrix
n = max(rows, cols);

% Preallocate for the id matrix:
T = zeros(n,n);

% generate a generic identity matrix
id = eye(n);

%fill in the first c cols of T with the last c cols of id
T(:,1:c)=id(:,n-(c-1):n);
%fill in the rest of T with the first part of id
T(:,c+1:n) = id(:,1:n-c);

hshifted_image=uint8(image_matrix*T);

imwrite(hshifted_image,'hshifted.jpg');
    
    