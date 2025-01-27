# Networks
# Peer-to-Peer Video Sharing System

This project implements a basic network-based system for video sharing and client-server communication. It includes a **server** for managing client registrations and video metadata, and a **client** for interacting with the server and other clients.

## Features
- **Server**:
  - Handles client registration and stores metadata about shared videos.
  - Processes commands for video downloads, registration, and queries.
  - Manages notifications for server disconnections and client activities.
- **Client**:
  - Shares local videos with other clients using a local server.
  - Downloads videos from other clients through a centralized server.
  - Communicates with the server to send commands and handle notifications.

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/YourUsername/PeerToPeerVideoSystem.git
   cd PeerToPeerVideoSystem

2. **Install Dependencies**:
   Ensure you have Python 3.x installed. If additional dependencies are required, you can install them using:
   ```bash
   pip install -r requirements.txt

3. **Set Up Folders**:
   Ensure the following folders exist in the project directory:
   - `videos_compartidos`: Contains videos available for sharing.
   - `videos_recibidos`: Stores videos downloaded from other clients.

4. **Run the Server, Run the Client**:
   Start the server in a terminal to listen for incoming connections:
   ```bash
   python server.py
   python client.py

5. **Interact with the Client**:  
   Use the client terminal to send commands to the server or interact with other clients. Examples of commands:  
   - `INSC <client_name> <IP_address> <listening_port>`: Register the client with the server.  
   - `VIDEOS <client_name> <number_of_videos> <video_list>`: Share a list of available videos.  
   - `DESCARGAR <video_name>`: Request to download a video from another client.  
   - `INFO`: Retrieve information about registered clients and shared files.

## Notes and Limitations
- The server requires a `bd_clientes.txt` file for initialization, containing client information. Ensure this file is present and correctly formatted.
- The client-server communication relies on specific command formats. Any deviation may result in errors.
- The project is designed for local network testing and may require adjustments for broader network compatibility.
- Error handling is basic and may need enhancements for production-level reliability.
- Directories for file sharing (`videos_compartidos`) and received files (`videos_recibidos`) are automatically created but must have appropriate permissions.














