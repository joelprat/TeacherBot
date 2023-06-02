package com.sarmale.arduinobtexampleledcontrol;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.provider.MediaStore;
import android.speech.RecognizerIntent;
import android.util.Log;
import android.view.TextureView;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.io.File;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;

public class ServerConnection extends AppCompatActivity {
    private static final int REQUEST_RECORD_AUDIO_PERMISSION = 1;
    private Button commandButton;
    private static final int REQUEST_CAMERA_PERMISSION = 1;
    private static final int REQUEST_IMAGE_CAPTURE = 2;
    private Uri photoUri;
    Socket socket;
    OutputStream outputStream ;
    BufferedWriter writer ;
    ConnectedThread connectedThread;
    private SpeechHandler speechHandler;
    CameraHandler cam;
    private TextureView textureView;
    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_server);
        speechHandler = new SpeechHandler(this);
        commandButton = findViewById(R.id.commandButton);
        textureView = findViewById(R.id.textureView);
        cam = new CameraHandler(this, textureView);
        // Verificar si el permiso ya está concedido
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
                != PackageManager.PERMISSION_GRANTED) {
            // El permiso no está concedido, solicitarlo al usuario
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.RECORD_AUDIO},
                    1001);
        }

        commandButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
                i.putExtra(RecognizerIntent.EXTRA_LANGUAGE, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
                i.putExtra(RecognizerIntent.EXTRA_LANGUAGE, "ca");
                i.putExtra(RecognizerIntent.EXTRA_PROMPT, "Digues 'Corregir' o 'Dictar'");
                startActivityForResult(i, 5);
            }
        });
        connectedThread = MyApplication.getApplication().getCurrentConnectedThread();
        speechHandler.speak("Bon dia, quin exercici vols fer avui?");
    }
    private void requestCameraPermission() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.CAMERA}, REQUEST_CAMERA_PERMISSION);
        } else {
            dispatchTakePictureIntent();
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == REQUEST_CAMERA_PERMISSION) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                dispatchTakePictureIntent();
            } else {
                Toast.makeText(this, "Permiso de la cámara denegado", Toast.LENGTH_SHORT).show();
            }
        }
    }
    private void dispatchTakePictureIntent() {
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);
        } else {
            Toast.makeText(this, "No se pudo abrir la cámara", Toast.LENGTH_SHORT).show();
        }
    }
    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == RESULT_OK) {
            Bundle extras = data.getExtras();
            Bitmap imageBitmap = (Bitmap) extras.get("data");

            // Enviar la foto a través del socket
            try {
                sendPhoto(imageBitmap);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
        if(requestCode == 5 && resultCode == RESULT_OK)
        {
            ArrayList<String> result =
                    data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);

            if(!((result).contains("corregir")) && !((result).contains("dictar paraules")) && !((result).contains("dictar frase")) ){
                speechHandler.speak("Si us plau, pots vocalitzar?");
            }
            if(((result).contains("corregir")))
            {
                Toast.makeText(getApplicationContext(), "corregir", Toast.LENGTH_LONG).show();
                cam.takePicture();
            }

            if (((result).contains("dictar paraules"))) {
                Toast.makeText(getApplicationContext(), "dictar", Toast.LENGTH_LONG).show();
                new ConnectTask().execute("DICTA");
            }
            if (((result).contains("dictar frase"))) {
                Toast.makeText(getApplicationContext(), "frase", Toast.LENGTH_LONG).show();
                new ConnectTask().execute("DICTAF");
            }
        }
    }
    private void sendPhoto(Bitmap bitmap) throws IOException {
        ByteArrayOutputStream stream = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG, 100, stream);
        byte[] imageBytes = stream.toByteArray();

        // Aquí debes usar el socket y enviar los imageBytes al servidor
        PrintWriter output = new PrintWriter(socket.getOutputStream(), true);
        output.println(imageBytes);
        // Luego de enviar la foto, puedes cerrar la actividad si es necesario
        finish();

    }
    public class ConnectTask extends AsyncTask<String, Void, Void> {
        private Socket socket;
        private OutputStream outputStream;
        private BufferedWriter writer;

        @Override
        protected Void doInBackground(String... params) {
            String command = params[0];
            try {
                // Establecer la dirección IP y el puerto del servidor
                String serverIP = "192.168.0.16"; // Ejemplo de dirección IP
                int serverPort = 1234; // Ejemplo de puerto
                connectedThread = MyApplication.getApplication().getCurrentConnectedThread();
                // Crear el socket y establecer la conexión con el servidor
                socket = new Socket(serverIP, serverPort);
                outputStream = socket.getOutputStream();

                writer = new BufferedWriter(new OutputStreamWriter(outputStream));

                BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                // Leer la respuesta del servidor
                String response = "";

                //writer.write(command);
                //writer.flush();
                outputStream.write(command.getBytes());
                outputStream.flush();
                while (!response.equalsIgnoreCase("FOTO") && !response.contains("START") && !response.contains("DICTA")) {
                    response = input.readLine();
                    Log.d("TAG", "Respuesta recibida del servidor: " + response);
                }

                //Send Image here
                // Leer la foto como un arreglo de bytes y enviar
                if (response.equalsIgnoreCase("FOTO")) {
                    requestCameraPermission();
                    //dispatchTakePictureIntent();
                    // Capturar la foto automáticamente
                    response = "";
                }
                if (response.contains("DICTA")) {
                    String[] frase = response.split(":");
                    speechHandler.speak(frase[1]);
                }
                if (response.contains("START")) {
                    String[] frase = response.split(":");
                    Log.d("TAG", "Entra: " + response);
                    connectedThread.write(frase[0] + "\n");
                    String[] graus = frase[1].split(";");
                    for (int i = 0; i < graus.length; i++) {
                        Thread.sleep(5000);
                        connectedThread.write(graus[i] + "\n");
                    }
                    response = "";

                }
                socket.close();

            } catch (IOException e) {
                e.printStackTrace();
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
            return null;
        }
    }


    @Override
    protected void onDestroy() {
        super.onDestroy();
        cam.closeCamera();
    }

}
