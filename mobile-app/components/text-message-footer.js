import { View, Text, StyleSheet } from 'react-native';

export function TextMessageFooter({ messageId, messageLength, responseStatusCode }) {

    let transcriptionType = "";

    switch (responseStatusCode) {
        case 200:
            transcriptionType = "Existing";
            break;
        case 201:
            transcriptionType = "New";
            break;
        default:
            transcriptionType = "Unknown";
            break;
    }

    return (
        <View style={ styles.container }>
            <Text style={ styles.text }>Message Id: {messageId}</Text>
            <Text style={ styles.text }>Length: {messageLength}</Text>
            <Text style={ styles.text }>Transcription Type: {transcriptionType}</Text>
        </View>
    )
}

const styles = StyleSheet.create({
    container: {
        flexDirection: 'column',
        textAlign: 'left',
        width: '100%',
        paddingHorizontal: 16,
    },
    text: {
        fontSize: 8,
        fontStyle: 'italic',
        color: 'black',
        width: '100%',
        paddingHorizontal: 16,
        paddingVertical: 2,
        backgroundColor: '#f0f0f0',
    },
});