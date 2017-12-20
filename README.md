LINKS API
====
A pastebin service to upload/share in a simple and fast way files, pieces of code/configuration,
etc..
The service is presented as a restful set of APIs written using the python Flask restful framework.
Add to your bashrc/zshrc the magic _nopaste_ alias to start sharing your snippets:

    alias nopaste = "curl -F c=@- https://IP:PORT/api/links"

The main features of this little webserver are the following:


* Upload a file

    cat $FILE | curl -F file=@- http://localhost:5000/api/links

* Show an uploaded file:

    curl -i http://localhost:5000/<URL>

* Show all the links present on the server (admin purposes: require authentication)

    curl -i -u user:password -X GET http://localhost:5000/api/links

* Show the helper (with curl or in a web browser)

    curl -i http://localhost:5000

* Show file metadata 

    curl -i http://localhost:5000/api/link/<ID>

* Delete a file

     curl -i -u fmount:fmount -X DELETE http://localhost:5000/api/link/<ID>


* Drop all links (delete files and clear the db table) **REQUIRE AUTH**

    curl -i -u fmount:fmount -X DELETE http://localhost:5000/api/links


USER API
===

* Create a user

    curl -i -X POST -H "Content-Type: application/json" -d '{"username":"fmount","password":"fmount"}' http://localhost:5000/api/users

* Get a user (admin only)

    curl -i -u admin:admin -X GET http://localhost:5000/api/user/<ID>

* Delete a user (admin only)

    curl -i -u admin:admin -X DELETE http://localhost:5000/api/user/<ID>



TESTS
===

* Massive file upload

    while true; do for i in $(ls); do  cat $i | curl -F file=@- http://localhost:5000/api/links; sleep 1; done; done

KNOWN ISSUES
===


TODO
===
* Put db in /var/lib/nopaste by default

