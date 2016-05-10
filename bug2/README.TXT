Hi, this is the improved solution compared to the previous one.

Thanks to Sandeep, I improved the algorithm for deciding how much angle to turn when robot hitting the s-line by using orientation.

And also this version can handle some other situations that cannot be handled by the initial version.

Please notice that to set the start and goal points, you have to change the encoding value start_x,start_y and goal_x,goal_y 

in the top of the script in bug2.py.

I did not do any changes for wallfollower.py.

Overall, this version can finally reach the goal in most cases. 


