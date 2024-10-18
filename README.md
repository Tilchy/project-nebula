## Disclaimer

Repository is in active development!

## Description

Social connections where people could insert info about important people in their lives and when they were last in contact with them, what they were talking about, was the last interaction positive or negative with them, also maybe gather data if they were happy or sad that day so maybe include mood tracking.

## Features

✔ **PASSWORD_GENERATOR**
Simple password generator

✔ **REGISTER**
Enables users to register to use the API

✔ **LOGIN**
Enables users to login to retrieve Access Token and Refresh Token to use the API

✔ **JWT**
Generation of Access Token and Refresh Token + Verification

✔ **ROLES**
Enables different user types.
IE -> Admin, Basic User, Pro User (paying)
Admins are able to create and delete roles.

✔ **USER_MANAGEMENT** (Partial)
Enables Admins to manage users

✔ **SOCIAL_CONNECTIONS** (Partial)
Enables users to insert when were they last in contact with a person

**MOOD**
Daily mood tracking. Happiness tracker…

**JOURNAL**
Not exactly journal, but user can describe their day by predefined, words or phrases..

**WEATHER**
Gets weather for location for data analytics purposes. Complements journal, mood and connections tracking.

Roadmap:

**NOTIFICATION SYSTEM**
By Email
By Push Notification
By other channels? (Discord, WhatsApp, Telegram...)

## How to run the project?

### Prerequisites

-   You must have docker installed on your system.
-   You must create .env, you should use '.env.example' file in the repository.

### Run

-   `docker compose up -d`

### Remove

-   `docker-compose down --rmi all -v`

### Access

-   Swagger is accessible at http://localhost:8000/docs
-   You can also use Postman or curl to execute API
-   Or if you use vscode you can install extension the following extension https://marketplace.visualstudio.com/items?itemName=humao.rest-client
-   And run .http files in the requests folder
