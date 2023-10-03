package com.example.skiichat.services

import com.example.skiichat.models.Message
import retrofit2.Call
import okhttp3.RequestBody
import retrofit2.http.Body
import retrofit2.http.POST

interface AudioService {

    @POST("sendAudio")
    fun sendAudio(
        @Body audioBody:RequestBody
    ): Call<Array<Message>>

}