package com.example.skiichat.models

data class Message(
    var message:String? = null,
    var fromSender:Boolean = false,
    var fromSkii:Boolean = false
)
