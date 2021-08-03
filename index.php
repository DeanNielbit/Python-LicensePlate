<?php 

/*show original plate*/
echo 'original image: <img src="uploadimage/image1.jpg" width="50%"><br /><br />';


/*show modified plate*/
$command = system('python main.py');
$output = shell_exec($command);
echo $output;



?>