import requests
import json
import subprocess

def download_file(url, filename, headers):
    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"下载完成: {filename}")
    except Exception as e:
        print(f"下载失败: {e}")
        exit()


# 配置参数
bvid = "BV1RdA6eBE4o"
cid = "28469822280"
params = {
    "bvid": bvid,
    "cid": cid,
    "qn": 80,
    "fnval": 4048,
    "fourk": 1
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
    "Referer": f"https://www.bilibili.com/video/{bvid}",
    "Cookie": "buvid3=FDD03CC8-55C4-FD1D-40A2-CAFFDA17C00E13715infoc; b_nut=1739545413; _uuid=D6B10378D-DA9D-5F53-10B1C-5E4FAE7AC9A813881infoc; enable_web_push=DISABLE; enable_feed_channel=DISABLE; DedeUserID=133787074; DedeUserID__ckMd5=fa74e2a3c3202695; header_theme_version=CLOSE; rpdid=|(J|)l|~mkYl0J'u~JmlRYJ|~; buvid4=83649C48-A067-D096-ABFD-221619077BA388420-023111122-ho21%2BqF6LZpSzGHiDpgOe9m9UNeZgHT9UIz%2Bn5qCtod3CXAdyJMahA%3D%3D; buvid_fp_plain=undefined; fingerprint=673ce83b201d91b5a5ccf4208f04e347; home_feed_column=5; CURRENT_QUALITY=80; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDA4Mzg1NjAsImlhdCI6MTc0MDU3OTMwMCwicGx0IjotMX0.9VR8u9ZlIpQKUEZpUbRpl6TpA8IpyfUv5BE4RqXCeXA; bili_ticket_expires=1740838500; SESSDATA=daf7e97c%2C1756145225%2C211ed%2A22CjCpktbKtj4hkEKRkCp8m4vSjn1Q9tHmxgkWVl6FZu5EV7--hysQ28cAOcHkf2PWfckSVkZhZTRJdXp4UlNmRGNOcEtqdE9pQ3FVTlFhRDZIUWlDSDdNVDJwR0Rvdy1sTW9oV0w3aTg1SENvWnJ4T0szQ25uSEVBZm9lQVJSekZVOE5CZkt1cTVnIIEC; bili_jct=40d7a360ef26b681e2ac2832a5757d79; LIVE_BUVID=AUTO9817406586465324; PVID=5; b_lsid=4E1EE7BE_1954C660AFA; browser_resolution=1526-1312; CURRENT_FNVAL=2000; sid=8rh3gabx; bmg_af_switch=1; bmg_src_def_domain=i2.hdslb.com; bp_t_offset_133787074=1038974647854432256; buvid_fp=FDD03CC8-55C4-FD1D-40A2-CAFFDA17C00E13715infoc"
}

# 获取视频元数据
response = requests.get("https://api.bilibili.com/x/player/wbi/playurl", params=params, headers=headers)
data = response.json()

if data.get("code") != 0:
    print("请求失败:", data.get("message"))
    exit()

try:
    dash_data = data["data"]["dash"]
    video_urls = [video["base_url"] for video in dash_data["video"]]
    audio_urls = [audio["base_url"] for audio in dash_data["audio"]]
except KeyError as e:
    print("JSON结构异常:", e)
    exit()

# 下载第一个分片（实际需遍历所有分片）
download_file(video_urls[0], "video.m4s", headers)
download_file(audio_urls[0], "audio.m4s", headers)

# 合并文件
subprocess.run([
    "ffmpeg", "-y",
    "-i", "video.m4s",
    "-i", "audio.m4s",
    "-c:v", "copy",
    "-c:a", "copy",
    "output.mp4"
])