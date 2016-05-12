Im = imread('test27.png'); 
flag = 1;
while flag 
	n = input('Please input the size of the filter(To end the program,input 0):');
	if n == 0
        flag = 0;
        fprintf('Exiting\n')
	else
		medianFilter(Im,n);
		averageFilter(Im,n);
	end
end


