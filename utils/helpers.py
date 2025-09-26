def seconds_to_hhmmss(seconds: float) -> str:
    if seconds is None:
        return '00:00:00'
    seconds = int(round(seconds))
    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hrs:02d}:{mins:02d}:{secs:02d}"
