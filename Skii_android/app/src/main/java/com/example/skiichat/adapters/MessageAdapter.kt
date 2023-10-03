package com.example.skiichat.adapters

import android.content.Context
import android.util.Log
import android.view.Gravity
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.FrameLayout
import android.widget.RelativeLayout
import android.widget.TextView
import androidx.cardview.widget.CardView
import androidx.recyclerview.widget.RecyclerView
import com.example.skiichat.R
import com.example.skiichat.models.Message

class MessageAdapter(
    var context: Context,
    var messages:ArrayList<Message>
    ): RecyclerView.Adapter<MessageAdapter.MessageViewHolder>() {

    private val fromSenderMessage = 1
    private val fromSkiiMessage = 2
    class MessageViewHolder(itemView: View):RecyclerView.ViewHolder(itemView) {
        val messageText = itemView.findViewById<TextView>(R.id.messageInMessageCard)
        val senderMessageCard = itemView.findViewById<RelativeLayout>(R.id.senderMessageCard)
        val skiiMessageCard = itemView.findViewById<CardView>(R.id.skiiMessageCard)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MessageViewHolder {
        return when(viewType){
            fromSenderMessage->{
                val view = LayoutInflater.from(parent.context).inflate(R.layout.sender_message_card,parent,false)
                MessageViewHolder(view)
            }
            fromSkiiMessage->{
                val view = LayoutInflater.from(parent.context).inflate(R.layout.skii_message_card,parent,false)
                MessageViewHolder(view)
            }
            else -> {throw IllegalArgumentException("Invalid view type")}
        }
    }

    override fun getItemCount(): Int {
        return messages.size
    }

    fun updateData(message: Message) {
        Log.d("receivedMessage", "got message in update data$message")
        messages.add(message)
        notifyDataSetChanged()
    }
    override fun onBindViewHolder(holder: MessageViewHolder, position: Int) {
        holder.messageText.text = messages[position].message.toString()

//        var layoutParams = holder.itemView.layoutParams
//        if (getItemViewType(position) == fromSkiiMessage) {
//            Log.d("message","in skii")
//                layoutParams = FrameLayout.LayoutParams(
//                    FrameLayout.LayoutParams.WRAP_CONTENT,
//                    FrameLayout.LayoutParams.WRAP_CONTENT,
//                    Gravity.START
//                ).apply {
//                    gravity = Gravity.START
//                    setMargins(16, 15, 216, 15) // set margins as per your requirements
//                }
//                holder.itemView.layoutParams = layoutParams
//        } else {
//            Log.d("message","in sender")
//                layoutParams = FrameLayout.LayoutParams(
//                    FrameLayout.LayoutParams.WRAP_CONTENT,
//                    FrameLayout.LayoutParams.WRAP_CONTENT,
//                    Gravity.END
//                ).apply {
//                    gravity = Gravity.END
//                    setMargins(16, 15, 16, 15) // set margins as per your requirements
//                }
//                holder.itemView.layoutParams = layoutParams
//        }
    }

    override fun getItemViewType(position: Int): Int {
        val message = messages[position]
        return if (message.fromSkii) fromSkiiMessage else fromSenderMessage
    }

}