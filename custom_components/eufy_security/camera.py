"""Define support for Eufy Security cameras/doorbells."""
import asyncio
import logging

from eufy_security.errors import EufySecurityError
from haffmpeg.camera import CameraMjpeg
from haffmpeg.tools import ImageFrame, IMAGE_JPEG

from homeassistant.components.camera import SUPPORT_ON_OFF, SUPPORT_STREAM, Camera
from homeassistant.components.ffmpeg import DATA_FFMPEG
from homeassistant.helpers.aiohttp_client import async_aiohttp_proxy_stream

from .const import DOMAIN, DATA_API, DATA_COORDINATOR
from .device import DeviceEntity


_LOGGER = logging.getLogger(__name__)

DEFAULT_FFMPEG_ARGUMENTS = "-pred 1"


async def async_setup_entry(hass, entry, async_add_entities):
    ffmpeg = hass.data[DATA_FFMPEG]
    api = hass.data[DOMAIN][entry.entry_id][DATA_API]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    async_add_entities(
        EufySecurityCam(ffmpeg, camera, coordinator)
        for camera in api.cameras.values()
    )


class EufySecurityCam(DeviceEntity, Camera):
    """Define a Eufy Security camera/doorbell."""

    def __init__(self, ffmpeg, device, coordinator):
        """Initialize."""
        super().__init__(device, coordinator)
        Camera.__init__(self)

        self._async_unsub_dispatcher_connect = None
        self._ffmpeg = ffmpeg
        self._ffmpeg_arguments = DEFAULT_FFMPEG_ARGUMENTS
        self._ffmpeg_image_frame = ImageFrame(ffmpeg.binary)
        self._ffmpeg_stream = CameraMjpeg(ffmpeg.binary)
        self._last_image = None
        self._last_image_url = None
        self._stream_url = None

    @property
    def supported_features(self):
        """Return supported features."""
        return SUPPORT_ON_OFF | SUPPORT_STREAM

    @property
    def motion_detection_enabled(self):
        """Return the camera motion detection status."""
        return self._device.params['CAMERA_PIR']

    async def async_camera_image(self):
        """Return a still image response from the camera."""
        if self._last_image_url != self._device.last_camera_image_url:
            self._last_image = await asyncio.shield(
                self._ffmpeg_image_frame.get_image(
                    self._device.last_camera_image_url,
                    output_format=IMAGE_JPEG,
                    extra_cmd=self._ffmpeg_arguments,
                )
            )
            self._last_image_url = self._device.last_camera_image_url

        return self._last_image

    async def async_disable_motion_detection(self):
        """Disable doorbell's motion detection"""
        await self._device.async_update_param('DETECT_SWITCH', False)

    async def async_enable_motion_detection(self):
        """Enable doorbell's motion detection"""
        await self._device.async_update_param('DETECT_SWITCH', True)

    async def async_turn_off(self):
        """Turn off the RTSP stream."""
        try:
            await self._device.async_stop_stream()
            _LOGGER.info("Stream stopped for %s", self._device.name)
        except EufySecurityError as err:
            _LOGGER.error("Unable to stop stream (%s): %s", self._device.name, err)

        self._stream_url = None

    async def async_turn_on(self):
        """Turn on the RTSP stream."""
        try:
            self._stream_url = await self._device.async_start_stream()
            _LOGGER.info("Stream started (%s): %s", self._device.name, self._stream_url)
        except EufySecurityError as err:
            _LOGGER.error("Unable to start stream (%s): %s", self._device.name, err)

    async def handle_async_mjpeg_stream(self, request):
        """Generate an HTTP MJPEG stream from the camera."""
        await self.async_turn_on()
        if not self._stream_url:
            return await self.async_camera_image()

        await self._ffmpeg_stream.open_camera(
            self._stream_url, extra_cmd=self._ffmpeg_arguments
        )

        try:
            stream_reader = await self._ffmpeg_stream.get_reader()
            return await async_aiohttp_proxy_stream(
                self.hass,
                request,
                stream_reader,
                self._ffmpeg.ffmpeg_stream_content_type,
            )
        finally:
            await self._ffmpeg_stream.close()

    async def stream_source(self):
        self._stream_url = await self._device.async_start_stream()
        return self._stream_url
