import { Button, StyleSheet, Text, View } from "react-native";

import { useShareIntent, ShareIntentFile } from "expo-share-intent";
import { useState } from "react";
import * as Progress from "react-native-progress";

import { TextMessage } from './components/text-message';
import { TextMessageFooter } from './components/text-message-footer';
import { BackendUrlInput } from "./components/backend-url-input";
import { FileMeta } from "./components/file-meta";
import { AudioPlayer } from "./components/audio-player";

export default function App() {
  const { hasShareIntent, shareIntent, resetShareIntent, error } =
    useShareIntent({
      debug: true,
      resetOnBackground: true,
    });

  let apiUrl = process.env.EXPO_PUBLIC_API_URL
  if (process.env.EXPO_PUBLIC_API_PORT) {
    apiUrl = apiUrl + ":" + process.env.EXPO_PUBLIC_API_PORT
  }

  const [transcription, setTranscription] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [url, setUrl] = useState(apiUrl);

  const uploadFileFromMobile = () => {
    uploadFile(shareIntent.files[0]);
  }

  // https://stackoverflow.com/a/64397804
  const sendXmlHttpRequest = (data) => {
    const xhr = new XMLHttpRequest();
    const fullUrl = url + "/transcribe";
  
    return new Promise((resolve, reject) => {
      xhr.onreadystatechange = e => {
        if (xhr.readyState !== 4) {
          return;
        }
  
        if (xhr.status === 200 || xhr.status === 201) {
          let transcription = JSON.parse(xhr.responseText);
          transcription.statusCode = xhr.status;
          resolve(transcription);
        } else {
          reject("Request Failed: " + xhr.responseText);
        }
      };
      xhr.open("POST", fullUrl);
      xhr.setRequestHeader("Content-Type", "multipart/form-data");
      xhr.setRequestHeader("X-API-KEY", process.env.EXPO_PUBLIC_API_KEY);
      xhr.send(data);
    });
  }
  

  const uploadFile = async (file) => {
    setIsLoading(true);

    const formData = new FormData();
    const audioFile = {
      uri: file.path,
      name: file.fileName,
      type: file.mimeType,
    }
    formData.append("audio", audioFile);
    
    const response = sendXmlHttpRequest(formData)
      .then((data) => {
        console.log(data)
        setTranscription(data)
        setIsLoading(false);
      })
      .catch((error) => {
        alert(error);
        setIsLoading(false);
      });
  }

  const reset = () => {
    setTranscription({});
    resetShareIntent();
  }

  return (
    <View style={styles.container}>
      <Text style={[styles.intentInfo, styles.bold]}>
        {hasShareIntent ? "A new audio has been shared!" : "No audio shared..."}
      </Text>

      {shareIntent?.files?.map((file) => (
          <>
            <FileMeta key={file.path} file={file} />
            <AudioPlayer key={file.fileName} audioPath={file.path}/>
          </>
      ))}

      <BackendUrlInput url={url} onChangeText={setUrl} />

      <View style={styles.buttonWrapper}>
        {!!shareIntent && (
          <Button style={styles.button} onPress={() => reset()} disabled={!hasShareIntent} title="Reset" />
        )}
        {!!shareIntent && (
          <Button style={styles.button} onPress={() => uploadFileFromMobile()} disabled={!hasShareIntent} title="Transcribe" />
        )}
      </View>

      { isLoading && 
        <Progress.Bar height={8} borderRadius={0} indeterminate={true} color="#666" animating={!isLoading} useNativeDriver={true}/>
      }

      { !!error && <Text style={[styles.error]}>{error}</Text> }

      <TextMessage message={transcription.text} />
      <TextMessageFooter 
        messageId={transcription.id} 
        messageLength={transcription.length} 
        responseStatusCode={transcription.statusCode} />

    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFFFFF",
    alignItems: "center",
    margin: 8,
    marginTop: 80,
  },
  intentInfo: {
    margin: 16,
  },
  buttonWrapper: {
    display: "flex",
    flexWrap: "wrap",
    flexDirection: "row",
    justifyContent: "flex-end",
    width: "100%",
    padding: 16,
    gap: 16,
  },
  bold: {
    fontWeight: "bold",
  },
  error: {
    color: "red",
    marginTop: 20,
  },
});
