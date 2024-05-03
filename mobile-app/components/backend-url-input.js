import { View, Text, TextInput, StyleSheet } from 'react-native';

export function BackendUrlInput({ url, onChangeText }) {
    return (
        <View style={ styles.container }>
            <View style={ styles.wrapper}>
                <Text>Backend URL: </Text>
                <TextInput onChangeText={onChangeText} value={url}/>
            </View>
        </View>
    )
}

const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        alignItems: 'center',
        textAlign: 'left',
        width: '100%',
        paddingHorizontal: 16,
    },
    wrapper: {
        flexDirection: 'row',
        alignItems: 'center',
        width: '100%',
        paddingHorizontal: 16,
        borderColor: 'black',
        borderWidth: 1,
    }
});