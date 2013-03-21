function [image_matrix] = dst_undo(image)

% read in the image and make it a nice little matrix
dst_matrix=double(imread(image));

% get the dimensions of the matrix
[rows, cols] = size(dst_matrix);

% get the largest dimension for the identity matrix
% although for this code, a square image is the intended input
n = max(rows, cols);

%DST template from the project
S = double(zeros (n , n )); %initialize S
for i = 1: n
    for j = 1: n
        a = (pi*(i-0.5)*(j-0.5))/n;
        S (i , j)  = (sqrt(2/n)*sin(a));
    end
end

%Multiply with the image_matrix to obtain the transform
image_matrix = uint8(S*dst_matrix*S*S);
% to undo DST's effects:
% dst_matrix = uint8(S* S* image_matrix* S* S*);

imwrite(image_matrix, 'dst.jpg');