# file-transfer

This project is based on the code provided in the echoClient/Server python files provided by Eric Freudenthal.

This project transfers files from the client to the server, a whole file name including the extension must be provided to the client for it to be able to determine what file it is that you want to send.

The server must be running before the client is launched or the client will throw an error and close, could be fixed to wait for connection but I can't possibly make the project any more graceful without creating a gracefulness black hole that would suck in all the gracefulness in the universe.

To see how graceful this project is, please refer to graceful.gif and multiply that gracefulness by about 2^96, and don't forget to thank Ron Swanson and Squidward for helping in testing of this project. 