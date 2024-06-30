# openssl req -x509 -new -nodes -key naina.key -sha256 -days 1024 -out naina.crt
# openssl genrsa -out naina.key 2048
# openssl pkcs12 -export -in naina.crt -inkey naina.key -out naina.p12
# openssl pkcs12 -in naina.p12 -nodes -out naina.pem
# sudo openssl req -newkey rsa:2048 -sha256 -nodes -keyout naina.key -x509 -days 365 -out naina.pem -subj "/C=IN/ST=TS/L=HYD/O=NAINA/CN=3.7.92.227"

# getwebhook ------  https://api.telegram.org/bot1043633896:AAGTiCkJ_J_v9tNkDTBHGbkNCuGr12I9FUE/getWebhookInfo
# delete webhook ------ https://api.telegram.org/bot1043633896:AAGTiCkJ_J_v9tNkDTBHGbkNCuGr12I9FUE/deleteWebHook?url=https://3.7.92.227/telegram
# add webhook ---- curl -F "url=https://3.7.92.227/" -F "certificate=@/etc/nginx/ssl/naina.pem" https://api.telegram.org/bot1043633896:AAGTiCkJ_J_v9tNkDTBHGbkNCuGr12I9FUE/setWebHook
