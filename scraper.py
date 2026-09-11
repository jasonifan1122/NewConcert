import json
import os
from datetime import datetime

def update_concerts():
    # 取得現在的時間
    now_time = datetime.now().strftime("%H:%M:%S")
    
    # 直接在程式內生成一筆假資料，完全不對外發送請求，保證不會被擋！
    new_data = [{
        "month": "測試",
        "day": "成功",
        "wk": "系統",
        "artist": f"機器人自動更新測試 (時間: {now_time})",
        "tags": ["mando"], 
        "famous": True,
        "venue": "GitHub 雲端主機",
        "sale": "剛剛",
        "platform": "自動化系統",
        "status": "wait",
        "statusText": "最新上架",
        "url": "https://github.com"
    }]

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
    
    print(f"成功強制寫入測試資料！時間: {now_time}")

if __name__ == "__main__":
    update_concerts()
