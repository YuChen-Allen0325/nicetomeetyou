# Unnotech Backend Engineer 徵才小專案

1. 抓取 http://tw-nba.udn.com/nba/index 中的焦點新聞。  (complete)  
2. 使用 [Django](https://www.djangoproject.com/) 設計恰當的 Model，並將所抓取新聞存儲至 DB。  (complete)
3. 使用 [Django REST Framework](http://www.django-rest-framework.org/) 配合 AJAX 實現以下頁面：  (complete)
	 * 焦點新聞列表
	 * 新聞詳情頁面
4. 以 Pull-Request 的方式將代碼提交。  (complete)
	
## 進階要求
1. 實現爬蟲自動定時抓取。  (complete)
2. 使用 Websocket 服務，抓取到新的新聞時立即通知前端頁面。 (undone)
3. 將本 demo 部署到伺服器並可正確運行。  (complete)
4. 所實現新聞列表 API 可承受 100 QPS 的壓力測試。  (complete)


# 本 Demo 筆記
---
焦點新聞並沒有所謂的日期排序, 也沒有點擊率類型的值可以抓取拿來排序, 所以這邊爬蟲抓取資料比對是否更新這件事都是全部一起比, 也因為如此排成抓取時所需的內存耗量會稍大一些(memory_profiler提供約略30 MiB左右), 不做成爬蟲一頁存一頁的原因是因為發起request到新聞頁所需時間其實挺久的, 會變向導致排程任務執行時 影響到 *焦點新聞列表 API 及 *新聞詳情頁面 API。


# 本 Demon 部屬及壓測部分
---
選用的技術為Docker swarm , AWS EC2, AWS ECR, K6

下圖為EC2擷取圖片, 啟用兩個EC2, 一個做為server端, 一個為PostgreSQL:

![image](https://github.com/YuChen-Allen0325/Unnotech_backend_django/assets/94295939/b4e0dd24-c7c0-4871-b825-8a2f32cffe1b)

Server端Docker部屬圖如下
![image](https://github.com/YuChen-Allen0325/Unnotech_backend_django/assets/94295939/c49e0ca6-e629-4281-ab61-9aec9337535e)




下圖為ECR 鏡像私有庫:
![image](https://github.com/YuChen-Allen0325/Unnotech_backend_django/assets/94295939/bdf3f61c-a034-4cbc-b72c-0584bc8247c3)




下圖為壓力測試結果 (可承受 200 QPS):
![K6_res](https://github.com/YuChen-Allen0325/Unnotech_backend_django/assets/94295939/63cc61d9-7182-45a1-b560-31f8c61f7639)

壓力測試JS範例(由chatGPT生程)
![image](https://github.com/YuChen-Allen0325/Unnotech_backend_django/assets/94295939/b9d4deeb-d1a8-498a-965a-23860221e137)




