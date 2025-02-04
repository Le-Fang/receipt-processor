# receipt-processor

This repository contains a webservice that fulfils the documented API listed in https://github.com/fetch-rewards/receipt-processor-challenge.git

To run this application, navigate to the root directory of this project, and run the following command to build the Docker image:

`docker build -t receipt-processor .`

After building the image, you can run the container using the following command (change the port number if 8000 is in use):

`docker run -d -p 8000:5000 receipt-processor`

Now the application shoule be accessible at http://localhost:8000