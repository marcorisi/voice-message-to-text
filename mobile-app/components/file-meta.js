import { View, Text, StyleSheet } from 'react-native';

export function FileMeta ({file}) {
    return (
        <View style={[styles.gap, styles.meta]}>
            <Text>File: {file.fileName}</Text>
            <Text>MimeType: {file.mimeType}</Text>
            <Text>Size: {Math.round((file.size || 0) / 1024)} KB</Text>
        </View>
    );
}

const styles = StyleSheet.create({
    gap: {
      marginBottom: 16,
      width: '100%',
      paddingHorizontal: 16,
    },
    meta: {
      alignItems: "left",
    },
});