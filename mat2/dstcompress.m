function [dst_matrix]=dstcompress(image)

%input DST for compression:
dst_matrix=uint8(imread(image));

% get the dimensions of the matrix
[rows, cols] = size(dst_matrix);

% get the largest dimension for the identity matrix
n = min(rows, cols);


p = 0.5;
%when p=0 , no data are saved
%when p=1 , all data are saved
for i = 1: n
    for j = 1: n
        if i +j > p *2* n
            dst_matrix (i , j ) =0;
        end
    end
end

imwrite(dst_matrix, 'dst.jpg');