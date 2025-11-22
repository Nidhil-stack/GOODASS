# ssh-key-manager
A quick utility to set ssh permissions to multiple servers

Create the config file like the one in the example then execute the wizard 

If you want to use an ssh key to connect to your servers, place a key.pem file in the folder with the main.py script, also add the key (the public part) as a user in the config.yaml file and give it admin privileges.
In this way (if the key is not already registered on the files) the program will ask for the password only the first time you connect to each host, once that key is added the you won't need any password.

# TODO features:
- move the default position of the ssh key file, also allow user to specify it
- add detatched mode, to be able to automate it
- add a small TUI for ease of use
- add the possibility to generate and edit the configs from inside the program
