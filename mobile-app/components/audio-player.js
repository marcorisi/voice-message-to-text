import { View, StyleSheet, Button } from 'react-native';
import { useEffect, useState } from 'react';
import { Audio } from 'expo-av';

export function AudioPlayer ({ audioPath }) {

    const [sound, setSound] = useState();
    const [isPlaying, setIsPlaying] = useState(false);

    async function playSound() {
        const { sound } = await Audio.Sound.createAsync( { uri: audioPath }, { shouldPlay: true } );
        setSound(sound);
        await sound.playAsync();
        setIsPlaying(true);
    }

    async function stopSound() {
        await sound.stopAsync();
        setIsPlaying(false);
    }

    useEffect(() => {
        return sound
          ? () => sound.unloadAsync()
          : undefined;
    }, [sound]);

    return (
        <View style={[styles.gap]}>
            { !isPlaying && <Button title="Play" onPress={playSound} color="grey" /> }
            { isPlaying && <Button title="Stop" onPress={stopSound} color="grey" /> }
        </View>
    );
}

const styles = StyleSheet.create({
    gap: {
      marginBottom: 16,
      width: '100%',
      paddingHorizontal: 16,
    },
});
