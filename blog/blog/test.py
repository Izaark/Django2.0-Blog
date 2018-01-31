'''


curl -X POST -d "username=username&password=password" http://localhost:8000/api/auth/token/
out: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6Iml6YWFrMjAwQGdtYWlsLmNvbSIsInVzZXJuYW1lIjoiaXNhYWMiLCJleHAiOjE1MTczODE0NDl9.4gF9-xiOjmGT2f6iBMwsLYGvWeYvIwJ54WgwZLk2iz8

Alternatively alternative to the above: curl -X POST -H "Content-Type: application/json" -d '{"username":"isaac","password":"geek5000"}' http://localhost:8000/api/auth/token/
out: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6Iml6YWFrMjAwQGdtYWlsLmNvbSIsInVzZXJuYW1lIjoiaXNhYWMiLCJleHAiOjE1MTczODE2ODZ9.S9bA2pLbGkY_sIepyzZfogrmVCZz8s0TK1zyyKeAIRY

curl -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MTczODIwNDAsImVtYWlsIjoiaXphYWsyMDBAZ21haWwuY29tIiwidXNlcm5hbWUiOiJpc2FhYyIsInVzZXJfaWQiOjF9.Y2E-G7P2nEQ8UPZ8PaJZyQH3OShOhUob1PDoOlZbn4s" http://localhost:8000/api/comments/
out: {"count":10,"response":[{"url":"http://localhost:8000/api/comments/67/","id":67,"content":"gggg .l.","timestamp":"2018-01-28T05:40:23.536803Z","reply_count":4},{"url":"http://localhost:8000/api/comments/61/","id":61,"content":"for users, developers, ark is the best","timestamp":"2018-01-24T06:39:06.071744Z","reply_count":1},{"url":"http://localhost:8000/api/comments/58/","id":58,"content":"ark es coll !!!","timestamp":"2018-01-24T06:10:31.076554Z","reply_count":2},{"url":"http://localhost:8000/api/comments/54/","id":54,"content":"la verdad me gusta mucho alv :D","timestamp":"2018-01-20T01:56:33.806131Z","reply_count":3},{"url":"http://localhost:8000/api/comments/49/","id":49,"content":"eeee","timestamp":"2018-01-19T21:32:23.725978Z","reply_count":1},{"url":"http://localhost:8000/api/comments/6/","id":6,"content":"eth desde admin django","timestamp":"2018-01-18T19:36:54.751265Z","reply_count":3},{"url":"http://localhost:8000/api/comments/5/","id":5,"content":"hmmmm","timestamp":"2018-01-18T19:34:28.238708Z","reply_count":0},{"url":"http://localhost:8000/api/comments/4/","id":4,"content":"h . bb","timestamp":"2018-01-18T19:25:13.233860Z","reply_count":0},{"url":"http://localhost:8000/api/comments/3/","id":3,"content":"es bueno la tecnología por contratos inteligentes es mas seguro y se forma aut.","timestamp":"2018-01-18T01:46:05.997106Z","reply_count":5},{"url":"http://localhost:8000/api/comments/2/","id":2,"content":"Me encanta ETH","timestamp":"2018-01-18T01:18:46.681873Z","reply_count":0}],"links":{"previous":null,"next":null},"code":200} 

curl -X POST -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MTczODMxODMsImVtYWlsIjoiaXphYWsyMDBAZ21haWwuY29tIiwidXNlcm5hbWUiOiJpc2FhYyIsInVzZXJfaWQiOjF9.s8-PkaGSDslXIb3VJYzZ1wNRO1G7eteMy2V8vRgVwuk" -H "Content-Type: application/json" -d '{"content":"comentario with autj jwt"}'  http://localhost:8000/api/comments/create/?slug=ark&type=post
out: {"id":74,"content":"comentario with autj jwt","timestamp":"2018-01-31T07:15:03.358704Z"}


curl -X POST -H "Content-Type: application/json" -d '{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImlzYWFjIiwiZW1haWwiOiJpemFhazIwMEBnbWFpbC5jb20iLCJvcmlnX2lhdCI6MTUxNzM4NjkwNCwidXNlcl9pZCI6MSwiZXhwIjoxNTIwODQyOTA0fQ.8hhW2uwP5y20-HOCDWqTPECrGtzr0s29y9MglYxyc_c"}' http://localhost:8000/api/auth/token/refresh/


curl -X POST -H "Content-Type: application/json" -d '{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MTczODcxMzMsInVzZXJfaWQiOjEsInVzZXJuYW1lIjoiaXNhYWMiLCJlbWFpbCI6Iml6YWFrMjAwQGdtYWlsLmNvbSJ9.JCH08WkPsHjl6BJzkbh6NldFvjPEt9o07XJ7aK65b-k"}' http://localhost:8000/api/auth/token/verify/
'''