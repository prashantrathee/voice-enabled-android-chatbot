package com.example.skiichat.models

import okhttp3.MediaType
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody
import okio.BufferedSink
import java.io.File

data class AudioMessage(
    val file:File
):RequestBody(){
    override fun contentType(): MediaType? {
        return "audio/wav".toMediaTypeOrNull()
    }

    override fun writeTo(sink: BufferedSink) {

    }

}
