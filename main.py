from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'outtmpl': '/tmp/%(title)s.%(ext)s',  # Save to /tmp directory
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
            # Construct the file path
            video_file_path = ydl.prepare_filename(info)
            # Return the download URL
            download_url = request.host_url + 'downloaded/' + os.path.basename(video_file_path)
            return jsonify({'download_url': download_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/downloaded/<filename>', methods=['GET'])
def serve_video(filename):
    return send_from_directory('/tmp', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))