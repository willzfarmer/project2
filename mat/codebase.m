im1_int  = imread( 'photo1.jpg' );   % Open the file to matrix in integer form
im1_flt  = double(im1_int);          % Convert to float
im1_size = size(im1_flt)

im1_gray = rgb2gray(im1_int);
grsize = size(im1_gray)

I = double(eye(grsize(1), grsize(2)))
im1_sh = dot(circshift(I, 5), double(im1_gray));
imshow(im1_sh)
