with open('diary.txt','a',encoding='utf-8') as file:
    date = input('今日の日付をyyyymmddの形で入力してください：')
    file.write(date + '\n')
    entry = input('今日の日記を入力してください：')
    file.write(entry + '\n')
print('日記は保存されました、今日も1日ご苦労さまでした！！！')
print('ブランチfeature2で行を追加')