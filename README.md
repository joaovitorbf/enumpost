# EnumPOST
Quick web user enumeration via HTTP POST requests.

A single script Python tool for enumerating users on a vulnerable POST request form.  
Uses multiple parallel processes to quickly send login requests and check if the page has changed or not, thus finding valid usernames. Pretty nice for CTFs.  
This repository also has a simple vulnerable pseudo-login page for testing.

## Installation
Runs on Python 3 and depends on urllib3 and requests.

    $ git clone https://github.com/joaovitorbf/enumpost.git
    cd ./enumpost
    pip install urllib3 requests

## Usage
    enumpost.py [-h] [-c cnt] [-v] [-s]
                   wordlist url payload [payload ...] failstr

    POST request user enumeration tool

    positional arguments:
      wordlist    username wordlist
      url         the URL to send requests to
      payload     the POST request payload to send
      failstr     failure string to search in the response body

    optional arguments:
      -h, --help  show this help message and exit
      -c cnt      process (thread) count, default 10, too many processes may cause
                  connection problems
      -v          verbose mode
      -s          stop on first user found
      
**Payload format:**  
`"field1:value1" "field2:value2"`  
Use {USER} to mark the value that will be replaced with the wordlist usernames:  
`"userfield:{USER}"`

 ## Examples
 Testing index.php on localhost with fields "username", "password", "submit" and failure string "Username does not exist" using the usernames.txt wordlist. The script will mark a username as valid if the response body doesn't have the failure string in it:
 
     ./enumpost.py usernames.txt http://localhost/index.php "username:{USER}" "password:123" "submit:Enter" "Username does not exist"
     
Testing the page "login" on "vulnerablewebsite.notadomain" with fields "user", "apitoken" and failure string "Invalid user" using the "/etc/opt/wlists/users.txt" wordlist. The script will mark a username as valid if the response body doesn't have the failure string in it:

    ./enumpost.py /etc/opt/wlists/users.txt httpp://vulnerablewebsite.notadomain/login "user:{USER}" "apitoken:987654321" "Invalid user"
    
## Disclaimer and licensing
Don't use this script on servers you don't have permission to spam requests, enumerate users and all the other stuff you shouldn't be doing to someone else's server. This script will probably also make the web server's access log explode.

Do whatever with my code. I believe that makes it MIT licensed? Never really understood software licensing.
