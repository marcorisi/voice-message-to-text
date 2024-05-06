import { Button, Image, StyleSheet, Text, View } from "react-native";

import { useShareIntent, ShareIntentFile } from "expo-share-intent";
import { Fragment, useState } from "react";

import { TextMessage } from './components/text-message';
import { TextMessageFooter } from './components/text-message-footer';
import { BackendUrlInput } from "./components/backend-url-input";
import { FileMeta } from "./components/file-meta";

export default function App() {
  const { hasShareIntent, shareIntent, resetShareIntent, error } =
    useShareIntent({
      debug: true,
      resetOnBackground: true,
    });

  const [transcription, setTranscription] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [url, setUrl] = useState("http://192.168.1.59:5000");

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

  return (
    <View style={styles.container}>
      <Text style={[styles.gap, styles.bold]}>
        {hasShareIntent ? "A new audio has been shared!" : "No audio shared..."}
      </Text>

      {shareIntent?.files?.map((file) => (
          <FileMeta file={file} />
      ))}

      <BackendUrlInput url={url} onChangeText={setUrl} />

      {!!shareIntent && (
        <Button onPress={() => resetShareIntent()} disabled={!hasShareIntent} title="Reset" />
      )}
      {!!shareIntent && (
        <Button onPress={() => uploadFileFromMobile()} disabled={!hasShareIntent} title="Transcribe" />
      )}
      <Text style={[styles.error]}>{error}</Text>

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
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
  logo: {
    width: 75,
    height: 75,
    resizeMode: "contain",
  },
  image: {
    width: 300,
    height: 200,
    resizeMode: "contain",
    // backgroundColor: "lightgray",
  },
  gap: {
    marginBottom: 20,
  },
  bold: {
    fontWeight: "bold",
  },
  meta: {
    alignItems: "center",
    justifyContent: "center",
  },
  error: {
    color: "red",
    marginTop: 20,
  },
});