package com.example.loginapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                LoginScreen()
            }
        }
    }
}
@Preview(showBackground = true)

@Composable
fun LoginScreen() {

    var username by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var selectedTab by remember { mutableStateOf(0) }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFEFEFEF)),
        contentAlignment = Alignment.Center
    ) {

        Column(
            horizontalAlignment = Alignment.CenterHorizontally
        ) {

            Spacer(modifier = Modifier.height(40.dp))

            Box(
                modifier = Modifier
                    .size(100.dp)
                    .background(Color.LightGray)
            )

            Spacer(modifier = Modifier.height(40.dp))

            Card(
                shape = RoundedCornerShape(30.dp),
                modifier = Modifier
                    .padding(horizontal = 24.dp)
                    .fillMaxWidth(),
                colors = CardDefaults.cardColors(
                    containerColor = Color.White
                )
            ) {

                Column(
                    modifier = Modifier
                        .padding(24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {

                    Row(
                        modifier = Modifier
                            .background(
                                Color(0xFFE6E6E6),
                                RoundedCornerShape(50)
                            )
                            .padding(4.dp)
                    ) {

                        Button(
                            onClick = { selectedTab = 0 },
                            shape = RoundedCornerShape(50),
                            colors = ButtonDefaults.buttonColors(
                                containerColor = if (selectedTab == 0)
                                    Color(0xFFB39DDB)
                                else Color.Transparent
                            )
                        ) {
                            Text("Log In")
                        }

                        Button(
                            onClick = { selectedTab = 1 },
                            shape = RoundedCornerShape(50),
                            colors = ButtonDefaults.buttonColors(
                                containerColor = if (selectedTab == 1)
                                    Color(0xFFB39DDB)
                                else Color.Transparent
                            )
                        ) {
                            Text("Sign Up")
                        }
                    }

                    Spacer(modifier = Modifier.height(30.dp))

                    Box(
                        modifier = Modifier
                            .size(70.dp)
                            .clip(CircleShape)
                            .background(Color.LightGray)
                    )

                    Spacer(modifier = Modifier.height(30.dp))

                    OutlinedTextField(
                        value = username,
                        onValueChange = { username = it },
                        label = { Text("Username/Email") },
                        modifier = Modifier.fillMaxWidth()
                    )

                    Spacer(modifier = Modifier.height(16.dp))

                    OutlinedTextField(
                        value = password,
                        onValueChange = { password = it },
                        label = { Text("Password") },
                        visualTransformation = PasswordVisualTransformation(),
                        modifier = Modifier.fillMaxWidth()
                    )

                    Spacer(modifier = Modifier.height(30.dp))

                    Button(
                        onClick = { },
                        shape = RoundedCornerShape(50),
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(50.dp),
                        colors = ButtonDefaults.buttonColors(
                            containerColor = Color(0xFFBDBDBD)
                        )
                    ) {
                        Text("Log In")
                    }
                }
            }
        }
    }
}


