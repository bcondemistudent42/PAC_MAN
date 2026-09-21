from dataclasses import dataclass


@dataclass
class GameSettings:
    map_width: int = 15
    map_height: int = 15
    cell_width_px: int = 24
    cell_height_px: int = 24
    scale: float = 1.0

    @classmethod
    def from_window(
        cls,
        window_width: int,
        window_height: int,
        map_width: int = 15,
        map_height: int = 15,
        cell_width_px: int = 24,
        cell_height_px: int = 24,
    ) -> GameSettings:
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
        )
