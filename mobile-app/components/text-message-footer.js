import { View, Text, StyleSheet } from 'react-native';

export function TextMessageFooter({ messageId, messageLength }) {
    return (
        <View style={ styles.container }>
            <Text style={ styles.text }>Message Id: {messageId}</Text>
            <Text style={ styles.text }>Length: {messageLength}</Text>
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