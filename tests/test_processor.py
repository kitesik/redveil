import numpy as np

from redveil.processor import RedveilOptions, apply_redveil


def test_apply_redveil_changes_only_face_region() -> None:
    image = np.full((80, 80, 3), 120, dtype=np.uint8)
    options = RedveilOptions(padding=0, blur_strength=0, grid_step=10, line_width=1, alpha=1)

    output = apply_redveil(image, [(20, 20, 30, 30)], options)

    assert not np.array_equal(output[20:50, 20:50], image[20:50, 20:50])
    assert np.array_equal(output[:15, :15], image[:15, :15])


def test_apply_redveil_clips_expanded_face_region() -> None:
    image = np.full((30, 30, 3), 80, dtype=np.uint8)
    options = RedveilOptions(padding=1, blur_strength=0, grid_step=8, line_width=1, alpha=1)

    output = apply_redveil(image, [(0, 0, 12, 12)], options)

    assert output.shape == image.shape
    assert not np.array_equal(output[:20, :20], image[:20, :20])
