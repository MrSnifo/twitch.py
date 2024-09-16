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

from __future__ import annotations

from .attachment import Attachment
from typing import TYPE_CHECKING
from .geteway import WebSocket
from .route import Route
from aiohttp import web

if TYPE_CHECKING:
    from typing import Dict, Any, Optional, Tuple
    from twitch import Client

import logging
_logger = logging.getLogger(__name__)


class Overlay:
    """
    Represents the overlay server application.

    This class sets up and manages the overlay server, including routing,
    handling WebSocket connections, managing file attachments, and sending alerts.

    ???+ Notes
        - If sound is not working in the web browser, make sure to set the website
          permissions for sound to "Allow."

        - To change the default template used by the server, you can set
          `route.default_template = 'Your HTML'` on setup.

    Parameters
    ----------
    client: Optional[Client]
        An optional `Client` instance for event dispatching.
    host: str
        The host address for the server (default is 'localhost').
    port: int
        The port number for the server (default is 5050).
    **options: Dict[str, Any]
        Additional options to configure the `web.Application` instance.
    """

    __slots__ = ('app', 'host', 'port', 'gateway', '_attachment', 'route', '_client')

    def __init__(self, client: Optional[Client] = None, host: str = 'localhost', port: int = 5050, **options) -> None:
        self.app = web.Application(**options)
        self.host = host
        self.port = port
        self.gateway = WebSocket()
        self._attachment = Attachment()
        self.route = Route(self.app.router, self.gateway, self._attachment)
        self._client: Optional[Client] = client

    def url(self, default: str = 'all') -> str:
        """
        Get the server URI.

        Parameters
        ----------
        default: str
            The filter parameter for the alert.

        Returns
        -------
        str
            The full URL of the server with the specified filter parameter.
        """
        return f'http://{self.host}:{self.port}/?default={default}'

    async def start_app(self, handle_signals: bool = False, **options) -> Tuple[web.AppRunner, web.TCPSite]:
        """
        Start the overlay server.

        Sets up the application runner and site, and starts the server.

        ???+ Note
            Call this method within your `setup_hook()`.

        Parameters
        ----------
        handle_signals: bool
            Whether to handle signals for graceful shutdown (default is False).
        **options
            Additional options to pass to the `web.TCPSite` constructor.

        Returns
        -------
        Tuple[web.AppRunner, web.TCPSite]
            The application runner and TCP site objects.
        """
        runner = web.AppRunner(self.app, handle_signals=handle_signals)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port, **options)
        _logger.debug('Starting overlay server on http://%s:%s', self.host, self.port)
        await site.start()
        _logger.debug('Overlay server started successfully.')
        if self._client is not None:
            self._client.dispatch('overlay_ready')
        return runner, site

    async def alert(
            self,
            text: str,
            font_name: str = 'Roboto',
            font_size: float = 64.0,
            text_color: str = '#FFFFFF',
            text_highlight_color: str = '#6441a5',
            text_animation: str = 'pulse',
            start_animation: str = 'fadeIn',
            end_animation: str = 'fadeOut',
            image: Optional[str] = None,
            audio: Optional[str] = None,
            alert_duration: float = 5.0,
            default: str = 'all'):
        """
        Send an alert with specified parameters.

        ???+ Info
             The overlay uses [Animate.css](https://animate.style/).

             Be careful with animation names as they are **case-sensitive**.
    
        Parameters
        ----------
        text: str
            The text message to display.
        font_name: str
            The name of the font to use.
        font_size: float
            The size of the text font.
        text_color: str
            The color of the text.
        text_highlight_color: str
            The highlight color for text.
        text_animation: str
            The animation applied to the text.
            Refer to [Animate.css](https://animate.style/) for available text animations.
        start_animation: str
            The animation applied at the start of the alert.
            Refer to [Animate.css](https://animate.style/) for available start animations.
        end_animation: str
            The animation applied at the end of the alert.
            Refer to [Animate.css](https://animate.style/) for available end animations.
        image: Optional[str]
            The path to the image to display.
        audio: Optional[str]
            The path to the audio file to play.
        alert_duration: float
            The duration of the alert in seconds.
        default: str
            The `default` parameter specifies which filter key will trigger alerts.
            If set to a specific value (e.g., `'special'`), only alerts with that key will be processed.
            For example, if you set `default='special'`, alerts will only be triggered for the 'special' filter.
            To ensure the alert is processed, include this filter in the request URL.
            Example URL: `http://localhost:5050/?default=special`
        """
        data: Dict[str, Any] = {
            'text': text,
            'font_name': font_name,
            'font_size': font_size,
            'text_color': text_color,
            'text_highlight_color': text_highlight_color,
            'text_animation': text_animation,
            'start_animation': start_animation,
            'end_animation': end_animation,
            'image': self._attachment.get_path_key(image),
            'audio': self._attachment.get_path_key(audio),
            'alert_duration': alert_duration
        }
        await self.gateway.send_data(data, default)
        _logger.debug('Alert sent to default `%s` with data: %s', default, data)
        if self._client is not None:
            self._client.dispatch('overlay_alert', default, data)

    def add_attachment(self, name: str, path: str) -> None:
        """
        Add a new file attachment.

        Parameters
        ----------
        name: str
            The name of the attachment.
        path: str
            The file path of the attachment.
        """
        self._attachment.load_file_into_memory(name, path)

    def remove_attachment(self, name: str) -> None:
        """
        Remove an existing file attachment.

        Parameters
        ----------
        name: str
            The name of the attachment to remove.
        """
        self._attachment.remove_attachment(name)

    def clear_attachments(self) -> None:
        """
        Clear all attachments.
        """
        self._attachment.clear()

    def get_attachments(self) -> Dict[str, str]:
        """
        Retrieve all file attachments.

        Returns
        -------
        Dict[str, str]
            A dictionary where the keys represent attachment names and
            the values represent their corresponding upload paths.
        """
        return self._attachment.path_keys
