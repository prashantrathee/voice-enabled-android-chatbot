package com.example.skiichat.services

import com.example.skiichat.models.Message
import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Query

interface MessageService {

    @GET("send_query")
    fun sendQuery(
        @Query ("query") query:String
    ): Call<Message>

}