# cisco_duo_helpdesk_app
For Duo MFA customers, this application provides a secure, web-based interface for helpdesk agents to verify the identity of individuals calling into the helpdesk. 
It leverages Duo's two-factor authentication API system to ensure that callers are who they claim to be, thereby enhancing security and 
preventing unauthorized access to sensitive information. Two methods of authentication are supported: Duo Push and Token (either hardware or from the Duo app).

## Contacts
* Rey Diaz
* Mark Orszycki
* Brandon Gordon

## Solution Components
* Authentication: Cisco Duo API
* Frontend: React JS
* Backend: FastAPI + Uvicorn (Python)

## Key Features
1. Duo Integration: Seamlessly integrates with Duo's API, enabling helpdesk staff to send a Duo push notification for user verification. 
2. User Verification: Allows helpdesk employees to search for a user (e.g., an executive) and initiate a Duo push notification to verify their identity during phone calls. 
3. Secure Branch Access: Incorporates a login system for the helpdesk, ensuring that only authorized personnel can use the application to initiate verification requests. 
4. Frontend Interface: Provides a user-friendly frontend, built with React.js, enabling staff to easily navigate and use the system. 
5. Backend API: Utilizes a robust FastAPI backend for handling authentication logic, API integration, and data processing.

## Installation/Configuration
### Backend
#### Retrieve Duo Credentials 
1. Follow the instructions under 'First Steps' to get your Duo Auth integration key, secret key and API hostname: https://duo.com/docs/authapi#first-steps.
2. Similarly, follow the instructions under 'First Steps' to get your Duo Admin integration key, secret key and API hostname: https://duo.com/docs/adminapi#first-steps.
The Grant Resource - Read permission is needed.
3. Clone this repository with git clone `git clone https://github.com/brandgor7/cisco-duo-helpdesk-app.git`.
4. Create and update .env (see below)
5. Proceed to 'usage' section.

#### Create and update .env
Create .env in backend/config/:
```script
cd backend/config
touch .env
open .env
```
Copy/Paste the .env variables and update accordingly:
```script
APP_NAME='Duo Manual Push Authentication'
APP_VERSION=1.0
LOGGER_LEVEL=DEBUG
DUO_API_URL=YOUR_API_HOSTNAME
DUO_IKEY=YOUR_DUO_INTEGRATION_KEY
DUO_SKEY=YOUR_DUO_SECRET_KEY
DUO_ADMIN_API_URL=YOUR_ADMIN_API_HOSTNAME
DUO_ADMIN_IKEY=YOUR_DUO_ADMIN_INTEGRATION_KEY
DUO_ADMIN_SKEY=YOUR_DUO_ADMIN_SECRET_KEY
```
* Note: APP_NAME and APP_VERSION are for auto-generated FastAPI docs at uvicorn_running_url/docs (i.e. http://127.0.0.1:8000/docs )

## Usage
### With Docker
#### 1. To build and start the containers, run: ``` docker-compose up --build ```
#### 2. Navigate to URL: ``` http://localhost:5173/ ```
#### 3. To stop the containers and remove them along with their network, run: ``` docker-compose down ```

### Without Docker
#### 1. Start Frontend
Terminal 1:
```script
cd frontend
npm install
npm run dev
```

#### 2. Start Backend
Terminal 2:
```scipt
cd backend
uvicorn main:app --reload
```

#### 3. Navigate to Frontend URL:
```script
http://localhost:5173/
```

# Screenshots


## Home:
![/IMAGES/Home.png](/IMAGES/Home.png)<br>

## App:
![/IMAGES/App.png](/IMAGES/App.png)<br>

## Endpoint Docs
![/IMAGES/endpoint_docs.png](/IMAGES/endpoint_docs.png)<br><br>

![/IMAGES/0image.png](/IMAGES/0image.png)


### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
