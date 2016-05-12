function Im2 = medianFilter(Im,n)
[height,width] = size(Im);
Im1 = double(Im);
Im2 = Im1;
center = round((n+1)/2);
for i = 1:height-n+1
	for j = 1:width-n+1
		temp = Im1(i:i+n-1,j:j+n-1);
		ele = temp(1,:);
		for count = 2:n
			ele = [ele,temp(count,:)];
		end
		med = median(ele);
		Im2(i+center,j+center) = med;
	end
end

Im2 = uint8(Im2);
figure
subplot(2,1,1)
imshow(Im)
subplot(2,1,2)
imwrite(Im2,'test34.png')
imshow(Im2)
xlabel('median filtering')
end