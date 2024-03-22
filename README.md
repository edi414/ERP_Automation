# Robot: ERP Automation
 A comprehensive automation solution for inventory management, pricing, and product enrichment within a supermarket ERP.

## About this Project

The idea of the Robots is:

_"To be a central automation for extraction and processing of important reports for the management of prices, stock, and catalog of the Supermarket"._

**PS:** Within this project, there are several Scripts that act in a particular way communicating with local and online databases.

<!-- **On the Media 🤩:** A [review](https://youtu.be/nu8mwGZUBFU) about this app (pt-BR 🇧🇷). (remove this part) -->

## Why?

This project is very important for the efficiency of the company, saving precious time for employees who were previously responsible for performing the entire process executed by the Robot. For me, this project gives me a lot of pride because it is a milestone in my career as a developer and certainly means a lot to the team that previously performed these processes and today can dedicate their precious time to more strategic activities.

Email-me: edivaldo414@gmail.com

Connect with me at [LinkedIn](https://www.linkedin.com/in/edivaldo-bezerra/).

Also, you can use this Project as you wish, either for study, for making improvements, or earning money with it!

It's free!

# Price Extract

https://github.com/edi414/ERP_Automation/assets/80610321/09f24308-127b-483f-9f80-c7745f461f17

## Some Observations about this Robot

1 - This robot is from the RPA class of robots and does not have a graphical interface, its execution is done via task scheduling by the Windows scheduling tool;

2 - It is not necessary to make any access release (local or online) within the Windows environment for its execution, only the correct configuration of the packages that are used to execute the sequence of steps;

3 - For security reasons, the step of connection with the online database will be hidden from the project, to protect the integrity of the bank.

4 - All execution steps of the Robot have triggers in case specific operational problems occur so that attempts are made.

<!-- ## Installers

If you want to test the App in the Production mode, the installers are listed below:

[Android .apk installer](https://drive.google.com/file/d/1LKgdu1WDPo8eU2NVjoB92TPi4my8QP4D/view?usp=sharing)

iOS .ipa installer: Soon! -->

## Functionalities

- Log files for error debugging during execution and Robot improvement

- Opening and logging in with the Supermarket ERP

- Entering the product report extraction area

- Configuration of the report columns to be extracted

- Printing the report, using the options made available by the ERP itself

- Save the extracted xlsx in a temporary folder on Google Drive

- Processing the extracted file, performing the ETL treatment process

- Connection to an online database on Railway (PostGresql)
    - Cleaning of the current table
    - Line by line insertion of data into the bank
    - Deletion of the extracted excel file

![loading_sync_db](https://github.com/edi414/ERP_Automation/assets/80610321/16cdfff0-4d0c-4185-b2de-58dbbd3d1f08)

<!-- ## Getting Started

### Prerequisites

To run this project in the development mode, you'll need to have a basic environment to run a React-Native App, that can be found [here](https://facebook.github.io/react-native/docs/getting-started).

Also, you'll need to the server running locally on your machine with the mock data. You can find the server and all the instructions to start the server [here](https://github.com/steniowagner/mindcast-server).

### Installing

**Cloning the Repository**

```
$ git clone https://github.com/steniowagner/mindCast

$ cd mindCast
```

**Installing dependencies**

```
$ yarn
```

_or_

```
$ npm install
```

### Connecting the App with the Server

1 - Follow the instructions on the [mindcast-server](https://github.com/steniowagner/mindcast-server) to have the server up and running on your machine.

2 - With the server up and running, go to the [/.env.development](https://github.com/steniowagner/mindCast/blob/master/.env.development) file and edit the SERVER_URL value for the IP of your machine (you can have some issues with _localhost_ if you're running on an android physical device, but you can use localhost safely on iOS).

It should looks like this:

SERVER_URL=http://**_IP_OF_YOUR_MACHINE_**:3001/mind-cast/api/v1

*or*

SERVER_URL=http://localhost:3001/mind-cast/api/v1

### Running

With all dependencies installed and the environment properly configured, you can now run the app:

Android

```
$ react-native run-android
```

iOS

```
$ react-native run-ios
```

## Built With

- [React-Native](https://facebook.github.io/react-native/) - Build the native app using JavaScript and React
- [React-Navigation](https://reactnavigation.org/docs/en/getting-started.html) - Router
- [Redux](https://redux.js.org/) - React State Manager
- [Redux-Saga](https://redux-saga.js.org/) - Side-Effect middleware for Redux
- [Axios](https://github.com/axios/axios) - HTTP Client
- [ESlint](https://eslint.org/) - Linter
- [React-Native-Dotenv](https://github.com/zetachang/react-native-dotenv) - Configs from .env file
- [Flow](https://flow.org/) - Static Type Checker
- [Prettier](https://prettier.io/) - Code Formatter
- [Babel](https://babeljs.io/) - JavaScript Compiler
- [Reactotron](https://infinite.red/reactotron) - Inspector
- [Styled-Components](https://www.styled-components.com/) - Styles
- [React-Native-Fast-Image](https://github.com/DylanVann/react-native-fast-image) - Image Loader
- [React-Native-Linear-Gradient](https://github.com/react-native-community/react-native-linear-gradient) - Gradient Styles
- [React-Native-SplashScreen](https://github.com/crazycodeboy/react-native-splash-screen) - Splashscreen of the App
- [React-Native-Vector-Icons](https://github.com/oblador/react-native-vector-icons) - Icons
- [React-Native-Side-Menu](https://github.com/react-native-community/react-native-side-menu) - Side Menu used on Player screen
- [React-Native-Swipeout](https://github.com/dancormier/react-native-swipeout) - Swipe for edit/remove playlists and remove podcasts inside some playlist
- [React-Native-Video](https://github.com/react-native-community/react-native-video) - Consume the audio files via streaming
- [React-Native-FS](https://github.com/itinance/react-native-fs) - Handle download/undownload podcasts on file-system


## Support tools

- [Image-Resize](https://imageresize.org) - Resize the Images
- [Amazon S3](https://aws.amazon.com/pt/s3/) - Storage Service -->

## Contributing

You can send how many PR's do you want, I'll be glad to analyse and accept them! And if you have any question about the project...

Email-me: edivaldo414@gmail.com

Connect with me at [LinkedIn](https://www.linkedin.com/in/edivaldo-bezerra/)

Thank you!

<!-- ## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/steniowagner/mindCast/blob/master/LICENSE) file for details -->
