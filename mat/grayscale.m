function gray_image=grayscale(image)
% This is a function to take an image in jpg form and put it into grayscale

% This reads in the image
image_matrix=imread(image);

% get the dimensions
[rows,columns,~]=size(image_matrix); 

% preallocate
gray_image = zeros(rows,columns);
for a=1:rows;
    for b=1:columns; 
            gray_image(a,b)=0.3*image_matrix(a,b,1)...
                +0.59*image_matrix(a,b,2)...
                +0.11*image_matrix(a,b,3);
    end 
end
imwrite(uint8(gray_image),'name.jpg')

end