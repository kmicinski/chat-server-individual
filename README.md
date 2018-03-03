---
layout: project
title:  "Project 2I: SquirrelChat"
date:   2018-3-3
due: 2018-3-23
categories: project assignment
permalink: /project/3
---

In this project, you'll be writing a chat server. You'll interface
with this chat server in a variety of ways: you can either telnet to
it manually and send commands, interface using a client (which I'll
hand out in the next week or two), or (in project 3) using a web
frontend. The protocol is reminiscent of
[IRC](https://en.wikipedia.org/wiki/Internet_Relay_Chat) or
[Slack](https://en.wikipedia.org/wiki/Slack_(software)).

The SquirrelChat protocol is described precisely at the end of this
document. Your server must correctly implement all of the commands
according to the protocol. To test your server, you'll either use
`telnet` or hand-rolled testing scripts. I'll give you one or two of
these scripts upon project release, but I'll also require that you
write some of your own. I'll maintain a public Github repo to which
you will contribute tests via pull request.

I have implemented some basic stub code that does parsing for various
messages. You can write your SquirrelChat server in whatever language
you want, but my starter code is given in Python. I would welcome
implementations in OCaml, Haskell, etc.. But I assume no obligation to
teach you these languages as part of this project. If you use a
particularly cool language or a particularly elegant technique (e.g.,
if you go out on a limb and try to use Haskell to write the server), I
*may* award you 1-4 points of extra credit.

SquirrelChat is a fairly simple chat protocol. There are users, and
there are chatrooms. Users can join (or create) chatrooms. Chatrooms
have a set of "administrators" that can change their topic (a short
message that is associated with the channel). When a user sends a
message to a channel, all members of the channel receive it. Users can
also send private messages to each other. SquirrelChat also allows
users to block each other, and has a few security features (e.g., only
admins can change topics and ban users). Additionally, users may
upload files to channels or to another user.

In this assignment, you'll implement the core of SquirrelChat as a
server that my client can connect to. There are also a set of tests,
some of which I've given you (others which I haven't). SquirrelChat is
inherently insecure: it's executing over raw sockets, meaning that
people in the middle will be able to sniff all of the information sent
across SquirrelChat (e.g., someone sniffing packets in the same coffee
shop as you). In the next assignment we'll add multiple security
features to SquirrelChat: encryption, encrypted file storage, properly
saving passwords, and having properly encrypted chatrooms so that only
the members of secure rooms can see each others' messages.

This assignment is open-ended by design. Throughout the course of the
project, I will periodically release some tests for you, but I am not
under *obligation* to give you all of the tests I will use. If you
have any questions on the spec, please let me know and I'll update
immediately.

# Command Overview

SquirrelChat packets are specified as follows. See `parser.py` and
`messages.py` for details. This is the master specification.

**IMPORTANT Note**: the maximum length of *any* packet in this part of
the project is `1024`. You are *not* obligated to handle the case
where packets longer than that are sent.

- `register <username> <password>` [5 points]
  - Both `username` and `password` are contiguous strings (i.e., no spaces)
  - `username` may not start with the character `#` (used for channels).
  - Upon successfully sending `register`, the server automatically
    logs the user in as `<username>` with the associated password
  - Must save a new record in the password database for username and password (the password database is described below)
  - If the `username` or `password` is invalid, or if the register command is given more arguments, then the server should return an `error` message with some descriptive error of your choice.
  - Example: `register kmicinski helloworld234**`

- `authenticate <username> <password>` [5 points]
  - Checks the password file for the entry of `username` and `password` and--if the username matches the password--logs in the user.
  - If the `username` or `password` does not match the one stored in the password database, returns an `error` of the appropriate type.
  - Example: `register kmicinski helloworld234**`

- `update_pw <password>` [5 points]
  - User must be logged in
  - Updates a logged-in user's password as `<password>`
  - Also updates the password file
  - Example: `update_pw helloworld234**`

- `join <channel_name>` [5 points]
  - User must be logged in.
  - Validate that `<channel_name>` starts with `#`. All channels have
    `#` at the start of their name.
  - If the channel *exists*:
    - Check to make sure the user is not banned from the channel.
      - If they are, return an error message to the user indicating this.
    - If they are not banned, add the user to the channel, they will now 
      receive subsequent messages to that channel.
  - If the channel does *not* exist:
    - Create the channel
    - Make the sending user the administrator of the channel
    - Add the user as the only member of the channel
    - Set the topic to some initial message
 - Example: `join #hello`

- `chat <user_or_channel> <message>` [5 points]
  - `<user_or_channel>` is a contiguous string, but `<message>` is
    just the rest of the message.
  - This is a message that a *user* sends to the *server*
  - If the user is logged in, check to make sure that the user or
    channel exists. If they aren't, send an error back.
  - If `<user_or_channel>` starts with a `#`, it is a channel. Ensure
    that the user is logged in to the channel. If they are not, send
    back an `error` message of the appropriate type.
  - If it does not start with `#`, it is a user. Check to ensure the
    user exists. IF the user does not exist, send back an `error` of
    the appropriate type.
  - If `<user_or_channel>` is a user that has not blocked the
    currently logged in user. If they have, do nothing.
  - If they have not blocked the sender of the message, the server
    sends that user a `chatfrom` message.
  - Example: `chat #channel Hi there everyone!`
  - Example: `chat eliana Hi there, Eliana!`
    
- `chatfrom <from_user> <channel_or_privmsg> <message>` [5 points]
  - This is a command that the *server* sends to a *client*.
  - The way to interpret this is that `<from_user>` sent a message to
    channel `<channel_or_privmsg>` if `<channel_or_privmsg>` begins
    with `#`. If `<channel_or_privmsg>` is exactly the string
    `privmsg`, then this is a private message.
  - `<from_user>` is a logged in user.
  - This command will never be received from users who have been
    blocked by the client. In other words, if Alice has blocked Bob,
    Alice will never receive messages from Bob: either on channels to
    which Bob belongs, or through private messages.
  - Example: `chatfrom bob #hello Hello there, everyone!`
  - Example: `chatfrom bob privmsg Hello there, Alice!`

- `gettopic #channel` [5 points]
  - Gets the topic for a channel

- `topic #channel <topic>` [5 points]
  - The server returns this packet as the result of a `gettopic`
    command, assuming that the user is logged in to the given channel
   (i.e., has successfully run a `join` command for that channel).

- `settopic #channel <topic>` [5 points]
  - Sets the topic for a channel, assuming the sender is the
    administrator of that channel.
  - Sends back error otherwise.

- `leave #channel` [5 points]
  - The sender will now stop receiving `chatfrom` messages sent to
    `#channel`. If they were the administrator, they are still the
    administrator. Nobody else becomes an administrator.
  - Sender must be able to join again later.

- `error <msg>`
  - The server sends this error to a client in the event that an error
    occurs.

- `ban <channel> <user>` [5 points]
  - If the sender of this message is the administrator of `<channel>`,
    then `<user>` is now banned from `<channel>` and can no longer
    receive messages. I.e., it is essentially as if `<user>` had run
    the `leave` command.
  - If the sender is *not* the administrator, send an `error` of the
    appropriate type.

- `unban <channel> <user>` [5 points]
  - If the sender of this message is the administrator of `<channel>`,
    then `<user>` is now unbanned from `<channel>` and can `join`
    again.
  - If the sender is *not* the administrator, send an `error` of the
    appropriate type.

# Starting the Server

The server is started via (in the `server` directory)

    ./server passwords.csv

Where `passwords.csv` is a CSV file listing usernames and passwords
for the server. CSV files are in [Comma-Separated
Values](https://en.wikipedia.org/wiki/Comma-separated_values)
format. An example `passwords.csv` might look like this:

```
username,password
isabella,hacker12**@a3
john,aacv23aad%$aD
```

The file will *always* start with the header (first line) of
`username,password` and will be followed by a set of lines containing
usernames and values, each separated by a comma.

Any password database must be able to be used, not just
`passwords.csv`. Various commands (`register` and `update_pw`) will
*change* the database. You must *save* an updated database whenever
these commands are sent to the server.

# Part 0: Design Document (10 points)

This project is intended to give you practice programming "in the
large." You will need to use a variety of data structures to help you
implement this server. Specifically, think about the following:

- How you will implement chat rooms?
- How will users be represented? (E.g., as classes?)
- How will you manage the state of the protocol? I.e., how will you
  make sure users don't send messages until they are logged in?
- How will you handle blocking and banning?

Write this in an email / document / Google Doc / etc... And give it to
me before you start writing up your code so I can read over it. I will
point you in the right directions. If you are feeling anxious about
how to tackle this, come to my office and we will sketch it out on the
board.

# Part 1: Server Protocol Implementation (60 points)

This part is the majority of the project. You are to flesh out the
implementation of the server according to the command specification
given above. I have provided starter code in the `server` directory of
this project.

You will get credit for each piece of the protocol you implement. Any
questions about minor technicalities can be addressed to me via Piazza
/ email and I will respond very quickly. I will also keep the course
webpage updated.

# Part 2: Writing Tests (10 points)

You must find *two separate pieces* of the project and figure out how
to write tests for them. For example, you might choose to ensure that
users can't send messages to other users that have blocked them. Or
you might want to ensure that usernames can't start with `#`. Write
these as two separate tests using either hand-rolled code or a unit
testing framework in your language of choice. Write in this README
where you put them.

# Part 3: Password Managers and PGP (10 points)

For this part of the project, you can do one of two things:

- Install a password manager and start using it for all of your
  passwords.

- Create a [PGP key](https://www.pitt.edu/~poole/accessiblePGP703.htm)
  for yourself and begin cryptographically signing your communication
  with a few other people you communicate with. You can do this by,
  e.g., writing me an email and signing it.

You must at least *read* about how PGP works and figure out what it
means to cryptographically sign your emails. We'll cover a bit of this
in class, and you'll start to do it on project 2G with your team.

To receive credit for this part, create a document in this directory,
`experiences.txt`, and write a brief discussion of your experiences
with either of these tools. Describe the pains and advantages of using
them, and how using one of the two has informed your thoughts on
security.

# If you get stuck...

Don't spend more than an hour or two stuck on a problem. If you feel
like you're stuck and not being productive, email me sooner rather
than later. These things can be tricky. You're all very good, though,
so I know you can do it..!
