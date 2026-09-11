import requests
import xml.etree.ElementTree as ET
import json
import os

def update_concerts():
    print("準備抓取最新演唱會新聞...")
    
    # 這是 Google 新聞的 RSS 網址，專門搜尋「台灣 演唱會」近 7 天的新聞
    url = "https://news.google.com/rss/search?q=台灣+演唱會+when:7d&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    
    try:
        # 新聞網站不防機器人，可以直接抓！
        response = requests.get(url)
        response.raise_for_status()
        
        # Google 新聞回傳的是 XML 格式，我們用內建工具解析它
        root = ET.fromstring(response.text)
    except Exception as e:
        print(f"抓取失敗: {e}")
        return

    new_data = []
    
    # 找到所有新聞項目 (item)，我們抓取前 3 篇最新的
    for item in root.findall('.//item')[:3]:
        title = item.find('title').text
        link = item.find('link').text
        pubDate = item.find('pubDate').text # 格式類似: Fri, 11 Sep 2026 12:00:00 GMT
        
        # 把新聞標題稍微縮短，避免把卡片撐破
        short_title = title[:22] + ("..." if len(title) > 22 else "")
        
        # 將新聞包裝成你網站的卡片格式
        new_data.append({
            "month": "新聞",
            "day": "快報",
            "wk": "自動",
            "artist": short_title,
            "tags": ["mando"], 
            "famous": False,
            "venue": "新聞情報，點擊前往查看",
            "sale": pubDate[5:16], # 擷取出日期的部分
            "platform": "Google 新聞",
            "status": "wait",
            "statusText": "最新上架",
            "url": link
        })

    # 讀取舊資料並替換
    old_data = []
    if os.path.exists('data.json'):
        with open('data.json', 'r', encoding='utf-8') as f:
            old_data = json.load(f)

    # 清除舊的自動抓取紀錄（把上次失敗卡在裡面的測試資料也清掉）
    old_data = [d for d in old_data if d.get('statusText') != '最新上架']
    
    # 合併後寫入
    combined_data = new_data + old_data
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)
    
    print(f"成功突破！抓到了 {len(new_data)} 篇演唱會新聞。")

if __name__ == "__main__":
    update_concerts()
