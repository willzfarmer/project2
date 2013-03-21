function [dst_matrix] = dstransform(image)

% read in the image and make it a nice little matrix
image_matrix=double(imread(image));

% get the dimensions of the matrix
[rows, cols] = size(image_matrix);

% get the largest dimension for the identity matrix
% although for this code, a square image is the intended input
n = max(rows, cols);

%DST template from the project
S = double(zeros (n , n )); %initialize S
for i = 1: n
    for j = 1: n
        a = (pi*(i-0.5)*(j-0.5))/n;
        S (i , j ) = sqrt(2/n)*sin(a);
    end
end

%Multiply with the image_matrix to obtain the transform
dst_matrix = uint8(S* image_matrix* S);
% to undo DST's effects:
% dst_matrix = uint8(S* S* image_matrix* S* S*);

imwrite(dst_matrix, 'dst.jpg');