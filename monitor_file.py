import os, time, argparse
from tqdm import tqdm


def human(n):
    # 1024単位での簡易フォーマット
    units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]
    i = 0
    while n >= 1024 and i < len(units) - 1:
        n /= 1024.0
        i += 1
    return f"{n:.2f}{units[i]}"


def monitor(path, target=None, interval=0.5):
    last = 0
    last_t = time.time()
    bar = tqdm(total=target or 0, unit="B", unit_scale=True, desc=os.path.basename(path))
    try:
        while True:
            if not os.path.exists(path):
                time.sleep(interval)
                continue
            sz = os.stat(path).st_size
            now = time.time()
            dt = max(now - last_t, 1e-6)
            rate = (sz - last) / dt  # bytes/s

            # バー更新
            if target:
                bar.total = target
                bar.n = min(sz, target)
            else:
                bar.update(max(0, sz - bar.n))
            bar.set_postfix_str(f"{human(sz)}  {human(rate)}/s")

            last, last_t = sz, now
            if target and sz >= target:
                break
            time.sleep(interval)
    finally:
        bar.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="file to monitor")
    ap.add_argument("--target-bytes", type=int, default=0, help="expected final size (bytes)")
    ap.add_argument("--interval", type=float, default=0.5)
    args = ap.parse_args()
    monitor(args.path, args.target_bytes or None, args.interval)
