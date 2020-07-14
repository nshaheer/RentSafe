package com.leaseguard.leaseguard.ui

import android.content.Context
import android.util.AttributeSet
import android.util.TypedValue
import android.view.Gravity
import android.widget.ImageView
import android.widget.LinearLayout
import com.google.android.material.floatingactionbutton.FloatingActionButton
import com.leaseguard.leaseguard.R

class ActionMenu @JvmOverloads constructor(
        context: Context, attrs: AttributeSet? = null, defStyleAttr: Int = 0
) : LinearLayout(context, attrs, defStyleAttr) {
    private var menuIsShowing = false
    private var isAnimating = false
    private val expandButton: FloatingActionButton = FloatingActionButton(context)

    private val menuItems : MutableList<MenuButton> = mutableListOf()
    private val menuItemContainer = LinearLayout(context).apply {
        layoutParams = LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT)
        orientation = VERTICAL
    }

    init {
        orientation = VERTICAL
        gravity = Gravity.BOTTOM or Gravity.END
        expandButton.setImageResource(R.drawable.ic_plus)
        expandButton.scaleType = ImageView.ScaleType.CENTER
        expandButton.background.setTint(context.getColor(R.color.darkblack))
        val buttonSize = TypedValue.applyDimension(
                TypedValue.COMPLEX_UNIT_DIP,
                context.resources.getDimension(R.dimen.round_button_width),
                resources.displayMetrics
        ).toInt()
        expandButton.layoutParams = LayoutParams(buttonSize, buttonSize)
        expandButton.setOnClickListener {
            toggleMenu()
        }
        addView(menuItemContainer)
        addView(expandButton)
    }

    fun addItem(label: String, resId: Int, onClickListener: OnClickListener) {
        menuItems.add(MenuButton(context, label, resId).apply {
            setOnClickListener(onClickListener)
        })
    }

    private fun toggleMenu() {
        if (menuIsShowing) {
            hideMenu()
            menuIsShowing = false
        } else {
            showMenu()
            menuIsShowing = true
        }
    }

    private fun showMenu() {
        if (!isAnimating) {
            isAnimating = true
            for (item in menuItems) {
                menuItemContainer.addView(item)
            }
            isAnimating = false
        }
    }

    private fun hideMenu() {
        if (!isAnimating) {
            isAnimating = true
            menuItemContainer.removeAllViews()
            isAnimating = false
        }
    }
}