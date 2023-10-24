# CEX Arbitrage

CEX Arbitrage is a tool designed to identify and leverage pricing discrepancies between different cryptocurrency exchanges.

## Getting Started

These instructions will cover usage information for the Docker container and how to get the application running.

### Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed the latest version of [Docker](https://docs.docker.com/get-docker/).

### Running CEX Arbitrage with Docker

Follow these steps to get your application running with Docker:

1. **Clone the repository**

   First, clone this repository to your local machine. You can do this by running:

   ```bash
   git clone https://github.com/lucastakara/cex_arbitrage_searcher.git

Replace the URL above with the URL of your repository. Navigate to the cloned directory using:
   ```bash
    cd cex_arbitrage
``` 

1. **Build the Docker image**

Build your Docker image using the following command. Be sure to replace your-username with your Docker Hub username 
and cex_arbitrage with your preferred image name.
```bash
docker build -t cex_arbitrage .
```
This command reads the Dockerfile in the current directory and builds a Docker image based on its instructions.

2. **Run the Docker container**

Once the image has been built, run it using the following command:
```bash
docker run -p 5000:5000 cex_arbitrage
```
This command runs the container in detached mode, with the local port 5000 mapped to the container's port 5000. 
The application should now be running and accessible at http://localhost:5000.


#### Usage
To use CEX Arbitrage, follow these steps:

Open a web browser and navigate to:
http://localhost:5000

The web interface should now display the application, providing real-time insights and opportunities for cryptocurrency arbitrage.