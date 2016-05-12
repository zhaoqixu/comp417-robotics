function Im2 = averageFilter(Im,n)
window = ones(n,n);%initialize the filter window
[height,width] = size(Im);

Im1 = double(Im);

Im2 = Im1;
center = round((n+1)/2);%the center of the window

for i = 1:height-n+1
	for j = 1:width-n+1
		temp = Im1(i:i+n-1,j:j+n-1).* window;%extract numbers of a window from (i,j) of Im1 and multiply with the window
		SUM = sum(sum(temp));%calculate the sum of the temp
		Im2(i+center,j+center) = SUM/(n*n);%calculate the average and assign the value to the center of the window
	end
end

Im2 = uint8(Im2);

%show the image before and after
figure
subplot(2,1,1)
imshow(Im)
subplot(2,1,2)
imshow(Im2)
xlabel('average filtering')
end

