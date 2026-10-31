---
title: Data Types in Image Processing
tags: [computer-vision, image-processing, numpy, fundamentals, auto-captured]
draft: false
---
Images usually arrive as 8-bit integers (`uint8`, values 0 to 255), and image algorithms are mostly arithmetic on pixels. NumPy does not warn when an integer operation leaves the type's range, so a wrong data type produces **plausible but wrong** results instead of an error. Tracking the type and range of every value is a core skill in computer vision. Basics of arrays and ranges: [[Image Representation and Indexing]].

## Silent Wrap-Around

`uint8` arithmetic wraps modulo 256 (tested with NumPy 2.4):

| Operation on `uint8` | Result | Note |
| -------------------- | ------ | ---- |
| `30 - 40` | 246 | Underflow |
| `abs(a - b)` | still 246 | The wrap happens before `abs`, so `abs` cannot repair it |
| `200 + 100` | 44 | Brightening can darken |
| `200 * 100` | 32 | Products wrap too |
| `-a` | 226 | Negation wraps |

Effect on matching costs: for pixel pairs `[10, 250]` and `[20, 5]` the correct SAD is 255 and the correct SSD is 60125, but with raw `uint8` they come out as 491 and 221 ([[Template Matching]]). Convert to a wider type first:

```python
diff = np.abs(a.astype(np.int16) - b.astype(np.int16))   # or float64
```

## Promotions and Conversions

- `a * 2.0` and `a / 2` give `float64`; `a // 2` stays `uint8`.
- `.sum()` and `.cumsum()` on `uint8` promote to `uint64`, which is safe, but passing `dtype=np.uint8` wraps. `.mean()` returns `float64`.
- Assigning a float into a `uint8` array **truncates** (127.9 becomes 127). A Python integer out of range raises `OverflowError`.
- `.astype(np.uint8)` on out-of-range floats is undefined: on one machine -1 became 255, 256 became 0 and 300 became 44. Always **clip, round, then cast**:

```python
out = np.clip(np.round(x), 0, 255).astype(np.uint8)
```

A related case is **interpolation**: bilinear sampling returns a float, so round it before storing into a `uint8` canvas (`V[y, x] = np.round(value)`). Direct assignment truncates, which darkens the image slightly everywhere ([[Image Stitching]]).

## Range, Sign and Precision

| Situation | Problem | Use |
| --------- | ------- | --- |
| Sobel or other derivative filters | Responses are signed, from -1020 to +1020 for a 3 x 3 Sobel on 8-bit input | `int16` or float; display with `abs` or normalization ([[Image Gradients and the Sobel Operator]]) |
| Harris response | Values reach about $10^{13}$ | `float64` ([[Harris Corner Detector]]) |
| Integral images | `float32` cannot hold integers above $2^{24}$ exactly. On a random 12-megapixel image a 10 x 10 sum came out as 13056 instead of 12993. `int32` overflows on an all-white 12 MP image (about $3.1 \times 10^9$ against $2.15 \times 10^9$) | `int64` or `float64` ([[Integral Images]]) |
| Normalized scores | NCC should stay in $[-1, 1]$ | float, with a small epsilon in the denominator |
| Float display | `imshow` expects floats in $[0, 1]$ or integers in $[0, 255]$; a float image in 0 to 255 shows as all white | Match the range to the type |
| 16-bit images | `uint16` wraps at 65535 | Convert before arithmetic |

Library conventions differ too: NumPy wraps, while OpenCV's `add` and `subtract` **saturate** (clip to 0 and 255). Many OpenCV functions require `uint8` or `float32` input. This is from my own knowledge and was not run.

## Reading Code With Types in Mind

1. For every line, state the type and range of each operand and of the result.
2. Look hardest at three places: arithmetic on `uint8`, a cast back to `uint8`, and any accumulator or product that can exceed its type.
3. Safe pattern: **convert to float on entry, compute, then clip, round and cast on exit.**
4. When running code, print `.dtype`, `.min()` and `.max()` at stage boundaries, or `assert` the expected range.

*Sources: behaviour verified by running NumPy 2.4 examples; the OpenCV remark is from my own knowledge.*

---
*Related:* [[Computer Vision MOC]], [[Pixel-Level Operations]], [[Image Representation and Indexing]], [[Image Basics Snippets]]
