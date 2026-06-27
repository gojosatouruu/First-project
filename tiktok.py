from flask import Flask, render_template, request, jsonify, send_file
import re
import os
import requests
import io

app = Flask(__name__)

HEADERS = {
    'authority': 'v16-webapp-prime.tiktok.com',
    'accept': '*/*',
    'accept-language': 'en-GB,en;q=0.9,si-LK;q=0.8,si;q=0.7,en-US;q=0.6',
    'cookie': 'd_ticket=c8274dcaf38e26783957572fd750cccceb1d2; multi_sids=7582606827553227784%3A34d4e40aefb03e5fc6da3b0ac7f8b732; cmpl_token=AgQYAPOz_hfkTtK5BDobs_HdMfOOGLC8xj-AEGCnmgE; uid_tt=e32b3d59f08146e527c935468ce176df28aa8e5a0488b29ec0e3b03d992e176a; uid_tt_ss=e32b3d59f08146e527c935468ce176df28aa8e5a0488b29ec0e3b03d992e176a; sid_tt=34d4e40aefb03e5fc6da3b0ac7f8b732; sessionid=34d4e40aefb03e5fc6da3b0ac7f8b732; sessionid_ss=34d4e40aefb03e5fc6da3b0ac7f8b732; store-idc=alisg; store-country-code=lk; store-country-code-src=uid; tt-target-idc=alisg; tt-target-idc-sign=ug2sjClG2IePcJ5lzZGgNA1k4WFM9SvtmETIFZobwQXfmi3rsQcI9OMXYSQ7-ZPJBptpGdt69CrMaZCbon6T8LoPpZ5sInha5Y9FmXMUHCDUM_6JBHTg3gk9pls-Qzv4dGLukuzh-W4p1w-rqcOxIUo33Te8xNr_oUIgtExX6bQrUCTX_f80o5aolIQlJgsFI9LoS4R7l4X2-iUiTltocGRfbJJNAvYUr0ao8Vu0SOEBvbS9cAT8tT8omjYU9rZRubIXrRw7uShETtlLtYrmG-CVMtWO5nhtzejcHiCgGu8tsCrrz2NEkOq97p9_fbZP7wgjSuQlVMk73al2LO_de2ciEwzExbs1rZv-eBI9Aep1CGeImPd8EJibwV_oJscB9cHy5Np2MVBkcz7YDG7PBM6PsMQH_BdD1A4MGva-7b0rmFlGJq5fwSgdMrYr-_PHGw948hURD6GJy282GdhnEVjqArIgqLKURg141x86CADGUqgSP6WIahP7ybmSyZL_; tt_chain_token=gvK0NJEkwh/7LYBvoFpHgA==; sid_guard=34d4e40aefb03e5fc6da3b0ac7f8b732%7C1777381824%7C15551974%7CSun%2C+25-Oct-2026+13%3A09%3A58+GMT; tt_session_tlb_tag=sttt%7C4%7CNNTkCu-wPl_G2jsKx_i3Mv________-fSGymV66K-rbbtsLoEp61PWtiXV5JR9Rd1Rx_aoyF4ng%3D; sid_ucp_v1=1.0.1-KDhmMzE4MTlkZTFlN2FhNGM3NGRiMzlhYzAyNGJmNjRkYTAzYTA5NWYKGQiIiIzew5e1nWkQwOPCzwYYsws4CEASSAQQAxoCbXkiIDM0ZDRlNDBhZWZiMDNlNWZjNmRhM2IwYWM3ZjhiNzMyMk4KIDpYC3K7NOcsGRIr858btYffripOOxvK-glVoXoDjaBBEiAZ2lLmGYxYd9iJJYArN_bfofK8lshmuGcK_e_Tb4N6hhgCIgZ0aWt0b2s; ssid_ucp_v1=1.0.1-KDhmMzE4MTlkZTFlN2FhNGM3NGRiMzlhYzAyNGJmNjRkYTAzYTA5NWYKGQiIiIzew5e1nWkQwOPCzwYYsws4CEASSAQQAxoCbXkiIDM0ZDRlNDBhZWZiMDNlNWZjNmRhM2IwYWM3ZjhiNzMyMk4KIDpYC3K7NOcsGRIr858btYffripOOxvK-glVoXoDjaBBEiAZ2lLmGYxYd9iJJYArN_bfofK8lshmuGcK_e_Tb4N6hhgCIgZ0aWt0b2s; cookie-consent={%22optional%22:false%2C%22ga%22:false%2C%22af%22:false%2C%22fbp%22:false%2C%22lip%22:false%2C%22bing%22:false%2C%22ttads%22:false%2C%22reddit%22:false%2C%22hubspot%22:false%2C%22version%22:%22v10%22}; odin_tt=18bbc9f38da5632127203af8e1e35f6b303ed37498379345447f677e7c317b777e82924a6b696e2dc0cd2983eae071f2022957002212832234bb3699d1297524; store-country-sign=MEIEDGvhnV6qfB2RxuaelAQgxYHWj_EZZLQTryiC1DBQ_QcA4TFjLbb8MtdmrKxhuO8EEDkdGyFx389MkyegNxc9eb4; ttwid=1%7Cux-eYkzfXdOl-hq2_COtip6Ixked0Q1qYfNLofOuO0E%7C1780768704%7C4869574822766afa890901530c8700cc804642438fc6e5f29b1a72a2b692a9a4; tt_csrf_token=wHoWvy4m-nmXFTPZzrmC6BAozb2FYnDMWVbs; msToken=ByoiLL7lk7BAFc4hUCVJGvXKAMhRzGS2XcSZldk_k4KkoRAuZiHS4qeEfcUWyN-4jSjO4b9iEwvuNDDNWTdXeMSw2ze6Nuu8EeS97unXemVkN7f1-3HkSkRvfUcxOjg_jiqxcH2we_uPB23OsGGxymJo-A==',
    'origin': 'https://www.tiktok.com',
    'referer': 'https://www.tiktok.com/',
    'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
}

