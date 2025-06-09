# Rare Hash Finder

### Description

This project is responsible for discovering the rarest hashes by generating random character strings and computing their SHA-256 hashes. When a hash meets the rarity criteria—starting with at least 25 consecutive zeros or ones—it is submitted to the Rare Hashes Website.

The service communicates with the web server using HTTP POST requests to upload valid rare hashes.

The project is part of a system consisting of three microservice components:

- A [web interface](https://github.com/YaroslavWork/RareHashesWebsite) displaying the rarest hashes found.
- A [Telegram bot](https://github.com/YaroslavWork/RareHashesTelegramBot) that notifies users about new rare hashes.
- An automated searching bot that scans and uploads rare hashes to the database.

This combination highlights advanced backend processing, database management, and real-time user notification integration.

*"Do one thing, and do it well."*

---

### Installation (for Linux)

1. Install Rare Hash Website (optional*):

    [Follow the installation process.](https://github.com/YaroslavWork/RareHashesWebsite?tab=readme-ov-file#installation-for-linux)

    *If my project is running, you can launch this bot and send hashes to my server by default.*

2. Configure YAML file (optional):
    
    Example config.yml:
    ```yaml
    # Made by YAr (github: YaroslavWork)

    # My site to write some rarest hashes (do not change this unless we change our domain)
    url: https://158.220.119.11:6798/write

    # Your nickname to see in my website
    nickname: pythonBot

    # How many letters the word has
    word_length: 32

    # How many 0 or 1 has in the start of sequence (to save in my site number must be at least 25)
    min_repetitions: 25

    # In case when site is not working
    save_file: .//save.txt
    ```

---

### Usage

1. [Follow the usage process.](https://github.com/YaroslavWork/RareHashesWebsite?tab=readme-ov-file#usage) (optional)

2. Create an image:
    ```sh
    docker build -t hash-bot .
    ```

3. Create and run a container:
    - To run one instance:
        ```sh
        docker run --rm -it --name hash-bot-cont hash-bot
        ```
    - Or multiple instances (with Docker Compose):
        ```yaml
        version: '3'
        services:
        worker:
            build: .
            deploy:
            replicas: 4  # Run 4 independent instances
            environment:
            - WORKER_ID=${WORKER_ID}
        ```
        ```
        docker-compose build
        docker-compose up --scale worker=4
        ```
---

### Project Structure

The project is organized in the **main.py** file. Additionally, this project has:

- **config.yml** - to configure this bot.
- **Dockerfile** and **requirements.txt** - Used to build and run the application in Docker containers.
---

### Dependencies

- Python 3.10.9+
- All Python modules are listed in **requirements.txt**.

---

### License

MIT License - see the `LICENSE` file for details.

---

### Demo

If my server isn’t being used for something else, the project should be running [here](https://158.220.119.11:6798/). I created my own certificate for this project. Web browsers will warn you about this, and you will need to confirm to proceed to the page.

**[Rare Hashes Web Server - Demo](https://158.220.119.11:6798/)**