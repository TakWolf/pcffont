from pcffont.metric import PcfMetric


class PcfGlyph:
    name: str
    encoding: int
    scalable_width: int
    character_width: int
    width: int
    height: int
    offset_x: int
    offset_y: int
    bitmap: list[list[int]]

    def __init__(
            self,
            name: str,
            encoding: int,
            scalable_width: int = 0,
            character_width: int = 0,
            dimensions: tuple[int, int] = (0, 0),
            offset: tuple[int, int] = (0, 0),
            bitmap: list[list[int]] | None = None,
    ):
        self.name = name
        self.encoding = encoding
        self.scalable_width = scalable_width
        self.character_width = character_width
        self.width, self.height = dimensions
        self.offset_x, self.offset_y = offset
        self.bitmap = [] if bitmap is None else bitmap

    @property
    def dimensions(self) -> tuple[int, int]:
        return self.width, self.height

    @dimensions.setter
    def dimensions(self, value: tuple[int, int]):
        self.width, self.height = value

    @property
    def offset(self) -> tuple[int, int]:
        return self.offset_x, self.offset_y

    @offset.setter
    def offset(self, value: tuple[int, int]):
        self.offset_x, self.offset_y = value

    def create_metric(self, is_ink: bool) -> PcfMetric:
        metric = PcfMetric(
            left_side_bearing=self.offset_x,
            right_side_bearing=self.offset_x + self.width,
            character_width=self.character_width,
            ascent=self.offset_y + self.height,
            descent=-self.offset_y,
        )

        if not is_ink:
            return metric

        # Top
        for bitmap_row in self.bitmap:
            if any(bitmap_row) != 0:
                break
            metric.ascent -= 1

        # Empty
        if metric.ascent + metric.descent == 0:
            metric.ascent = 0
            metric.descent = 0
            metric.right_side_bearing = metric.left_side_bearing
            return metric

        # Bottom
        for bitmap_row in reversed(self.bitmap):
            if any(bitmap_row) != 0:
                break
            metric.descent -= 1

        # Left
        for i in range(self.width):
            if any(bitmap_row[i] for bitmap_row in self.bitmap) != 0:
                break
            metric.left_side_bearing += 1

        # Right
        for i in range(self.width):
            if any(bitmap_row[self.width - 1 - i] for bitmap_row in self.bitmap) != 0:
                break
            metric.right_side_bearing -= 1

        return metric
