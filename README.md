# pttCrawler

1. 對ptt某看板進行爬蟲

2. 串接 line通知, 需先至https://notify-bot.line.me/zh_TW/ , 申請token

3. 設定每15分鐘爬蟲一次

4. 爬到的data若有觸發line通知, 會暫存在記憶體內, 避免重複通知。每日23:30會 clear 存放的set
