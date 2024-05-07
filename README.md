# Voice Message to Text

This repository contains a project that converts Whatsapp voice messages into text using a React Native frontend and a Flask backend.

<img src="./assets/video.gif" width="270" />

## Frontend

The frontend is a React Native app built using [Expo](https://expo.dev/) and the [Expo Share Intent plugin](https://github.com/achorein/expo-share-intent).  

> **Disclaimer:** This app has only been tested on Android devices.  
> I do not have access to any iPhone devices, and therefore, I have not been able to test the app on iOS.  
> However, I believe that running the app on iOS should be relatively straightforward.

### Requirements
1. Node.js, Git and Watchman (see [Expo installation](https://docs.expo.dev/get-started/installation/))
2. Android Studio Emulator (see [Expo installation](https://docs.expo.dev/workflow/android-studio-emulator/))
3. Java ([official instruction](https://www.java.com/en/download/help/index_installing.html)) and JDK ([download link](https://www.oracle.com/java/technologies/downloads/))
4. *(optional)* An Expo account, if you want to build with EAS ([link](https://expo.dev/signup))

### Run the app in development mode
```
$ cd mobile-app/
$ npx expo prebuild --no-install --clean --platform android
$ npx expo run:android
```

### Build the app

Run the following commands to build the app with EAS.
```
$ cd mobile-app/
$ eas login
$ eas build --platform android --profile preview
```

If you want to build your app locally, add `--local` to the last command.

## Backend

The backend is written in Flask and utilizes virtualenv for dependency management.  
For voice recognition, this app uses [Whisper](https://github.com/openai/whisper), an open-source Speech-to-Text model developed by OpenAI.  
All the data is stored in `db.json`, a super lightweight text database managed with [TinyDB](https://tinydb.readthedocs.io/en/latest/).

### Requirements
1. virtualenv ([installation link](https://virtualenv.pypa.io/en/latest/installation.html))
2. ffmpeg ([official website](https://ffmpeg.org/))


### Run the app
```
$ cd backend/
$ source venv/bin/activate
$ pip install -r requirements.txt
$ flask --app app run --host=0.0.0.0
```

### Run the test
```
$ cd backend/
$ python -m unittest -v
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
