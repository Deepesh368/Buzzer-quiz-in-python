import socket
import _thread
import sys
import time
import random

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(('localhost', 1234))
s.listen(3)
questions = ["What is length of a day in hours? \na.24 b.16 c.12 d.23",
             "What is the name of our planet? \na.Earth b.Pluto c.Venus d.cleopatra",
             "What is our PM's name? \na.Modi b.Michael c.popstar d.bloodborne",
             "What is 1 + 2? \na.3 b.4 c.1 d.10",
             "What is the capital of India? \na. New Delhi b.Vizag c.Bangalore d.Pune",
             "What is 10 * 2? \na.20 b.30 c.1 d.12",
             "What is the name of our galaxy? \na.Milkyway b.Way c.Galaxy d.Popquiz",
             "What is 2 + 2? \na.4 b.5 c.6 d.7",
             "What is our country's name \na.India b.China c.USA d.North Korea",
             "What is 2 + 3? \na.10 b.5 c.7 d.12",
             "What is 10 * 10? \na.50 b.70 c.100 d.123",
             "What is 1 + 5? \na.1 b.2 c.3 d.6",
             "What is 1 + 6? \na.1 b.3 c.7 d.8",
             "What is 5 * 5? a.12 b.25 c.26 d.50",
             "What is 6 * 5? \na.25 b.30 c.15 d.50",
             "What is 1 * 5? \na.6 b.5 c.7 d.11",
             "What is 10 * 6? \na.60 b.25 c.33 d.12",
             "What is 12 * 12? \na.140 b.144 c.125 d.122",
             "What is 13 * 13? \na.160 b.130 c.169 d.175",
             "What is 3 * 3? \na.20 b.25 c.7 d.9",
             "What is 3 * 4? \na.12 b.13 c.14 d.15",
             "What is 5 * 3? \na.14 b.15 c.13 d.25",
             "What is 9 * 9? \na.12 b.15 c.81 d.100",
             "What is 11 * 11? \na.121 b.100 c.150 d.160",
             "What is 6 * 7? \na.42 b.40 c.123 d.124",
             "What is 8 * 8? \na.64 b.25 c.123 d.23",
             "What is 50 + 5? \na.12 b.55 c.60 d.24",
             "What is 1000 * 2? \na.2000 b.250 c.1000 d.5000",
             "What is 1 + 99? \na.101 b.100 c.50 d.25",
             "What is 1 + 78? \na.79 b.80 c.81 d.111",
             "What is 25 + 26? \na.50 b.51 c.52 d.12",
             "What is 50 + 51? \na.101 b.25 c.26 d.1",
             "What is 10 * 9? \na.89 b.90 c.25 d.20",
             "What is 10 + 11? \na.21 b.20 c.25 d.26",
             "What is 22 + 23? \na.45 b.46 c.11 d.24"]

answers = ["a", "a", "a", "a", "a", "a",
           "a", "a", "a", "b", "c", "d", "c", "b", "b", "b", "a", "b", "c", "d", "a", "b", "c", "a", "a", "a", "b", "a", "b", "a", "b", "a", "b", "a", "a"]

scores = [0.0, 0.0, 0.0]
first_client = [s, -1]
checks = [0, 0]
client_list = []
move_on = 0


def remove_question(n):
    global questions
    global answers
    if(len(questions) != 0):
        questions.pop(n)
        answers.pop(n)


def broadcast(message):
    global client_list
    for client in client_list:
        client.send(bytes(message, "utf-8"))


def quiz():
    global client_list
    global checks
    if (len(questions) != 0):
        checks[1] = random.randint(0, 100) % len(questions)
        for connection in client_list:
            connection.send(bytes(questions[checks[1]], "utf-8"))
        time.sleep(1)
        for connection in client_list:
            connection.send(bytes("1", "utf-8"))


def game_over():
    global scores
    broadcast("Game Over!")
    print("Game Over\n")
    if(max(scores) < 5):
        broadcast("Nobody won the quiz\n")
        print("Nobody won the quiz")
    broadcast("The scores are:\nPlayer 1  " +
              str(scores[0])+"\nPlayer 2  "+str(scores[1])+"\nPlayer 3: "+str(scores[2]))
    s.close()
    sys.exit()


def client_thread(connection, address, i):
    global scores
    global first_client
    global checks
    global questions
    global answers
    global move_on
    connection.send(
        bytes("Welcome to the quiz!\nYou are player " + str(i) + "\nPress any letter for the buzzer", "utf-8"))
    while True:
        answer = str(connection.recv(1024).decode())
        if(answer is not "N"):
            if(checks[0] == 0):
                first_client[0] = connection
                checks[0] = 1
                first_client[1] = i
                broadcast("Player" + str(i) + "has pressed the buzzer\n")
                print("Player" + str(i) + "has pressed the buzzer\n")
                time.sleep(1)
                first_client[0].send(bytes("1", "utf-8"))
            elif(checks[0] == 1 and first_client[0] == connection):
                if(answer[0] is answers[checks[1]]):
                    scores[i-1] += 1
                    broadcast(
                        "Player" + str(first_client[1]) + "has answered correctly\n")
                    print(
                        "Player" + str(first_client[1]) + "has answered correctly\n")
                    if(scores[i-1] >= 5):
                        broadcast(
                            "Player" + str(first_client[1]) + "has won the game\n")
                        print(
                            "Player" + str(first_client[1]) + "has won the game\n")
                        game_over()
                        sys.exit()
                else:
                    scores[i-1] -= 0.5
                    broadcast(
                        "Player" + str(first_client[1]) + "has answered incorrectly\n")
                    print(
                        "Player" + str(first_client[1]) + "has answered incorrectly\n")
                checks[0] = 0
                move_on += 1
            else:
                move_on += 1
        elif(answer is "N"):
            if(checks[0] == 1 and first_client[0] == connection):
                scores[i-1] -= 0.5
                broadcast("Player" + str(i) + "has answered incorrectly\n")
                print("Player" + str(i) + "has answered incorrectly\n")
                checks[0] = 0
                move_on += 1
            else:
                move_on += 1
        if(move_on == 3):
            remove_question(checks[1])
            move_on = 0
            if(len(questions) == 0):
                game_over()
            else:
                quiz()


number = 0
while True:
    connection, address = s.accept()
    client_list.append(connection)
    number += 1
    print(address[0] + " connected")
    _thread.start_new_thread(client_thread, (connection, address, number))
    if(len(client_list) == 3):
        print(
            "All of the clients have been connected\nThe quiz will start in a few seconds\n")
        time.sleep(3)
        quiz()

s.close()
