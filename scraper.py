import cloudscraper
import json
import os

def update_concerts():
    print("啟動偽裝爬蟲，準備前往 KKTIX...")
    # 使用 cloudscraper 建立一個會模擬真實瀏覽器的爬蟲
    scraper = cloudscraper.create_scraper()
    url = "https://kktix.com/events.json"
    
    try:
        response = scraper.get(url)
        response.raise_for_status()
        feed = response.json()
    except Exception as e:
        print(f"抓取失敗，可能防護等級提升了: {e}")
        return

    new_data = []
    
    # 檢查抓下來的活動，篩選出跟演唱會或音樂有關的
    for entry in feed.get('entry', []):
        title = entry.get('title', '')
        # 嚴格篩選：只抓取標題有這些字的活動
        if '演唱' in title or '音樂' in title or 'LIVE' in title.upper():
            published = entry.get('published', '')
            month_str = published[5:7] + "月" if len(published) >= 7 else "近期"
            day_str = published[8:10] if len(published) >= 10 else "TBD"
            
            new_data.append({
                "month": month_str,
                "day": day_str,
                "wk": "自動",
                "artist": title[:18] + ("..." if len(title)>18 else ""),
                "tags": ["mando"], 
                "famous": False,
                "venue": "詳見 KKTIX 官網",
                "sale": "系統自動抓取",
                "platform": "KKTIX",
                "status": "wait",
                "statusText": "最新上架",
                "url": entry.get('url', 'https://kktix.com/')
            })
            
        if len(new_data) >= 3: # 每次最多只新增 3 筆
            break

    # 讀取舊資料並替換
    old_data = []
    if os.path.exists('data.json'):
        with open('data.json', 'r', encoding='utf-8') as f:
            old_data = json.load(f)

    # 清除舊的自動抓取紀錄 (包含我們剛剛的測試卡片)
    old_data = [d for d in old_data if d.get('statusText') != '最新上架']
    
    # 合併後寫入
    combined_data = new_data + old_data
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)
    
    print(f"成功突破！抓到了 {len(new_data)} 筆真實音樂活動。")

if __name__ == "__main__":
    update_concerts()
