package com.sarmale.arduinobtexampleledcontrol;

import android.content.Context;
import android.speech.tts.TextToSpeech;
import android.util.Log;

import java.util.Locale;

public class SpeechHandler {
    private Context context;
    private TextToSpeech textToSpeech;
    private boolean isReady = false;
    private String pendingText;

    public SpeechHandler(Context context) {
        this.context = context;
        setupTextToSpeech();
    }

    private void setupTextToSpeech() {
        textToSpeech = new TextToSpeech(context, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status == TextToSpeech.SUCCESS) {
                    int result = textToSpeech.setLanguage(new Locale("ca", "ES"));
                    if (result == TextToSpeech.LANG_MISSING_DATA
                            || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                        Log.e("TTS", "Language not supported");
                    } else {
                        isReady = true;
                        Log.i("TTS", "TextToSpeech is Initialized.");
                        if (pendingText != null) {
                            speak(pendingText);
                            pendingText = null;
                        }
                    }
                } else {
                    Log.e("TTS", "Initialization failed");
                }
            }
        });
    }

    public void speak(String text) {
        if (isReady) {
            textToSpeech.speak(text, TextToSpeech.QUEUE_FLUSH, null, null);
        } else {
            pendingText = text;
        }
    }
}

