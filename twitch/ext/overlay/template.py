"""
The MIT License (MIT)

Copyright (c) 2024-present Snifo

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT firstED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import textwrap


class Template:
    """
    Represents a template for generating overlay HTML with dynamic content.
    """
    __slots__ = ()

    def __init__(self):
        pass

    def _index(self) -> str:
        """Generate the HTML template for the overlay."""
        index = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Overlay</title>
            <meta name="copyright" content="MIT License (c) 2024 by Snifo">
            <meta name="description" content="Overlay extension for twitch.py.">
            <meta name="author" content="Snifo">
            <meta name="generator" content="twitch.py">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
            <style> {styles} </style>
        </head>
        <body>
            <div id="alert-container" class="alert-container">
                <div id="alert-image-wrapper" class="alert-image-wrapper hide">
                    <img src id="alert-image" class="alert-image"> 
                </div>
                <div id="alert-text-wrapper" class="alert-text-wrapper">
                    <div id="alert-message" class="alert-message">
                    </div>
                </div>
            </div>
            <script>
            {filter_script} 
             </script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/howler/2.2.3/howler.min.js"></script>
            <script>
            {alert_script}
            </script>
        </body>
        </html>
        '''
        html = index.format(styles=self._styles,
                            filter_script=self._js_filter,
                            alert_script=self._js_alert)
        return html.replace('        ', '')

    @property
    def _styles(self) -> str:
        """Define the CSS styles for the overlay."""
        return '''
        :root {
            --animate-duration: 1.8s;
        }
        
        html, body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            background: transparent;
            overflow: hidden;
        }
        
        .alert-container, .alert-warp {
            display: flex;
            flex-direction: column;
            width: 100%;
            height: 100%;
        }
        
        .alert-image-wrapper.hide {
            display: none;
        }
        
        /* Image */
        .alert-image-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            flex: 7.8;
            overflow: hidden;
        }
        
        .alert-image {
            width: 100%;
            height: auto;
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            display: block;
        }
        
        .alert-image.hidden {
            visibility: hidden;
        }
        
        /* Text */
        .alert-text-wrapper {
            flex: 2.2; /* 20% height */
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            position: relative;
            width: 100%;
            padding: 0;
            box-sizing: border-box;
        }
        
        .alert-message {
            font-size: 64px;
            color: rgb(255, 255, 255); /* White text */
            font-family: sans-serif;
            font-weight: 400;
            text-align: center;
            line-height: 1.2;
            letter-spacing: 1px;
            text-shadow: 2px 2px 2px rgba(0, 0, 0, 1); /* Dark, sharp shadow */
            padding: 0 20px;
            box-sizing: border-box;
            width: 100%;
            white-space: normal; /* Allow text to wrap */
            word-break: break-word; /* Prevent text overflow */
        }
        
        /* Highlighted text styling */
        .alert-message .highlight {
            color: cyan;
            font-weight: bold; /* Example highlight style */
            display: inline-block; /* Ensure it's an inline element */
        }
        
        /* Small text styling */
        .alert-message .small-text {
            font-size: 0.6em; /* Reduce font size to 60% */
            display: inline-block;
        }
        '''

    @property
    def _js_filter(self) -> str:
        """JavaScript to set the default filter for the overlay."""
        return '''
        // Set default filter if not present
        const urlParams = new URLSearchParams(window.location.search);
        const filterParam = urlParams.get('default') || 'all';

        if (!urlParams.has('default')) {
            urlParams.set('default', 'all');
            window.history.replaceState({}, '', `${window.location.pathname}?${urlParams}`);
        }
        '''

    @property
    def _js_alert(self) -> str:
        """JavaScript for handling alerts, including animations, fonts, and images."""
        js_template = '''
        let reconnectInterval = 5000; // Time before attempting to reconnect
        const maxReconnectInterval = 60000; // Maximum delay for reconnection
        let isAnimating = false;
        let Queue = [];

        {initialize_audio}

        {alert_animate}

        {load_google_font}

        {load_image}

        {alert_update}

        {process_queue}

        {connect_websocket}

        connectWebSocket();         
        '''

        js_script = js_template.format(
            initialize_audio=self._js_initialize_audio,
            alert_animate=self._js_alert_animate,
            load_google_font=self._js_load_google_font,
            load_image=self._js_load_image,
            alert_update=self._js_alert_update,
            process_queue=self._js_process_queue,
            connect_websocket=self._js_connect_websocket
        )
        return js_script

    @property
    def _js_initialize_audio(self) -> str:
        """JavaScript function to initialize audio with Howler.js."""
        return '''
        const Initializeaudio = (url) => {
            return new Promise((resolve, reject) => {
                const audio = new Howl({
                    src: [url],
                    autoplay: false,
                    volume: 1.0,
                    onload: () => resolve(audio), // Resolve when the audio is loaded
                    onloaderror: () => reject(new Error('Failed to load audio')) // Reject if audio loading fails
                });
            });
        };
        '''

    @property
    def _js_alert_animate(self) -> str:
        """JavaScript function to animate an element using Animate.Style."""
        return '''
        // Animate an element using Animate.css
        const AlertAnimation = (element, animation) => {
            return new Promise((resolve) => {
                element.classList.add('animate__animated', `animate__${animation}`);
        
                // Resolve when the animation ends
                function handleAnimationEnd(event) {
                    event.stopPropagation();
                    element.classList.remove('animate__animated', `animate__${animation}`);
                    resolve('Animation ended');
                }
                element.addEventListener('animationend', handleAnimationEnd, { once: true });
            });
        };      
        '''

    @property
    def _js_load_google_font(self) -> str:
        """JavaScript function to load Google Fonts dynamically."""
        return '''
        // Load Google Fonts dynamically
        const LoadGoogleFonts = (fontName) => {
            return new Promise((resolve, reject) => {
                const link = document.createElement('link');
                link.href = `https://fonts.googleapis.com/css2?family=${fontName.replace(/ /g, '+')}&display=swap`;
                link.rel = 'stylesheet';
                link.onload = resolve; // Resolve when the font is loaded
                link.onerror = () => reject(new Error('Failed to load font')); // Reject if font loading fails
                document.head.appendChild(link);
            });
        };
        '''

    @property
    def _js_load_image(self) -> str:
        """JavaScript function to load an image and set its source."""
        return '''
        const LoadImage = (element, url) => {
            return new Promise((resolve, reject) => {
                element.src = url;  // Set the image source URL
                element.onload = () => {
                    resolve();  // Resolve the promise when the image is successfully loaded
                };
                element.onerror = () => {
                    reject(new Error('Failed to load image')); 
                };
            });
};
        '''

    @property
    def _js_alert_update(self) -> str:
        """JavaScript function to update the alert with new content and animations."""
        return '''
        // Main function to update the alert with dynamic content
        function Update(data) {
            return new Promise(async (resolve) => {
                const imageWarpElement = document.getElementById('alert-image-wrapper');
                const imageElement = document.getElementById('alert-image');
                const textElement = document.getElementById('alert-message');
                const alertWarpElement = document.getElementById('alert-container');
        
                if (!textElement || !alertWarpElement) {
                    console.error('Required element(s) not found.');
                    return resolve(); // Resolve immediately if elements are not found
                }
        
                // Load and apply custom font
                try {
                    await LoadGoogleFonts(data.font_name);
                    textElement.style.fontFamily = `'${data.font_name}', sans-serif`;
                } catch (error) {
                    textElement.style.fontFamily = 'sans-serif'; // Fallback to default font
                    console.error(error.message);
                }
        
                
                textElement.style.fontSize = `${data.font_size}px`
                
                textElement.style.color = data.text_color
        
                // Load and play audio if available
                let audio = null;
                if (data.audio) {
                    try {
                        audio = await Initializeaudio(data.audio);
                    } catch (error) {
                        console.error('Error initializing audio:', error);
                    }
                }
        
                // Apply text formatting (highlight and small text)
                const fontSizeRegex = /%([^%]+)%/g;
                const highlightRegex = /<<([^<>]+)>>/g;
                let formattedText = data.text
                    .replace(fontSizeRegex, '<div class="small-text">$1</div>')
                    .replace(highlightRegex, `<div id="highlight" class="highlight">$1</div>`);
                
        
                // Play audio if loaded
                if (audio) {
                    audio.play();
                }
        
                // Load and display image if available
                imageWarpElement.classList.add('hide');
                
                if (data.image) {
                    try {
                        await LoadImage(imageElement, data.image);
                        imageWarpElement.classList.remove('hide');
                    } catch (error) {
                        console.error(error.message);
                    }
                }
                
                textElement.innerHTML = formattedText;
        
                // Animate highlighted text if present
                const highlightElements = document.querySelectorAll('#highlight');
        
                if (highlightElements.length > 0) {
                    highlightElements.forEach((element) => {
                        // Add the animation class to each element
                        element.style.color = data.text_highlight_color
                        element.classList.add('animate__animated', `animate__${data.text_animation}`,
                        'animate__infinite');
                    });
                }
        
                // Animate the alert and manage its lifecycle
                AlertAnimation(alertWarpElement, data.start_animation).then(() => {
                    setTimeout(() => {
                        AlertAnimation(alertWarpElement, data.end_animation).then(() => {
                            // Clean up: reset elements after the animation ends
                            imageElement.src = '';
                            textElement.innerHTML = '';
                            textElement.style = '';
        
                            // Stop audio if playing
                            if (audio && audio.playing()) {
                                audio.stop();
                            }
                            resolve(); // Resolve the promise when everything is done
                        });
                    }, data.alert_duration * 1000); // Wait for alert duration before ending
                });
            });
        }
        '''

    @property
    def _js_process_queue(self) -> str:
        """JavaScript function to process a queue of alerts with a delay."""
        return '''
        const processQueue = () => {
            if (Queue.length > 0 && !isAnimating) {
                const data = Queue.shift();

                // Check if data is a non-empty object
                if (data && Object.keys(data).length > 0) {
                    isAnimating = true;
                    Update(data)
                        .then(() => {
                            isAnimating = false;
                            setTimeout(processQueue, 300);
                        })
                        .catch(error => {
                            // Log and handle errors, reset isAnimating and continue processing
                            console.error('Error in Update:', error);
                            isAnimating = false;
                            setTimeout(processQueue, 300);
                        });
                } else {
                    // Data is empty or invalid, just reset isAnimating and continue processing
                    isAnimating = false;
                    setTimeout(processQueue, 300);
                }
            }
        };
        '''

    @property
    def _js_connect_websocket(self) -> str:
        """JavaScript function to connect to a WebSocket server and handle messages."""
        return '''
        function connectWebSocket() {
            try {
                const urlParams = new URLSearchParams(window.location.search);
                const filterParam = urlParams.get('default') || 'all';
                
                const host = window.location.hostname;
                const port = window.location.port;
                
                ws = new WebSocket(`ws://${host}:${port}/ws?default=${encodeURIComponent(filterParam)}`);
        
                ws.onopen = () => {
                    console.log('WebSocket connection established');
                    reconnectInterval = 5000; // Reset reconnection interval
                };
        
                ws.onmessage = (event) => {
                    try {
                        const data = JSON.parse(event.data);
                        console.log('WebSocket message received:', data);
        
                        Queue.push(data);
                        processQueue();
                    } catch (err) {
                        console.error('Error processing WebSocket message:', err);
                    }
                };
        
                ws.onclose = (event) => {
                    console.warn(`WebSocket closed: ${event.reason || 'No reason provided'}`);
                    scheduleReconnect();
                };
        
                ws.onerror = (error) => {
                    console.error('WebSocket error:', error);
                    ws.close(); // Close and trigger onclose to handle reconnection
                };
        
            } catch (err) {
                console.error('WebSocket initialization failed:', err);
                scheduleReconnect();
            }
        }
        
        
        function scheduleReconnect() {
            console.log(`Reconnecting in ${reconnectInterval / 1000} seconds...`);
            setTimeout(() => {
                reconnectInterval = Math.min(reconnectInterval * 2, maxReconnectInterval); // Exponential backoff
                connectWebSocket();
            }, reconnectInterval);
        }
        '''

    def __str__(self) -> str:
        return textwrap.dedent(self._index()).strip()
