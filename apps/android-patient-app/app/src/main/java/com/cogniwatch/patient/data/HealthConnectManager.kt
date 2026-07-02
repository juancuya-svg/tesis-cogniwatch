package com.cogniwatch.patient.data

import android.content.Context
import androidx.health.connect.client.HealthConnectClient

class HealthConnectManager(private val context: Context) {
    fun availabilityStatus(): Int = HealthConnectClient.getSdkStatus(context)

    suspend fun syncPlaceholder(): Map<String, Any?> {
        // This is intentionally lightweight in the thesis scaffold.
        // In the full build, this manager reads sleep, steps, heart rate,
        // exercise sessions and other available records from Health Connect,
        // then aggregates them into a daily summary for backend ingestion.
        return mapOf(
            "steps" to 4810,
            "total_sleep_minutes" to 401,
            "resting_heart_rate" to 68,
            "source" to "health_connect"
        )
    }
}
