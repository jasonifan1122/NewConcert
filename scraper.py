import requests
import json
import os

def update_concerts():
    url = "https://kktix.com/events.json"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        feed = response.json()
    except Exception as e:
        print(f"抓取失敗: {e}")
        return

    new_data = []
    
    # 這次我們不設任何關鍵字過濾條件，直接抓前 3 筆最新活動！
    for entry in feed.get('entry', [])[:3]:
        title = entry.get('title', '')
        published = entry.get('published', '')
        month_str = published[5:7] + "月" if len(published) >= 7 else "近期"
        day_str = published[8:10] if len(published) >= 10 else "TBD"
        
        new_data.append({
            "month": month_str,
            "day": day_str,
            "wk": "自動",
            "artist": title[:20] + ("..." if len(title)>20 else ""), # 標題太長自動截斷
            "tags": ["mando"], 
            "famous": False,
            "venue": "詳見 KKTIX 官網",
            "sale": "系統自動抓取",
            "platform": "KKTIX",
            "status": "wait",
            "statusText": "最新上架",
            "url": entry.get('url', 'https://kktix.com/')
        })

    # 讀取舊資料並替換
    old_data = []
    if os.path.exists('data.json'):
        with open('data.json', 'r', encoding='utf-8') as f:
            old_data = json.load(f)

    # 清除舊的自動抓取紀錄
    old_data = [d for d in old_data if d.get('statusText') != '最新上架']
    
    # 合併後寫入
    combined_data = new_data + old_data
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)
    
    print("成功強制寫入 3 筆測試資料！")

if __name__ == "__main__":
    update_concerts()
