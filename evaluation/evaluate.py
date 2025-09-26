import re, time

def _normalize(s: str):
    s = s.lower()
    s = re.sub(r'[^a-z0-9\\s]', '', s)
    return s.split()

def wer(ref: str, hyp: str) -> float:
    r = _normalize(ref)
    h = _normalize(hyp)
    d = [[0] * (len(h)+1) for _ in range(len(r)+1)]
    for i in range(len(r)+1):
        d[i][0] = i
    for j in range(len(h)+1):
        d[0][j] = j
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                d[i][j] = 1 + min(d[i-1][j], d[i][j-1], d[i-1][j-1])
    return d[len(r)][len(h)] / max(1, len(r))

def benchmark_transcription(transcribe_func, sample_file: str, repeat: int = 1):
    t0 = time.time()
    for _ in range(repeat):
        transcribe_func(sample_file)
    t1 = time.time()
    elapsed = t1 - t0
    return {'elapsed_seconds': elapsed, 'per_run': elapsed / repeat}
