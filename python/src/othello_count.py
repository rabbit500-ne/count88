"""
main.py
    router.py
    server.py

"""
import rooter
import server

#------------------------------------------------
# main
#------------------------------------------------
def main():
    rooter.start()
    server.start()

"""
クライアント <-> サーバ
フォーマット

クライアント 要求電文
form="req"

サーバ　応答電文
form="cal01"
b="0x0080808080808080"
w="0x0080808080808080"

クライアント　報告電文
form="cal01return"
b="0x0080808080808080"
w="0x0080808080808080"
count=69804

"""
"""
“dbh.users.insert(user_doc, safe=True)”

抜粋:: Niall O'Higgins  “MongoDB & Python”。 Apple Books  

"""

if "__main__" == __name__ :
    main()