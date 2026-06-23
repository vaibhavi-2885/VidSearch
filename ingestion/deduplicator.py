from PIL import Image
import imagehash


class FrameDeduplicator:
    def __init__(self, threshold: int) -> None:
        self.threshold = threshold
        self._previous_hash: imagehash.ImageHash | None = None

    def should_keep(self, image: Image.Image) -> tuple[bool, str]:
        current_hash = imagehash.phash(image)
        if self._previous_hash is None:
            self._previous_hash = current_hash
            return True, str(current_hash)

        distance = current_hash - self._previous_hash
        if distance <= self.threshold:
            return False, str(current_hash)

        self._previous_hash = current_hash
        return True, str(current_hash)
