# HMC API

## User

### User
- [x] sign up
- [x] sign in
- [x] change password
- [ ] verify email
- [ ] init password
- [ ] update user profile (just name... )
- [ ] get user's info
- [ ] profile image

### Group
- [x] create group
- [x] enter group
- [x] leave group
- [x] search group
- [ ] get questions (unsolved solutions from group's members)


<br />

## Problem

### Original Problem
- [x] add original problem
- [ ] *<span style="color: #DDD;">나머지는 admin으로</span>*

### Problem
- [x] copy all original problem and get own problem
- [ ] (위에 추가 혹은 예외 만들기) remove own problem when original problem removed
- [ ] test get own problem when original problem deleted
- [ ] update own problem when solution modified
- [ ] (models, serializers) get problem count, solved_problem count, unsolved_problem count

### Problem Group
- [ ] add Problem Group (limit count)
- [ ] remove Problem Group
- [ ] modify Problem Group
- [ ] add own problems to problem group
- [ ] test get group's problems when original problem deleted


<br />

## Solution

### Solution
- [x] add solution to original problem
- [x] modify own solution <- **bad**
- [ ] change (modify own solution) to (if solved, add another solution solved and not change unsolved problem:)
- [x] delete own solution
- [ ] make good count field to solution model
- [ ] view count + 1
- [ ] good count + 1
- [ ] get solutions of own group users from own problem's original problem

### Comment
- [ ] add comment to solution
- [ ] modify own comment
- [ ] delete comment (comment owner, solution owner)
- [ ] get comments of solutions (get solutions에 넣을지 말지 결정)