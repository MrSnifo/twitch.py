---
icon: material/format-text-variant 
hide:  
  - toc  
---

# Text Formatting and Animation in Alerts

Enhance your alerts with text formatting and animations to make them more engaging.

### **Highlighting and Animating Text**
___

- **Highlight Text**: Use `<<text>>` to emphasize.
- **Animate Text**: Use the `animation` parameter with classes from [Animate.css](https://animate.style/).

#### **Example Alert**

```python
await self.overlay.alert(
    '<<Exciting News!>> <br>%Don’t miss out% <br> Join us now!',
    font_size=64,
    font_name='Rubik',
    text_color='#FFFFFF',
    text_highlight_color='#00FFFF',
    text_animation='bounce',
    start_animation='bounceIn',
    end_animation='bounceOut'
)
```

**Details:**

- `<<Exciting News!>>` is highlighted and text animation.
- `%Don’t miss out%` is smaller.
- `<br>` adds line breaks.

### **Customizing Styles**
- **Fonts**: Use [Google Fonts](https://fonts.google.com) with the `font_name` parameter.
- **Animations**: Check [Animate.css](https://animate.style/) for more effects.

### **Notes**
- **Browser Behavior**: Animations may pause when the browser tab is inactive.
- **Audio Issues**: If audio doesn’t play, set **sound** permissions from default to allow in your browser settings.