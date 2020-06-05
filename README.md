# MORGORITHM API


## 요청 방법

### 1. 사용자 인증
```js
// ...
headers: {
  "Authorization": `Token ${token}`,
  // token : 로그인 인증 토큰 (로그인 / 회원 가입시 발급)
},
// ...
```
### 2. post/put/delete 데이터 요청 방법
```js
{
  method: "POST",
  headers: {
    "Authorization": `Token ${token}`,
    "Content-Type": "application/json"
  }
}
```

<br />

## API 사용법

### 1. User

> 사용자 인증 불필요 API

| url | method | data(query) | return | 기능 |
|---|---|---|---|---|
|`/api/v1/users/signup/`|POST| username(string), name(string)(option), password(string) |id, username, name, avatar|회원 가입|
|`/api/v1/users/signin/`|POST| username(string), password(string) |id, username, name, avatar| 로그인 |

> 사용자 인증 필요 API

| url | method | data(query) | return | 기능 |
|---|---|---|---|---|
|`/api/v1/users/`|GET| username |id, username, name, avatar|username params가 존재하면 해당 유저를, 아니면 현재 로그인 한 유저의 정보를 반환|
|`/api/v1/users/`|PUT| username(string), name(string) |id, username, name, avatar|유저 정보 수정|
|`/api/v1/users/`|DELETE| password(string) | |회원 탈퇴|
|`/api/v1/users/signout/`|GET| | | 로그아웃 |
|`/api/v1/users/change_password/`|POST| password(string) | | 로그아웃 |
|`/api/v1/users/profile_image/`|PUT| avatar(image) |id, username, name, avatar| 프로필 이미지 수정 |
|`/api/v1/users/profile_image/`|DELETE| | | 프로필 이미지 삭제 |
|`/api/v1/users/group/`|GET| keyword(option) | id, name, members(id, username, name, avatar), members_count, is_private, is_joined | 검색된 그룹 혹은 모든 그룹 중 10개 가져오기|
|`/api/v1/users/group/`|POST| name(string), password(string)(option) |id, name, members(id, username, name, avatar), members_count, is_private, is_joined | 그룹 생성 |
|`/api/v1/users/group/<int:group_id>/`|GET| | id, name, members(id, username, name, avatar), members_count, is_private, is_joined | 그룹 상세 가져오기 |
|`/api/v1/users/group/<int:group_id>/enter/`|POST| password(string)(option) | id, name, members(id, username, name, avatar), members_count, is_private, is_joined | 그룹 가입 |
|`/api/v1/users/group/<int:group_id>/leave/`|GET| |  | 그룹 나가기 |



### 2. Problem (모두 사용자 인증 필요)

| url | method | data(query) | return | 기능 |
|---|---|---|---|---|
|`/api/v1/problems/`|POST|group(array of problem group id), category(array of string), level(array of int), solved(null or true or false), keyword(string)|id, origin(id, level, url, number, category, title, remark), is_solved, solved_time|주어진 데이터들을 기반으로 페이징된(10개씩) 문제들 가져오기|
|`/api/v1/problems/<int:origin_id>/`|GET| |id, origin(id, level, url, number, category, title, remark), is_solved, solved_time|original problem id를 기반으로 로그인된 유저의 문제 가져오기|
|`/api/v1/problems/fetch/`|POST|level(int), url(url), number(int), category(string), title(string), remark(string)|id, level, url, number, category, title, remark|origin problem 하나를 새로 데이터베이스에 생성|
|`/api/v1/problems/init/`|GET| |id, origin(id, level, url, number, category, title, remark), is_solved, solved_time|유저의 마지막 업데이트 시간보다 늦게 생성된 original problem들을 복사해 유저에게 할당하고 반환하기|
|`/api/v1/problems/group/`|POST|name(string), problems(array of problem id)|id, name, problems_count, solutions_count|문제리스트를 만들고 문제 넣기|
|`/api/v1/problems/group/<int:group_id>/`|POST| adding_problems(array of problem id), removing_problems(array of problem id) |id, name, problems_count, solutions_count|문제리스트에 문제 넣고 빼기|
|`/api/v1/problems/group/<int:group_id>/`|PUT| name(string) | id, name, problems_count, solutions_count |문제리스트 이름 비꾸기|
|`/api/v1/problems/group/<int:group_id>/`|DELETE| | | 문제리스트 삭제|



### 3. Solution (모두 사용자 인증 필요)
| url | method | data(query) | return | 기능 |
|---|---|---|---|---|
|`/api/v1/solutions/`|GET|solved(None/true/false), user(None/user id), problem(None/problem id), group(None/problem grouop id)|id, code, lang, caption, solved, creator(id, username, name, avatar), problem(id, level, url, number, category, title, remark), view, likes_count, comments_count|query params를 기반으로 풀이 가져오기|
|`/api/v1/solutions/`|POST|problem(origin problem id), code(string), lang(string - c/cpp/java/python/javascript), solved(boolean), caption(string)(option)|id, code, lang, caption, solved, creator(id, username, name, avatar), problem(id, level, url, number, category, title, remark), view, likes_count, comments_count|풀이 생성|
|`/api/v1/solutions/<int:solution_id>/`|GET| |id, code, lang, caption, solved, creator(id, username, name, avatar), problem(id, level, url, number, category, title, remark), view, likes_count, comments_count|상세 풀이 가져오기|
|`/api/v1/solutions/<int:solution_id>/`|PUT|code(string), lang(string), caption(string) |id, code, lang, caption, solved, creator(id, username, name, avatar), problem(id, level, url, number, category, title, remark), view, likes_count, comments_count|풀이 수정|
|`/api/v1/solutions/<int:solution_id>/`|DELETE| | |풀이 삭제|
|`/api/v1/solutions/<int:solution_id>/like/`|GET| |좋아요가 눌리면 201 반환, 사라지면 204 반환 |좋아요 혹은 좋아요 취소|
|`/api/v1/solutions/<int:solution_id>/comments/`|GET| | id, solution(id), creator(id, username, name, avatar), message, likes(array of [id, username, name, avatar]), likes_count, natural_time, is_liked |풀이에 대한 댓글 모두 가져오기|
|`/api/v1/solutions/<int:solution_id>/comments/`|POST| message(string) | id, solution(id), creator(id, username, name, avatar), message, likes(array of [id, username, name, avatar]), likes_count, natural_time, is_liked | 풀이에 대한 댓글 생성 |
|`/api/v1/solutions/comments/<int:comment_id>/`|PUT| message(string) | id, solution(id), creator(id, username, name, avatar), message, likes(array of [id, username, name, avatar]), likes_count, natural_time, is_liked | 댓글 수정 |
|`/api/v1/solutions/comments/<int:comment_id>/`|DELETE| | | 댓글 삭제 |
|`/api/v1/solutions/comments/<int:comment_id>/like/`|GET| |좋아요가 눌리면 201 반환, 사라지면 204 반환 |좋아요 혹은 좋아요 취소|