package com.example.skiichat.services

import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit


object ServiceBuilder {

    private const val URL = "http://192.168.69.64:1578"
    private val logger = HttpLoggingInterceptor().setLevel(HttpLoggingInterceptor.Level.BODY)
    private val okHttp = OkHttpClient.Builder().addInterceptor(logger).callTimeout(30,TimeUnit.SECONDS).build()
    private val builder = Retrofit.Builder().baseUrl(URL)
        .addConverterFactory(GsonConverterFactory.create())
        .client(okHttp)
    private val retrofit = builder.build()
    fun <T> buildService(serviceType:Class<T>):T{
        return retrofit.create(serviceType)
    }
}