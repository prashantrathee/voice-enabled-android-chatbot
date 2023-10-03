package com.example.skiichat

import android.app.Dialog
import android.graphics.Color
import android.graphics.drawable.ColorDrawable
import android.media.MediaRecorder
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.skiichat.adapters.MessageAdapter
import com.example.skiichat.databinding.ActivityMainBinding
import com.example.skiichat.models.Message
import com.example.skiichat.services.AudioService
import com.example.skiichat.services.MessageService
import com.example.skiichat.services.ServiceBuilder
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.cancel
import kotlinx.coroutines.launch
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.asRequestBody
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import wseemann.media.FFmpegMediaMetadataRetriever
import java.io.File
import java.io.FileOutputStream
import kotlin.coroutines.resume
import kotlin.coroutines.suspendCoroutine


class MainActivity : AppCompatActivity() {
    lateinit var binding:ActivityMainBinding
    lateinit var messagesAdapter:MessageAdapter
    var messages = arrayListOf<Message>()
    lateinit var recorder :MediaRecorder

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)


        val loadingDialog = Dialog(this)
        loadingDialog.setContentView(layoutInflater.inflate(R.layout.loading_circle_dialog,null))
        loadingDialog.window!!.setBackgroundDrawable(ColorDrawable(Color.TRANSPARENT))

        binding.recordIconCardInMainActivity.setOnClickListener {
//            if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
//                // Permission is not granted, request it from the user
//                ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.RECORD_AUDIO), REQUEST_RECORD_AUDIO_PERMISSION)
//            } else {
//                // Permission is already granted, perform the recording operation
//                startRecording()
//            }
            recorder = MediaRecorder()
            binding.recordIconCardInMainActivity.visibility = View.GONE
            binding.stopIconCardInMainActivity.visibility = View.VISIBLE
            val outputFile = File(applicationContext.externalCacheDir, "recorded_audio.pcm")
            outputFile.createNewFile()
            recorder.setAudioSource(MediaRecorder.AudioSource.MIC)
            recorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP)
            recorder.setAudioEncoder(MediaRecorder.AudioEncoder.DEFAULT)
//            recorder.setAudioChannels(1) //
            Toast.makeText(applicationContext,"Absolute path = ${outputFile.absolutePath}",Toast.LENGTH_LONG).show()
            recorder.setOutputFile(outputFile.absolutePath)
            recorder.prepare()
            recorder.start()
        }
        binding.stopIconCardInMainActivity.setOnClickListener {
            recorder.stop()
            recorder.reset()
            recorder.release()
            binding.stopIconCardInMainActivity.visibility = View.GONE
            binding.recordIconCardInMainActivity.visibility = View.VISIBLE
            var audioCoroutineScope = CoroutineScope(Dispatchers.Main)
            audioCoroutineScope.launch {
                loadingDialog.create()
                loadingDialog.show()
                var messagesReceived = sendAudio(audioPath = "recorded_audio.pcm")
                if(messagesReceived!=null){
                    addToRecyclerView(messagesReceived[0],messagesReceived[1])
                }
                loadingDialog.cancel()
                audioCoroutineScope.cancel()
            }
        }

        binding.recyclerViewInMainActivity.layoutManager = LinearLayoutManager(applicationContext)
        messagesAdapter = MessageAdapter(this,messages)
        binding.sendIconCardInMainActivity.setOnClickListener {
            val messageInput = binding.messageInputInMainActivity.text.toString().trim()
            if(messageInput.isEmpty()){
                Toast.makeText(this,"Enter some message first",Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }
            var messageCoroutineScope = CoroutineScope(Dispatchers.Main)
            messageCoroutineScope.launch {
                loadingDialog.create()
                loadingDialog.show()
                val skiiMessage= sendMessage(messageInput)
                    if(skiiMessage != null){
                        addToRecyclerView(Message(
                            message = messageInput,
                            fromSkii = false,
                            fromSender = true
                        ),skiiMessage)
                    }
                loadingDialog.cancel()
                messageCoroutineScope.cancel()
            }
        }
    }

    private fun addToRecyclerView(senderMessage:Message,skiiMessage: Message) {
        Log.d("receivedMessage","in add to recycler view with messages = "+senderMessage.toString() + " and skii message = "+skiiMessage.toString())
        messagesAdapter.updateData(senderMessage)
        messagesAdapter.updateData(skiiMessage)
        binding.recyclerViewInMainActivity.adapter = messagesAdapter
        binding.recyclerViewInMainActivity.scrollToPosition(messagesAdapter.itemCount - 1)
    }

    private suspend fun sendAudio(audioPath:String):Array<Message>?{
        return suspendCoroutine { continuation ->
//            val wavFilePath = "recorded_audio.wav"
//            val mmr = FFmpegMediaMetadataRetriever()
//            mmr.setDataSource(audioPath)
//
//            val audioBytes: ByteArray = mmr.getEmbeddedPicture()
//            val fos: FileOutputStream = FileOutputStream(wavFilePath)
//            fos.write(audioBytes)
//            fos.close()
            val file = File(applicationContext.externalCacheDir,audioPath)
            val requestBody = file.asRequestBody("audio/pcm".toMediaTypeOrNull())
            if(requestBody == null){
                continuation.resume(null)
            }else{
                val audioService = ServiceBuilder.buildService(AudioService::class.java)
                val requestCall = audioService.sendAudio(requestBody)
                requestCall.enqueue(object:Callback<Array<Message>>{
                    override fun onResponse(
                        call: Call<Array<Message>>,
                        response: Response<Array<Message>>
                    ) {
                        if(response.isSuccessful){
                            continuation.resume(response.body())
                        }else{
                            Toast.makeText(this@MainActivity,"Didn't receive a good response",Toast.LENGTH_SHORT).show()
                            continuation.resume(null)
                        }
                    }

                    override fun onFailure(call: Call<Array<Message>>, t: Throwable) {
                        Toast.makeText(this@MainActivity, "Error : $t", Toast.LENGTH_SHORT).show()
                        Log.d("messageReceived","Error : $t")
                        continuation.resume(null)
                    }

                })
            }
        }
    }

    private suspend fun sendMessage(messageInput: String): Message? {
        return suspendCoroutine { continuation ->
            val messageService = ServiceBuilder.buildService(MessageService::class.java)
            val requestCall = messageService.sendQuery(messageInput)
            requestCall.enqueue(object : Callback<Message> {
                override fun onResponse(call: Call<Message>, response: Response<Message>) {
                    if (response.isSuccessful) {
                        var receivedMessage = response.body()!!
                        Log.d(
                            "receivedMessage",
                            "message = " + receivedMessage.message + "from sender" + receivedMessage.fromSender.toString()
                        )
                        continuation.resume(receivedMessage)
                    }else continuation.resume(null)
                }

                override fun onFailure(call: Call<Message>, t: Throwable) {
                    Toast.makeText(this@MainActivity, "Error : $t", Toast.LENGTH_SHORT).show()
                    Log.d("messageReceived","Error : $t")
                    continuation.resume(null)
                }

            })
        }
    }

    override fun onPause() {
        super.onPause()
        if(this::recorder.isInitialized) {
            recorder.stop()
            recorder.reset()
            recorder.release()
        }
    }
}