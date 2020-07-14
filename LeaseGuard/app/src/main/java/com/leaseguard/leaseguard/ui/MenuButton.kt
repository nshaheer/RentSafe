package com.leaseguard.leaseguard.ui

import android.content.Context
import android.util.TypedValue
import android.view.Gravity
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import com.google.android.material.floatingactionbutton.FloatingActionButton
import com.leaseguard.leaseguard.R

class MenuButton constructor(
        context: Context, label: String, imgSrc: Int
) : LinearLayout(context, null, 0) {
    private val menuLabel : TextView = TextView(context)
    private val actionButton : FloatingActionButton = FloatingActionButton(context)
    init {
        orientation = HORIZONTAL
        gravity = Gravity.CENTER_VERTICAL or Gravity.START
        clipToPadding = false
        clipChildren = false
        layoutParams = LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT)

        actionButton.background.setTint(context.getColor(R.color.lightgrey))
        actionButton.scaleType = ImageView.ScaleType.CENTER
        actionButton.size = convertToPixel(context.resources.getDimension(R.dimen.small_button_size))
        val paddingSize = convertToPixel(context.resources.getDimension(R.dimen.generic_padding))
        actionButton.setPadding(paddingSize, paddingSize, 0, paddingSize)
        menuLabel.setPadding(paddingSize, paddingSize, paddingSize, paddingSize)
        menuLabel.textSize = 16f
        setText(label)
        setImage(imgSrc)
        addView(actionButton)
        addView(menuLabel)
    }

    fun setText(text: String) {
        menuLabel.text = text
    }

    fun setImage(resId: Int) {
        actionButton.setImageResource(resId)
    }

    private fun convertToPixel(value: Float): Int {
        return TypedValue.applyDimension(
                TypedValue.COMPLEX_UNIT_DIP,
                value,
                resources.displayMetrics).toInt()
    }
}