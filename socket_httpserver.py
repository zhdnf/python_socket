import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(("0.0.0.0", 9090))
sock.listen(1)

res1 = b"HTTP/1.1 200 OK\r\n\r\n"
res1 += b"<!DOCTYPE HTML>"
res1 += b"<html>"
res1 += b"<head><title>Index</title></head>"
res1 += b"<body>"
res1 += b"<h1>Index</h1>"
res1 += b"</body>"
res1 += b"</html>"

res2 = b"HTTP/1.1 200 OK\r\n\r\n"
res2 += b"<!DOCTYPE HTML>"
res2 += b"<html>"
res2 += b"<head><title>Test</title></head>"
res2 += b"<body>"
res2 += b"<h1>Test</h1>"
res2 += b"</body>"
res2 += b"</html>"

res3 = b"HTTP/1.1 200 OK\r\n\r\n"
res3 += b"<!DOCTYPE HTML>"
res3 += b"<html>"
res3 += b"<head><title>news</title></head>"
res3 += b"<body>"
res3 += b"<p>title:{{category}}</p>"
res3 += b"<p>date :{{date}}</p>"
res3 += b"</body>"
res3 += b"</html>"


res4 = b"HTTP/1.1 200 OK\r\n\r\n"
res4 += b"<!DOCTYPE HTML>"
res4 += b"<html>"
res4 += b"<head><title>Login</title></head>"
res4 += b"<body>"
res4 += b"<form method='POST' action='/Login'>"
res4 += b"<label>username</label><input type='text' name='username'></br>"
res4 += b"<label>password</label><input type='text' name='password'></br>"
res4 += b"<input type='submit' value='Login'>"
res4 += b"</form>"
res4 += b"</body>"
res4 += b"</html>"

res_f_r = b"HTTP/1.1 302 FOUND\r\nLocation: /fail\r\n\r\n"


res_f = b"HTTP/1.1 200 OK\r\n\r\n"
res_f += b"<!DOCTYPE HTML>"
res_f += b"<html>"
res_f += b"<head><title>Fail</title></head>"
res_f += b"<body>"
res_f += b"<h1>Fail</h1>"
res_f += b"</body>"
res_f += b"</html>"

res_s =  b"HTTP/1.1 302 FOUND\r\n"
res_s +=  b"Location: /Login\r\n"
res_s +=  b"Set-Cookie: username=hah; Path=/; Domain=10.163.197.105\r\n"
res_s +=  b"Connection: close\r\n\r\n"


res404 = b"HTTP/1.1 200 OK\r\n\r\n"
res404 += b"<!DOCTYPE HTML>"
res404 += b"<html>"
res404 += b"<head><title>404</title></head>"
res404 += b"<body>"
res404 += b"<h1>404</h1>"
res404 += b"</body>"
res404 += b"</html>"

try:
    while True:
        conn, addr = sock.accept()
        req_init = conn.recv(100000).decode("utf8")
        req = req_init.split("\r\n")
        req_text = req_init.split("\r\n\r\n")[1]
        url = req[0].split(" ")[1]
        val = ""
        if "?" in url:
            path = url.split("?")[0]
            val = url.split("?")[1]
        else:
            path = url
        print(path)
        if path == "/":
            conn.send(res1)
        elif path == "/test":
            conn.send(res2)
        elif path == "/news":
            if val == None:
                categroy =  default
                date= "null"
            else: 
                tp = val.split("&")
                for i in tp:
                    if  i.split("=")[0] == "categroy":
                        category = i.split("=")[1]
                    elif i.split("=")[0] == "date":
                        date = i.split("=")[1]
                    else:
                        category = "default"
                        date = "null"
            res3_replace =res3.replace(b"{{category}}",category.encode("utf-8")).replace(b"{{date}}",date.encode("utf-8"))
            conn.send(res3_replace)
        elif path == "/Login":
            method = req[0].split(" ")[0]
            if method == "GET":
                conn.send(res4)
            elif method == "POST":
                f_tp = req_text.split("&")
                f_dict = {}
                for i in f_tp:
                    f_dict[i.split("=")[0]] = i.split("=")[1]
                if f_dict["username"]=="hah" and f_dict["password"]=="123":
                    conn.send(res_s)
                else:
                    conn.send(res_f_r)
        elif path == "/fail":
            conn.send(res_f)
        else:
            conn.send(res404)
        conn.close()

except KeyboardInterrupt:
    conn.close()
    print("Bye.")
    exit(0)

except Exception as e:
    print(e)
    conn.close()
    print("Exit")
    exit(1)
