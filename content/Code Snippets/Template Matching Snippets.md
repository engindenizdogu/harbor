---
title: Template Matching Snippets
tags: [computer-vision, template-matching, image-processing, code-snippets, auto-captured]
draft: false
---
NumPy-only implementations with no library image operations. Theory: [[Template Matching]], [[Multi-Scale Template Matching]], [[Gaussian Filtering and Convolution]]. Every function returns the window's top-left corner `(x, y)`, where x is the column and y is the row.

## SAD (minimize)

```python
def templ_sad(canvas, template):
    canvas = canvas.astype(np.float64)      # avoid uint8 wrap-around on subtraction
    template = template.astype(np.float64)
    H, W = canvas.shape
    h, w = template.shape

    best, tx, ty = np.inf, 0, 0
    for y in range(H - h + 1):
        for x in range(W - w + 1):
            sad = np.sum(np.abs(canvas[y:y+h, x:x+w] - template))
            if sad < best:
                best, tx, ty = sad, x, y
    return tx, ty
```

## NCC, zero-mean (maximize)

```python
def templ_ncc(canvas, template):
    canvas = canvas.astype(np.float64)
    template = template.astype(np.float64)
    H, W = canvas.shape
    h, w = template.shape

    eps = 1e-8                               # guards flat (zero-norm) windows
    t_bar = template - template.mean()       # constant: compute once
    t_ss = np.sum(t_bar ** 2)

    best, tx, ty = -np.inf, 0, 0
    for y in range(H - h + 1):
        for x in range(W - w + 1):
            win = canvas[y:y+h, x:x+w]
            w_bar = win - win.mean()
            ncc = np.sum(w_bar * t_bar) / (np.sqrt(np.sum(w_bar ** 2) * t_ss) + eps)
            if ncc > best:
                best, tx, ty = ncc, x, y
    return tx, ty
```

Hoist everything that does not depend on the window out of the loop (template mean and sum of squares). Further speedups use FFT-based correlation or integral images for the window sums.

## Gaussian kernel and zero-padded filtering

```python
def generate_gaussian(sigma, size=13):
    ref = (size - 1) / 2                     # index of the center
    k = np.zeros((size, size))
    for x in range(size):
        for y in range(size):
            k[x, y] = np.exp(-((x - ref) ** 2 + (y - ref) ** 2) / (2 * sigma ** 2)) / (2 * np.pi * sigma ** 2)
    return k / k.sum()                       # weights sum to 1

def filter_image(img, kernel):
    H, W = img.shape
    h, w = kernel.shape                      # odd sizes assumed
    ph, pw = (h - 1) // 2, (w - 1) // 2
    padded = np.zeros((H + 2 * ph, W + 2 * pw))   # manual zero-padding (np.pad not allowed)
    padded[ph:ph + H, pw:pw + W] = img

    out = np.zeros((H, W))
    for y in range(H):
        for x in range(W):
            out[y, x] = np.sum(padded[y:y+h, x:x+w] * kernel)   # dot product with the kernel
    return out
```

A size of `2 * ceil(3 * sigma) + 1` fits the kernel to sigma; the fixed 13 here is larger than needed for sigma = 1.

## Multi-scale search: remove, blur, subsample, map back

```python
# 1. Small instances: find, then zero out so the next search cannot return it again
x, y = templ_ncc(img, tmpl)
img[y:y+h, x:x+w] = 0
x2, y2 = templ_ncc(img, tmpl)                # second small instance
img[y2:y2+h, x2:x2+w] = 0

# 2. Low-pass BEFORE subsampling (avoids aliasing)
blurred = filter_image(img, generate_gaussian(sigma=1.0))
half    = np.clip(blurred[::2, ::2], 0, 255).astype(np.uint8)
quarter = np.clip(blurred[::4, ::4], 0, 255).astype(np.uint8)

# 3. Search with the unchanged small template, then map coordinates back
mx, my = templ_ncc(half, tmpl);    medium = (mx * 2, my * 2)
lx, ly = templ_ncc(quarter, tmpl); large  = (lx * 4, ly * 4)
```

## Non-maximum suppression and integral image

```python
def nms_score_map(score, thresh, radius):
    # Keep pixels that are above thresh and the maximum of their (2r+1) x (2r+1) neighbourhood
    H, W = score.shape
    peaks = []
    for y in range(H):
        for x in range(W):
            s = score[y, x]
            if s < thresh:
                continue
            win = score[max(0, y-radius):y+radius+1, max(0, x-radius):x+radius+1]
            if s == win.max():
                peaks.append((x, y, s))
    return sorted(peaks, key=lambda p: -p[2])   # best first; exact ties can yield duplicates

def iou(a, b):                                  # boxes as (x, y, w, h)
    iw = max(0, min(a[0]+a[2], b[0]+b[2]) - max(a[0], b[0]))
    ih = max(0, min(a[1]+a[3], b[1]+b[3]) - max(a[1], b[1]))
    inter = iw * ih
    return inter / (a[2]*a[3] + b[2]*b[3] - inter)

def nms_boxes(boxes, scores, thr):
    order = sorted(range(len(boxes)), key=lambda i: -scores[i])
    keep = []
    while order:
        i = order.pop(0)
        keep.append(i)
        order = [j for j in order if iou(boxes[i], boxes[j]) <= thr]
    return keep

def integral(img):                              # zero row and column in front
    ii = np.zeros((img.shape[0] + 1, img.shape[1] + 1))
    ii[1:, 1:] = img.cumsum(0).cumsum(1)
    return ii

def rect_sum(ii, x, y, w, h):                   # four lookups, any rectangle size
    return ii[y+h, x+w] - ii[y, x+w] - ii[y+h, x] + ii[y, x]
```

Checked on small synthetic inputs. Theory: [[Non-Maximum Suppression]], [[Integral Images]].

## Generating salt-and-pepper noise

```python
# Add salt-and-pepper noise at increasing levels (5% per step, per mask)
for i in range(1, 18):
    img = np.copy(img_clean)
    snp_corruption = 0.05 * i
    mask_s = np.random.random(img.shape)         # two independent random masks
    mask_p = np.random.random(img.shape)
    img[mask_s < snp_corruption] = 0             # black pixels (pepper)
    img[mask_p > 1 - snp_corruption] = 255       # white pixels (salt)
    imshow(img)
    fname = 'match' + repr(i) + '.png'
    cv2.imwrite(os.path.join(rootpath, fname), img)
```

Because the two masks are independent, the real corrupted fraction is about $1 - (1 - 0.05\,i)^2$, roughly double the label ([[Median Filter]], [[Image Noise]]).

## Noise sweep with a detection check

```python
true_locations = [(50, 60), (200, 50)]
is_detected = lambda x, y: (x, y) in true_locations     # tolerance 0 px

for i in range(2, 17, 2):                    # match2.png = 10% ... match16.png = 80%
    noise = 5 * i
    noisy = cv2.cvtColor(cv2.imread(f"match{i}.png"), cv2.COLOR_BGR2GRAY)
    sad_xy, ncc_xy = templ_sad(noisy, tmpl), templ_ncc(noisy, tmpl)
    print(noise, sad_xy, is_detected(*sad_xy), ncc_xy, is_detected(*ncc_xy))
```

---
*Related:* [[Code Snippets MOC]], [[Computer Vision MOC]]
