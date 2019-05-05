# `Flask`实现`api token`

## 1. 项目结构说明

基于`AES`加密生成用户`token`，并将`token`保存在`redis`数据库中，经过设定的生存时间后过期。

## 2. 主要接口

* 用户注册

```
$ curl -v -X POST http://127.0.0.1:8888/token/users -H 'content-type: application/json' -d '{"un": "jason", "pd": "123456"}'
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1...
* Connected to 127.0.0.1 (127.0.0.1) port 8888 (#0)
> POST /token/users HTTP/1.1
> Host: 127.0.0.1:8888
> User-Agent: curl/7.47.0
> Accept: */*
> content-type: application/json
> Content-Length: 31
>
* upload completely sent off: 31 out of 31 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 201 CREATED
< Content-Type: application/json
< Content-Length: 26
< Location: http://127.0.0.1:8888/token/users/2
< Server: Werkzeug/0.14.1 Python/3.7.1
< Date: Sun, 05 May 2019 08:10:02 GMT
<
{
  "username": "jason"
}
* Closing connection 0
```

* 获取`token`

```
$ curl -v -u jason:123456 -X GET http://127.0.0.1:8888/token
Note: Unnecessary use of -X or --request, GET is already inferred.
*   Trying 127.0.0.1...
* Connected to 127.0.0.1 (127.0.0.1) port 8888 (#0)
* Server auth using Basic with user 'jason'
> GET /token HTTP/1.1
> Host: 127.0.0.1:8888
> Authorization: Basic amFzb246MTIzNDU2
> User-Agent: curl/7.47.0
> Accept: */*
>
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 102
< Server: Werkzeug/0.14.1 Python/3.7.1
< Date: Sun, 05 May 2019 08:10:07 GMT
<
{
  "duration": 600,
  "token": "zfkTrbS7MYE69bTK086Hzc7ChPTFXhI4NypDvRTuD/93+p9JlelmQ0qRZeduAHPc"
}
* Closing connection 0
```

* 密码验证取回数据

```
$ curl -v -u jason:123456 -X GET http://127.0.0.1:8888/data
Note: Unnecessary use of -X or --request, GET is already inferred.
*   Trying 127.0.0.1...
* Connected to 127.0.0.1 (127.0.0.1) port 8888 (#0)
* Server auth using Basic with user 'jason'
> GET /data HTTP/1.1
> Host: 127.0.0.1:8888
> Authorization: Basic amFzb246MTIzNDU2
> User-Agent: curl/7.47.0
> Accept: */*
>
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 30
< Server: Werkzeug/0.14.1 Python/3.7.1
< Date: Sun, 05 May 2019 08:11:34 GMT
<
[
  [
    2,
    "111"
  ]
]
* Closing connection 0
```

* `token`验证取回数据

```
$ curl -v -u zfkTrbS7MYE69bTK086Hzc7ChPTFXhI4NypDvRTuD/93+p9JlelmQ0qRZeduAHPc:unused -X GET http://127.0.0.1:8888/data
Note: Unnecessary use of -X or --request, GET is already inferred.
*   Trying 127.0.0.1...
* Connected to 127.0.0.1 (127.0.0.1) port 8888 (#0)
* Server auth using Basic with user 'zfkTrbS7MYE69bTK086Hzc7ChPTFXhI4NypDvRTuD/93+p9JlelmQ0qRZeduAHPc'
> GET /data HTTP/1.1
> Host: 127.0.0.1:8888
> Authorization: Basic emZrVHJiUzdNWUU2OWJUSzA4Nkh6YzdDaFBURlhoSTROeXBEdlJUdUQvOTMrcDlKbGVsbVEwcVJaZWR1QUhQYzp1bnVzZWQ=
> User-Agent: curl/7.47.0
> Accept: */*
>
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 30
< Server: Werkzeug/0.14.1 Python/3.7.1
< Date: Sun, 05 May 2019 08:11:35 GMT
<
[
  [
    2,
    "111"
  ]
]
* Closing connection 0
```