from dataclasses import dataclass


@dataclass
class GameSettings:
    """Store window, map, scale, and ghost timing configuration."""

    window_width: int
    window_height: int
    tile_size: float
    map_width: int = 15
    map_height: int = 15
    cell_width_px: int = 24
    cell_height_px: int = 24
    scale: float = 1.0
    chase_duration: float = 20.0
    scatter_duration: float = 7.0

    @classmethod
    def from_window(
        cls,
        window_width: int,
        window_height: int,
        map_width: int = 9,
        map_height: int = 9,
        cell_width_px: int = 24,
        cell_height_px: int = 24,
    ) -> GameSettings:
        """Build settings scaled to fit a window.

        Args:
            window_width: Available window width in pixels.
            window_height: Available window height in pixels.
            map_width: Number of map cells horizontally.
            map_height: Number of map cells vertically.
            cell_width_px: Unscaled cell width in pixels.
            cell_height_px: Unscaled cell height in pixels.

        Returns:
            Settings with a scale that fits the requested window.
        """
        map_pixel_width = map_width * cell_width_px
        map_pixel_height = map_height * cell_height_px
        scale = min(
            window_width / map_pixel_width,
            window_height / map_pixel_height,
        )

        return cls(
            map_width=map_width,
            map_height=map_height,
            cell_width_px=cell_width_px,
            cell_height_px=cell_height_px,
            scale=scale,
            window_width=window_width,
            window_height=window_height,
            tile_size=8 * scale,
        )
