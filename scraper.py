import requests
import json
import os

def update_concerts():
    # 透過 KKTIX 公開的 API 抓取最新活動
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
    
    # 檢查抓下來的活動，篩選出跟演唱會或音樂有關的
    for entry in feed.get('entry', []):
        title = entry.get('title', '')
        if '演唱' in title or '音樂' in title or 'LIVE' in title.upper():
            # 解析日期
            published = entry.get('published', '')
            month_str = published[5:7] + "月" if len(published) >= 7 else "近期"
            day_str = published[8:10] if len(published) >= 10 else "TBD"
            
            # 將 KKTIX 的資料轉成你網頁的格式
            new_data.append({
                "month": month_str,
                "day": day_str,
                "wk": "新進",
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
            
        if len(new_data) >= 3: # 每次最多只新增 3 筆最新活動
            break

    # 讀取你原本舊的 data.json 檔案
    old_data = []
    if os.path.exists('data.json'):
        with open('data.json', 'r', encoding='utf-8') as f:
            old_data = json.load(f)

    # 清除上一批由系統自動抓取的舊資料 (避免重複堆疊)
    old_data = [d for d in old_data if d.get('statusText') != '最新上架']
    
    # 把新抓到的活動加在最上面，後面接著你原本的資料
    combined_data = new_data + old_data

    # 把新資料寫回 data.json
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)
    
    print(f"成功更新！新增了 {len(new_data)} 筆最新活動。")

if __name__ == "__main__":
    update_concerts()