def sanitize_filename(caption_text):
    if not caption_text or caption_text.strip() == "":
        return "tiktok_video"
    clean = re.sub(r'[\\/*?:"<>|]', "", caption_text).strip()
    return clean if clean else "tiktok_video"

def extract_videos_with_metadata(initial_url):
    try:
        response1 = requests.get(initial_url, headers=HEADERS, allow_redirects=True, timeout=30)
        final_url = response1.url
        response2 = requests.get(final_url, headers=HEADERS, timeout=30)
        
        html_content = response2.text
        html_content = html_content.replace(r"\u002F", "/").replace(r"\u002f", "/").replace(r"\/", "/")

        thumbnail_url = ""
        cover_match = re.search(r'"CoverList"\s*:\s*\[\s*"([^"]+)"', html_content)
        if cover_match:
            thumbnail_url = cover_match.group(1)

        url_list_matches = list(re.finditer(r'"UrlList"\s*:\s*\[', html_content))
        video_list = []
        seen_resolutions = set()

        for match in url_list_matches:
            start_pos = match.start()
            
            desc_pos = html_content.rfind('"desc"', 0, start_pos)
            caption = "TikTok Video Stream"
            if desc_pos != -1:
                desc_segment = html_content[desc_pos:desc_pos + 600]
                desc_match = re.search(r'"desc"\s*:\s*"([^"]*?)"', desc_segment)
                if desc_match:
                    caption = desc_match.group(1)

            width_pos = html_content.rfind('"width"', 0, start_pos)
            if width_pos == -1 or (start_pos - width_pos > 2500):
                width_pos = html_content.rfind('"Width"', 0, start_pos)

            height_pos = html_content.rfind('"height"', 0, start_pos)
            if height_pos == -1 or (start_pos - height_pos > 2500):
                height_pos = html_content.rfind('"Height"', 0, start_pos)

            width, height = "Unknown", "Unknown"
            if width_pos != -1:
                w_match = re.search(r'"[Ww]idth"\s*:\s*(\d+)', html_content[width_pos:width_pos+50])
                if w_match: width = w_match.group(1)
            if height_pos != -1:
                h_match = re.search(r'"[Hw]eight"\s*:\s*(\d+)', html_content[height_pos:height_pos+50])
                if h_match: height = h_match.group(1)

            resolution_str = f"{width}x{height}"
            
            if resolution_str in seen_resolutions or resolution_str == "UnknownxUnknown":
                continue

            end_pos = html_content.find(']', match.end())
            if end_pos == -1: 
                end_pos = match.end() + 2000
                
            list_zone = html_content[match.end():end_pos]
            url_pattern = r'(https://[^\s"\'<>,\\]*?webapp-prime\.tiktok\.com/video/tos/[^\s"\'<>,\\]+)'
            urls_in_this_list = re.findall(url_pattern, list_zone)
            
            if urls_in_this_list:
                seen_resolutions.add(resolution_str)
                video_list.append({
                    "url": urls_in_this_list[0],
                    "resolution": resolution_str,
                    "caption": caption
                })
                
        return {"thumbnail": thumbnail_url, "videos": video_list}
    except Exception:
        return {"thumbnail": "", "videos": []}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_links', methods=['POST'])
def get_links():
    data = request.get_json()
    user_url = data.get('url', '').strip()
    if not user_url:
        return jsonify({"success": False, "message": "URL cannot be empty."})
    
    result = extract_videos_with_metadata(user_url)
    if not result["videos"]:
        return jsonify({"success": False, "message": "No downloadable video options found."})
    
    return jsonify({"success": True, "thumbnail": result["thumbnail"], "videos": result["videos"]})

@app.route('/download_video', methods=['POST'])
def download_video():
    data = request.get_json()
    video_url = data.get('url')
    caption = data.get('caption', 'tiktok_video')
    
    try:
        res = requests.get(video_url, headers=HEADERS, stream=True, timeout=30)
        if res.status_code == 200:
            safe_name = sanitize_filename(caption)
            video_bytes = io.BytesIO(res.content)
            
            # Cloud Safe: Sends file straight to client download pipeline natively
            return send_file(
                video_bytes,
                mimetype='video/mp4',
                as_attachment=True,
                download_name=f"{safe_name}.mp4"
            )
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    # Port is set dynamically for cloud services, defaults to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
an", local_path], check=False)
            
            return send_file(
                video_bytes,
                mimetype='video/mp4',
                as_attachment=True,
                download_name=f"{safe_name}.mp4"
            )
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
