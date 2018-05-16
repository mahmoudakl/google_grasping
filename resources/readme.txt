
To get the newest google robot model and objects in your environment editor to drop in the bin, do:

- drop google_grasp robot in your $HBP/Models
- drop objects folder in your $HBP/Models
- add these lines to _rpmbuild/models.txt
	google_grasp
	objects/banana
	objects/bottle
	objects/can
	objects/cup
	objects/football
	objects/lightbulb
	objects/pin
	objects/rubberduck

- substitute $HBP/Models/libraries/model_library.json with the file in this repo
- go to $HBP/Models and run ./create_symlinks
- go to $HBP/user_scripts and run ./configure_nrp
- clear your browser cache and cookies
