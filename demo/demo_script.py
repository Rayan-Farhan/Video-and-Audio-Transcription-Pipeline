import requests, sys, time
API = 'http://localhost:8000/api'

def upload_and_wait(filepath):
    with open(filepath, 'rb') as f:
        files = {'file': (filepath, f)}
        r = requests.post(f"{API}/video/transcribe", files=files)
    r.raise_for_status()
    data = r.json()
    file_id = data['file_id']
    print('Uploaded, file_id=', file_id)
    time.sleep(1)
    tr = requests.get(f"{API}/video/{file_id}/transcript")
    print('Transcript:', tr.json())
    ch = requests.get(f"{API}/video/{file_id}/chunks")
    print('Chunks:', ch.json())

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python demo/demo_script.py path/to/video.mp4')
        sys.exit(1)
    upload_and_wait(sys.argv[1])
