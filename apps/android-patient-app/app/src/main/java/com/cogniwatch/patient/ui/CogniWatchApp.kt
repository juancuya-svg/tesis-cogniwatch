package com.cogniwatch.patient.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

private val cards = listOf(
    "Consentimiento y privacidad",
    "Conectar Health Connect",
    "Vincular cuidador",
    "Check-in diario",
    "Sueño y actividad",
    "Microevaluación cognitivo-motora",
)

@Composable
fun CogniWatchApp() {
    Scaffold(
        topBar = { TopAppBar(title = { Text("CogniWatch") }) }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            item {
                Card(modifier = Modifier.fillMaxWidth()) {
                    Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text("Seguimiento simple para el paciente", style = MaterialTheme.typography.headlineSmall)
                        Text("Esta app resume tu sueño, actividad y bienestar. No reemplaza atención médica.")
                        Button(onClick = { }) {
                            Text("Comenzar onboarding")
                        }
                    }
                }
            }
            items(cards) { label ->
                Card(modifier = Modifier.fillMaxWidth()) {
                    Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text(label, style = MaterialTheme.typography.titleMedium)
                        Text("Pantalla incluida en el flujo base del proyecto para la tesis.")
                    }
                }
            }
        }
    }
}
