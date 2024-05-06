import { Button, Image, StyleSheet, Text, View } from "react-native";

import { useShareIntent, ShareIntentFile } from "expo-share-intent";
import { Fragment, useState } from "react";

import { TextMessage } from './components/text-message';
import { TextMessageFooter } from './components/text-message-footer';
import { BackendUrlInput } from "./components/backend-url-input";

export default function App() {
  const { hasShareIntent, shareIntent, resetShareIntent, error } =
    useShareIntent({
      debug: true,
      resetOnBackground: true,
    });

  const [transcribedText, setTranscribedText] = useState("");
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
          resolve(JSON.parse(xhr.responseText));
        } else {
          reject("Request Failed" + xhr.responseText);
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
        setTranscribedText(data.text)
        setIsLoading(false);
      })
      .catch((error) => {
        console.log(error)
        setTranscribedText(error)
        setIsLoading(false);
      });
  }

  return (
    <View style={styles.container}>
      <Text style={[styles.gap, styles.bold]}>
        {hasShareIntent ? "SHARE INTENT FOUND !" : "NO SHARE INTENT DETECTED"}
      </Text>

      {/* TEXT and URL */}
      {!!shareIntent.text && <Text style={styles.gap}>{shareIntent.text}</Text>}
      {!!shareIntent.meta?.title && (
        <Text style={styles.gap}>{JSON.stringify(shareIntent.meta)}</Text>
      )}

      {/* FILES */}
      {shareIntent?.files?.map((file) => (
        <Fragment key={file.path}>
          {file.mimeType.startsWith("image/") && (
            <Image source={{ uri: file.path }} style={[styles.image]} />
          )}
          <FileMeta file={file} />
        </Fragment>
      ))}

      {/* FOOTER */}
      {!!shareIntent && (
        <Button onPress={() => resetShareIntent()} title="Reset" />
      )}
      {!!shareIntent && (
        <Button onPress={() => uploadFileFromMobile()} title="Transcribe" />
      )}
      <Text style={[styles.error]}>{error}</Text>

      <BackendUrlInput url={url} onChangeText={setUrl} />
      <TextMessage message={transcribedText} />
      <TextMessageFooter messageId="random-number-000" messageLength="00:24" />


    </View>
  );
}

function FileMeta({ file }) {
  return (
    <View style={[styles.gap, styles.meta]}>
      <Text style={styles.bold}>{file.fileName}</Text>
      <Text>
        {file.mimeType} ({Math.round((file.size || 0) / 1024)}
        ko)
      </Text>
      {file.width && (
        <Text>
          {file.width} x {file.height}
        </Text>
      )}
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