I = imread('test9.jpg');
O = imadjust(I, [0 0.8], [0 1]);
figure;
imwrite(O, 'test36.jpg');
imshow(O); 