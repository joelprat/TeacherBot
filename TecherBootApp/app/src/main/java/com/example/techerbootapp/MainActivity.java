package com.example.techerbootapp;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.Camera;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import android.Manifest;
public class MainActivity extends AppCompatActivity {
    private Button connectButton;
    private static final int REQUEST_CAMERA_PERMISSION = 1;
    private static final int REQUEST_IMAGE_CAPTURE = 2;
    private Uri photoUri;
    Socket socket;
    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        connectButton = findViewById(R.id.connectButton);
        connectButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ConnectTask connectTask = new ConnectTask();
                connectTask.execute();
            }
        });
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
    private class ConnectTask extends AsyncTask<Void, Void, Socket> {

        @Override
        protected Socket doInBackground(Void... voids) {
            try {
                // Establecer la dirección IP y el puerto del servidor
                String serverIP = "192.168.0.16"; // Ejemplo de dirección IP
                int serverPort = 1234; // Ejemplo de puerto
                requestCameraPermission();
                // Crear el socket y establecer la conexión con el servidor
                socket = new Socket(serverIP, serverPort);
                //BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                // Leer la respuesta del servidor
                String response= "";
                while(true) {
                    while (!response.equalsIgnoreCase("FOTO")) {
                        response = input.readLine();
                        Log.d("TAG", "Respuesta recibida del servidor: " + response);
                    }

                    //Send Image here
                    // Leer la foto como un arreglo de bytes y enviar
                    if(response.equalsIgnoreCase("FOTO")) {
                       dispatchTakePictureIntent();
                        // Capturar la foto automáticamente
                        response= "";
                    }

                }


                //return socket;
            } catch (IOException e) {
                e.printStackTrace();

                return null;
            }
        }

        @Override
        protected void onPostExecute(Socket socket) {
            if (socket != null) {
                // La conexión se realizó exitosamente
                // Aquí puedes realizar cualquier acción adicional que desees
            } else {
                // Hubo un error al establecer la conexión
                // Aquí puedes mostrar un mensaje de error o tomar otras medidas
            }
        }
    }

}
