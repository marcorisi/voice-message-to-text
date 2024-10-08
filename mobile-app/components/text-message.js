import { View, Text, StyleSheet } from 'react-native';

export function TextMessage({ message }) {
    return (
        <View style={ styles.container }>
            <Text style={ styles.text } selectable={true}>{message}</Text>
        </View>
    )
}

const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        textAlign: 'left',
        width: '100%',
        padding: 16,
    },
    text: {
        fontSize: 12,
        color: 'black',
        width: '100%',
        paddingVertical: 8,
        paddingHorizontal: 16,
        backgroundColor: '#f0f0f0',
    },
});
