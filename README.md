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