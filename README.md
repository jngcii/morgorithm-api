# MORGORITHM API

## User

### User
- [x] sign up
- [x] sign in
- [x] change password
- [x] verify email
- [x] init password
- [x] update user profile (just name... )
- [x] get user's info
- [x] profile image

### Group
- [x] create group
- [x] enter group
- [x] leave group
- [x] search group
- [x] get questions (unsolved solutions from group's members)
- [x] search questions


<br />

## Problem
| url | method | data | return | 기능 |
|---|---|---|---|---|
|`/api/v1/problems/`|POST|group(array of id), category(array of string), level(array of int), solved(null or true or false), keyword(string)|id, origin(id, level, url, number, category, title, remark), is_solved, solved_time|주어진 데이터들을 기반으로 페이징된(10개씩) 문제들 가져오기|
|`/api/v1/problems/<int:origin_id>/`|GET| |id, origin(id, level, url, number, category, title, remark), is_solved, solved_time|original problem id를 기반으로 로그인된 유저의 문제 가져오기|
|`/api/v1/problems/fetch/`|POST|level(int), url(url), number(int), category(string), title(string), remark(string)|id, level, url, number, category, title, remark|origin problem 하나를 새로 데이터베이스에 생성|
|`/api/v1/problems/init/`|GET| |id, origin(id, level, url, number, category, title, remark), is_solved, solved_time|유저의 마지막 업데이트 시간보다 늦게 생성된 original problem들을 복사해 유저에게 할당하고 반환하기|

### Original Problem
- [x] add original problem
- [x] *<span styles="color: #DDD;">나머지는 admin으로</span>*

### Problem
- [x] copy all original problem and get own problem
- [x] (위에 추가 혹은 예외 만들기) remove own problem when original problem removed
- [x] test get own problem when original problem deleted
- [x] update own problem when solution modified

### Problem Group
- [x] add Problem Group (limit count)
- [x] remove Problem Group
- [x] modify Problem Group
- [x] add own problems to problem group
- [x] (models, serializers) get problem count, solved_problem count, unsolved_problem count


<br />

## Solution

### Solution
- [x] add solution to original problem
- [x] modify own solution <- **bad**
- [x] delete own solution
- [x] view count + 1
- [x] make like model and like count property field to solution model
- [x] like count + 1
- [x] get solutions of own group users from own problem's original problem
- [x] get solution detail by solution Id

### Comment
- [x] add comment to solution
- [x] modify own comment
- [x] delete comment (comment owner, solution owner)
- [x] add comments to get solutions serializer