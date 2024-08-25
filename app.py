
#By Sarveshwar Senthilkumar in 2021 & 2022

from flask import Flask, render_template, request, redirect, session
from flask_session import Session 
from datetime import datetime
import pytz
from sql import *

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def BSshipCheck(board):
  c=5
  b=4
  cr=3
  s=3
  d=2

  destroyedShips = []

  for row in board:
    for code in row:
      if "cp" in code:
        c-=1
      elif "bp" in code:
        b-=1
      elif "crp" in code:
        cr-=1
      elif "sp" in code:
        s-=1
      elif "dp" in code:
        d-=1

  if c == 0:
    destroyedShips.append("c")
  if b == 0:
    destroyedShips.append("b")
  if cr == 0:
    destroyedShips.append("cr")
  if s == 0:
    destroyedShips.append("s")
  if d == 0:
    destroyedShips.append("d")

  return destroyedShips

def getBoard(pickStr):
  rows = pickStr.split(":")

  board = []

  for row in rows:
    columns = row.split(",")
    board.append(columns)

  return board

def checkboard(board):
  win = False
  winner = "No One"
  for i in range(3):
      if board[i][0] == "X" and  board[i][1] == "X" and board[i][2] == "X":
        board[i][0] = "Xw"
        board[i][1] = "Xw"
        board[i][2] = "Xw"
        win = True
        winner = "Player 1"
      elif board[i][0] == "O" and  board[i][1] == "O" and board[i][2] == "O":
        board[i][0] = "Ow"
        board[i][1] = "Ow"
        board[i][2] = "Ow"
        win = True
        winner = "Player 2"
      if board[0][i] == "X" and  board[1][i] == "X" and board[2][i] == "X":
        board[0][i] = "Xw"
        board[1][1] = "Xw"
        board[2][2] = "Xw"
        win = True
        winner = "Player 1"
      elif board[0][i] == "O" and  board[1][i] == "O" and board[2][i] == "O":
        board[0][i] = "Ow"
        board[1][i] = "Ow"
        board[2][i] = "Ow"
        win = True
        winner = "Player 2"
  if board[0][0] == "X" and  board[1][1] == "X" and board[2][2] == "X":
      board[0][0] = "Xw"
      board[1][1] = "Xw"
      board[2][2] = "Xw"
      win = True
      winner = "Player 1"
  elif board[0][0] == "O" and  board[1][1] == "O" and board[2][2] == "O":
      board[0][0] = "Ow"
      board[1][1] = "Ow"
      board[2][2] = "Ow"
      win = True
      winner = "Player 2"
  if board[0][2] == "X" and  board[1][1] == "X" and board[2][0] == "X":
      board[0][2] = "Xw"
      board[1][1] = "Xw"
      board[2][0] = "Xw"
      win = True
      winner = "Player 1"
  elif board[0][2] == "O" and  board[1][1] == "O" and board[2][0] == "O":
      board[0][2] = "Ow"
      board[1][1] = "Ow"
      board[2][0] = "Ow"
      win = True
      winner = "Player 2"
    
  return win, winner, board

@app.route("/")
def normalRoute():
  return render_template("normal.html")

@app.errorhandler(500)
def not_found(e):
  return redirect("/results")

@app.route("/pickaspotbs")
def pickaspotbs():
  pickI=int(request.args.get("integer"))
  info = session.get("cookie")
  list1=info.split()
  id=list1[0]
  player=list1[1]
  name=list1[2]
  db = SQL("sqlite:///games.db")
  results = db.execute("SELECT * FROM games WHERE id = :id", id=id)
  pickStr = results[0]["pickStr"]
  whoseTurn = results[0]["turn"]
  pickStr2 = results[0]["pickStr2"]
  board = getBoard(pickStr)
  board2 = getBoard(pickStr2)

  if player == "player1":
    myStr = pickStr2
    myBoard = board2
  else:
    myStr = pickStr
    myBoard = board

  notList = ["c", " ", "b", " ", "cr", " ", "s", " ", "d"]

  for code in notList:
      if code in myStr:
        notList.remove(code)

  if len(notList) != 4:
      return redirect("/results")
  
  if whoseTurn == None:
    if player=="player1":
      space = int(pickI)-1
      row = int(space/10)
      column = space%10

      if "p" not in myBoard[row][column]:
     
        myBoard[row][column] += "p"

        db = SQL("sqlite:///games.db")
        db.execute("UPDaTE games SET turn = :whoseTurn WHERE id = :id", whoseTurn="player2", id=id)

  elif whoseTurn == "player1":
    if player=="player1":
      space = int(pickI)-1
      row = int(space/10)
      column = space%10
      if "p" not in myBoard[row][column]:
        myBoard[row][column] += "p"

        db = SQL("sqlite:///games.db")
        db.execute("UPDATE games SET turn = :whoseTurn WHERE id = :id", whoseTurn="player2", id=id)

  elif whoseTurn == "player2":
    if player=="player2":
     
      space = int(pickI)-1
      row = int(space/10)
      column = space%10

      if "p" not in myBoard[row][column]:
        myBoard[row][column] += "p"

        db = SQL("sqlite:///games.db")
        db.execute("UPDaTE games SET turn = :whoseTurn WHERE id = :id", whoseTurn="player1", id=id)

  
  boardStr = ""

  for row in myBoard:
    for column in row:
      boardStr += column + ","
    boardStr = boardStr[:-1]
    boardStr+=":"
  newPickStr = boardStr[:-1]
  
  if player == "player2":
    db = SQL("sqlite:///games.db")
    db.execute("UPDATE games SET pickStr = :pickStr WHERE id = :id", pickStr=newPickStr, id=id)
  else:
    db = SQL("sqlite:///games.db")
    db.execute("UPDATE games SET pickStr2 = :pickStr WHERE id = :id", pickStr=newPickStr, id=id)

  return redirect("/results")



@app.route("/pickaspot")
def pickaspot():
  pick1=int(request.args.get("integer"))
  info = session.get("cookie")
  list1=info.split()
  id=list1[0]
  player=list1[1]
  name=list1[2]

  
  db = SQL("sqlite:///games.db")
  results = db.execute("SELECT * FROM games WHERE id = :id", id=id)
  pickStr = results[0]["pickStr"]
  whoseTurn = results[0]["turn"]
  board = results[0]["pickStr"]

  mdList = []
  listOfLists = pickStr.split(":")

  for i in listOfLists:
    tempList=[]
    for j in i:
      if j.isnumeric() or j.isalpha():
        tempList.append(j)
    mdList.append(tempList)

  if whoseTurn == None:
    if player=="player1":
      space = int(pick1)-1
      row = int(space/3)
      column = space%3

      if mdList[row][column] != "X" and mdList[row][column] != "O":
        mdList[row][column] = "X"

        db = SQL("sqlite:///games.db")
        db.execute("UPDaTE games SET turn = :whoseTurn WHERE id = :id", whoseTurn="player2", id=id)

        db = SQL("sqlite:///games.db")
        db.execute("UPDATE games SET moves = :moves WHERE id = :id", moves=1, id=id)

  elif whoseTurn == "player1":
    if player=="player1":
      space = int(pick1)-1
      row = int(space/3)
      column = space%3
      if mdList[row][column] != "X" and mdList[row][column] != "O":
        mdList[row][column] = "X"

        db = SQL("sqlite:///games.db")
        db.execute("UPDATE games SET turn = :whoseTurn WHERE id = :id", whoseTurn="player2", id=id)

        db = SQL("sqlite:///games.db")
        moves = db.execute("SELECT moves FROM games WHERE id = :id", id=id)[0]["moves"]
        moves=int(moves)+1
        db = SQL("sqlite:///games.db")
        moves = db.execute("UPDATE games SET moves = :moves WHERE id = :id", moves=moves, id=id)

  elif whoseTurn == "player2":
    if player=="player2":
      space = int(pick1)-1
      row = int(space/3)
      column = space%3

      if mdList[row][column] != "X" and mdList[row][column] != "O":
        mdList[row][column] = "O"

        db = SQL("sqlite:///games.db")
        db.execute("UPDATE games SET turn = :whoseTurn WHERE id = :id", whoseTurn="player1", id=id)

        db = SQL("sqlite:///games.db")
        moves = db.execute("SELECT moves FROM games WHERE id = :id", id=id)[0]["moves"]
        moves=int(moves)+1
        db = SQL("sqlite:///games.db")
        moves = db.execute("UPDATE games SET moves = :moves WHERE id = :id", moves=moves, id=id)

  newPickStr = ""
  for row in mdList:
    for column in row:
      newPickStr+= column+","
    newPickStr=newPickStr[0:-1]+":"

  newPickStr = newPickStr[0:-1]

  db = SQL("sqlite:///games.db")
  db.execute("UPDATE games SET pickStr = :pickStr WHERE id = :id", pickStr=newPickStr, id=id)

  return redirect("/results")


@app.route("/creategame")
def created():
  name=request.args.get("data")
  game=request.args.get("game")
  if name!="":
    tz_NY = pytz.timezone('America/New_York')
    now=datetime.now(tz_NY)
    OTime= now.strftime("%d/%m/%y")
    db = SQL("sqlite:///games.db")
    if game == "rps":
      db.execute("INSERT INTO games (player1, player2, date, game) VALUES (?,?,?,?)", name,"Not Chosen Yet",OTime,"rps")
    elif game == "ttt":
      db.execute("INSERT INTO games (player1, player2, date, game, pickStr) VALUES (?,?,?,?,?)", name,"Not Chosen Yet",OTime,"ttt","1,2,3:4,5,6:7,8,9")
    elif game == "bs":
      board=""
      for num in range(1,101):
        if num % 10 == 0:
          board = board + str(num) + ":"
        else:
          board = board + str(num) +","
      
      board = board[:-1]
      board2 = board

      db.execute("INSERT INTO games (player1, player2, date, game, pickStr, pickStr2) VALUES (?,?,?,?,?,?)", name,"Not Chosen Yet",OTime,"bs",board,board2)
    results = db.execute("SELECT * FROM games")
    id=results[-1]["id"]
    session["cookie"] = str(id)+" player1 "+name+" " + game
    sentence = "ID: " + str(id)
    if game == "rps":
      return render_template("play.html", sentences=[sentence], game=game)
    elif game == "ttt":
      return render_template("play.html", sentences=[sentence], game=game, board=[["1","2","3"],["4","5","6"],["7","8","9"]])
    elif game == "bs":
      db = SQL("sqlite:///games.db")

      pickStr = db.execute("SELECT pickStr FROM games WHERE id = :id", id=id)[0]["pickStr"]

      board = getBoard(pickStr)

      return render_template("play.html", sentences=[sentence], game=game, board=board, notList=["c", "b", "cr", "s", "d"])
  else:
    return redirect("/")

@app.route("/joingame")
def rps():
  name=request.args.get("data")
  id=request.args.get("id")
  db = SQL("sqlite:///games.db")
  player2yet = db.execute("SELECT * FROM games WHERE id = :id", id=id)
  name=name.strip()

  game=player2yet[0]["game"]

  board = player2yet[0]["pickStr"]

  if game == "ttt":
    db = SQL("sqlite:///games.db")
    results = db.execute("SELECT * FROM games WHERE id = :id", id=id)
    pickStr = results[0]["pickStr"]
    whoseTurn = results[0]["turn"]

    mdList = []
    listOfLists = pickStr.split(":")

    for i in listOfLists:
      tempList=[]
      for j in i:
        if j !=",":
          tempList.append(j)
      mdList.append(tempList)

  if player2yet[0]["player2"] == "Not Chosen Yet" and name!="":
    db.execute("UPDATE games SET player2 = :name WHERE id=:id", name=name, id=id)
    session["cookie"] = str(id)+" player2 "+name+" " + game

    if game == "ttt":
      return render_template("play.html", sentences=[""], game=game, board=mdList)
    elif game == "rps":
      return render_template("play.html", sentences=[""], game=game)
    elif game == "bs":
      db = SQL("sqlite:///games.db")
      results = db.execute("SELECT * FROM games WHERE id = :id", id=id)
      pickStr2 = results[0]["pickStr2"]
      board = getBoard(pickStr2)
      return render_template("play.html", sentences=[""], game=game, board=board, notList=["c", "b", "cr", "s", "d"])
  else:
    return redirect("/")

@app.route("/play")
def play():
  return render_template("play.html")

def getCoordinate(pickI):

  row, column = pickI.split(",")

  row, column = int(row), int(column)

  row-=1
  column-=1

  return row, column

@app.route("/assignship")
def assignship():
  info = session.get("cookie")
  list1=info.split()
  id=list1[0]
  player=list1[1]
  name=list1[2]

  db = SQL("sqlite:///games.db")
  results=db.execute("SELECT * FROM games WHERE id = :id", id=id)
  if player == "player1":
    pickStr=results[0]["pickStr"]
  else:
    pickStr=results[0]["pickStr2"]
  board = getBoard(pickStr)
  otherBoard = board

  pickI = request.args.get("data")
  angle = request.args.get("game")
  ship = request.args.get("ship")

  space = int(pickI)-1
  row = int(space/10)
  column = space%10

  firstMove = str(row) + "," + str(column) 

  places = [firstMove]

  if ship == "carrier":
    placeholder = "c"
    placesNum = 5
    placesNum -= 1
    if angle == "h":
      while placesNum > 0:
        column += 1
        move = str(row) + "," + str(column) 
        places.append(move)
        placesNum-=1
    elif angle == "v":
      while placesNum > 0:
        row += 1
        move = str(row) + "," + str(column) 
        places.append(move)
        placesNum-=1
  elif ship == "battleship":
    placeholder = "b"
    placesNum = 4
    placesNum -= 1
    if angle == "h":
      while placesNum > 0:
        column += 1
        move = str(row) + "," + str(column) 
        places.append(move)
        placesNum-=1
    elif angle == "v":
      while placesNum > 0:
        row += 1
        move = str(row) + "," + str(column) 
        places.append(move)
        placesNum-=1
  elif ship == "cruiser" or ship == "submarine":
    if ship == "cruiser":
      placeholder = "cr"
    else:
      placeholder = "s"
    placesNum = 3
    placesNum -= 1
    if angle == "h":
      while placesNum > 0:
        column += 1
        move = str(row) + "," + str(column) 
        places.append(move)
        placesNum-=1
    elif angle == "v":
      while placesNum > 0:
        row += 1
        move = str(row) + "," + str(column) 
        places.append(move)
        placesNum-=1
  elif ship == "destroyer":
    placeholder = "d"
    placesNum = 2
    placesNum -= 1
    if angle == "h":
        column += 1
        move = str(row) + "," + str(column) 
        places.append(move)
        placesNum-=1
    elif angle == "v":
        row += 1
        move = str(row) + "," + str(column) 
        places.append(move)
        placesNum-=1
  for place in places:
    row, column = place.split(",")
    row = int(row)
    column = int(column)

    if board[row][column].isnumeric():
      board[row][column] += placeholder
    else:
      board = otherBoard
      break

  boardStr = ""

  listBoard = board
    
  for row in board:
    for column in row:
      boardStr += column + ","
    boardStr = boardStr[:-1]
    boardStr+=":"
  board = boardStr[:-1]

  if player == "player1":
      db = SQL("sqlite:///games.db")
      db.execute("UPDATE games SET pickStr = :pickStr WHERE id = :id", pickStr=board, id=id)
  else:
      db = SQL("sqlite:///games.db")
      db.execute("UPDATE games SET pickStr2 = :pickStr WHERE id = :id", pickStr=board, id=id)

  return redirect("/results")

@app.route("/results")
def results():
  info = session.get("cookie")
  list1=info.split()
  id=list1[0]
  player=list1[1]
  name=list1[2]
  
  db = SQL("sqlite:///games.db")
  results = db.execute("SELECT * FROM games WHERE id = :id", id=id)
  player1=results[0]["player1"]
  player2=results[0]["player2"]
  pickStr = results[0]["pickStr"]

  game = results[0]["game"]
  sentenceList=[]
  if game == "rps":
    games=pickStr.split()
    sentenceList=[]
    score1=0
    score2=0
    if len(games[-1]) == 1:
      games=games[0:-1]
    if player=="player1":
      sentenceList.append("You are " + player1 + "(Player 1)")
    else:
      sentenceList.append("You are " + player2 + "(Player 2)")
    gameNum = len(games)+1
    games=games[::-1]
    for i in games:
      play1=i[0]
      play2=i[1]
      if play1 == "r":
        if play2 == 'r':
          gameNum-=1
          sentenceList.append("")
          sentenceList.append("Game: " + str(gameNum))
          sentenceList.append(player1+": Rock(Draw)")
          sentenceList.append(player2+": Rock(Draw)")
        elif play2 == 'p':
          gameNum-=1
          sentenceList.append("")
          sentenceList.append("Game: " + str(gameNum))
          sentenceList.append(player1+": Rock(Loser)")
          sentenceList.append(player2+": Paper(Winner)")
          score2+=1
        else:
          gameNum-=1
          sentenceList.append("")
          sentenceList.append("Game: " + str(gameNum))
          sentenceList.append(player1+": Rock(Winner)") 
          sentenceList.append(player2+": Scissors(Loser)")
          score1+=1
      elif play1 == "p":
        if play2 == 'p':
          gameNum-=1
          sentenceList.append("")
          sentenceList.append("Game: " + str(gameNum))
          sentenceList.append(player1+": Paper(Draw)")
          sentenceList.append(player2+": Paper(Draw)")
        elif play2 == 's':
          gameNum-=1
          sentenceList.append("")
          sentenceList.append("Game: " + str(gameNum))
          sentenceList.append(player1+": Paper(Loser)")
          sentenceList.append(player2+": Scissors(Winner)")
          score2+=1
        else:
          gameNum-=1
          sentenceList.append("")
          sentenceList.append("Game: " + str(gameNum))
          sentenceList.append(player1+": Paper(Winner)")
          sentenceList.append(player2+": Rock(Loser)")
          score1+=1
      elif play1 == "s":
        if play2 == 's':
          gameNum-=1
          sentenceList.append("")
          sentenceList.append("Game: " + str(gameNum))
          sentenceList.append(player1+": Scissors(Draw)")
          sentenceList.append(player2+": Scissors(Draw)")
        elif play2 == 'r':
          gameNum-=1
          sentenceList.append("")
          sentenceList.append("Game: " + str(gameNum))
          sentenceList.append(player1+": Scissors(Loser)")
          sentenceList.append(player2+": Rock(Winner)")
          score2+=1
        else:
          gameNum-=1
          sentenceList.append("")
          sentenceList.append("Game: " + str(gameNum))
          sentenceList.append(player1+": Scissors(Winner)")
          sentenceList.append(player2+": Paper(Loser)")
          score1+=1
    sentenceScore = player1+": " + str(score1) + " || "+player2+": " + str(score2)
    sentenceList.insert(1, sentenceScore)
    
    start="n"
    db = SQL("sqlite:///games.db")
    results = db.execute("SELECT * FROM games WHERE id = :id", id=id)
    pickStr = results[0]["pickStr"]

    if pickStr!=None:
      if score1 != 3 and score2 !=3:
        if player=="player1":
          if pickStr[-1] == " ":
            start="y"
          else:
            sentenceList.insert(2, "")
            sentence="Game "+str(len(games)+1)+": Please wait for Player 2..." 
            sentenceList.insert(3, sentence)
        else:
          if pickStr[-1] != " ":
            start="y"
          else:
            sentenceList.insert(2, "")
            sentence="Game "+str(len(games)+1)+": Please wait for Player 1..." 
            sentenceList.insert(3, sentence)
      
    else:
      start="y"

    if score1 == 3:
      sentenceWon = player1+"(Player 1) won the tournament"
      sentenceList.insert(0, sentenceWon)
      sentenceList.insert(1,"")
      start="n"
    elif score2 == 3:
      sentenceWon = player2+"(Player 2) won the tournament"
      sentenceList.insert(0, sentenceWon)
      sentenceList.insert(1,"")
      start="n"
    
    return render_template("menu.html", sentences=sentenceList, start=start, game="rps")

  elif game == "ttt":
    db = SQL("sqlite:///games.db")
    results = db.execute("SELECT * FROM games WHERE id = :id", id=id)
    pickStr = results[0]["pickStr"]
    whoseTurn = results[0]["turn"]

    mdList = []
    listOfLists = pickStr.split(":")

    for i in listOfLists:
      tempList=[]
      for j in i:
        if j !=",":
          tempList.append(j)
      mdList.append(tempList)

    win, winner, board = checkboard(mdList)

    if player=="player1":
      sentenceList.append("You are " + player1 + " (Player 1 : 'X')")
    else:
      sentenceList.append("You are " + player2 + " (Player 2 : 'O')")

    db = SQL("sqlite:///games.db")
    moves = db.execute("SELECT moves FROM games WHERE id = :id", id=id)

    if win==True and winner=="Player 1":
      sentenceWon = player1+"(Player 1) won the tournament"
      sentenceList.insert(0, sentenceWon)
      sentenceList.insert(1,"")
      start="n"
    elif win==True and winner=="Player 2":
      sentenceWon = player2+"(Player 2) won the tournament"
      sentenceList.insert(0, sentenceWon)
      sentenceList.insert(1,"")
      start="n"
    elif moves == 9:
      sentenceWon = player2+"No One Won the tournament"
      sentenceList.insert(0, sentenceWon)
      sentenceList.insert(1,"")
      start="n"

    if pickStr!=None:
      if win == False:
        if player=="player1":
          if whoseTurn == player:
            start="y"
          else:
            sentenceList.insert(2, "")
            sentence="Please wait for Player 2..." 
            sentenceList.insert(3, sentence)
            start="n"
        else:
          if whoseTurn == player:
            start="y"
          else:
            sentenceList.insert(2, "")
            sentence="Please wait for Player 1..." 
            sentenceList.insert(3, sentence)
            start="n"

    sentenceID = "The Game ID is " + id
    sentenceList.append(sentenceID)

    return render_template("menu.html", sentences=sentenceList, start=start, game="ttt", board=board)
  elif game == "bs":
    win = False
    start = "y"
    whoseTurn = results[0]["turn"]

    if whoseTurn == None:
      whoseTurn = "player1"

    pickStr = results[0]["pickStr"]
    pickStr2 = results[0]["pickStr2"]

    if player == "player1":
      myStr = pickStr
      opponentStr = pickStr2
      board = getBoard(pickStr)
      board2 = getBoard(pickStr2)
    else:
      myStr = pickStr2
      opponentStr = pickStr
      board = getBoard(pickStr2)
      board2 = getBoard(pickStr)

    notList = ["c", " ", "b", " ", "cr", " ", "s", " ", "d"]

    for code in notList:
      if code in myStr:
        notList.remove(code)
    
    opponentNotList = ["c", " ", "b", " ", "cr", " ", "s", " ", "d"]

    for code in opponentNotList:
      if code in opponentStr:
        opponentNotList.remove(code)

    if pickStr!=None and len(notList) == 4:
      if win == False:
        if player=="player1":
          if whoseTurn == player:
            start="y"
        
          else:
            sentenceList.insert(2, "")
            sentence="Please wait for Player 2..." 
            sentenceList.insert(3, sentence)
            start="n"
        else:
          if whoseTurn == player:
            start="y"
          else:
            sentenceList.insert(2, "")
            sentence="Please wait for Player 1..." 
            sentenceList.insert(3, sentence)
            start="n"

    if len(opponentNotList) != 4 and player == "player1":
      sentenceID = "Please wait for Player 2..." 
      sentenceList.append(sentenceID)
      sentence=""
      sentenceList.append(sentence)
      start="n"
    elif len(opponentNotList) != 4:
      sentenceID = "Please wait for Player 1..." 
      sentenceList.append(sentenceID)
      sentence=""
      sentenceList.append(sentence)
      start="n"

    sentenceID = "The Game ID is " + id
    sentenceList.append(sentenceID)

    if len(notList) == 4 and len(opponentNotList) == 4:

      pickStrE = results[0]["pickStr"]
      pickStr22 = results[0]["pickStr2"]

      boardE = getBoard(pickStrE)
      board22 = getBoard(pickStr22)
        
      destroyedShips = BSshipCheck(boardE)
      destroyedShips2 = BSshipCheck(board22)

      
      if len(destroyedShips) > 0:
        for i in range(10):
          for j in range(10):
            for ship in destroyedShips:
              shipCode = ship + "p"
              if player == "player1":
                if shipCode in board[i][j]:
                  column = board[i][j]
                  column = column[:-1] + "sd"
                  board[i][j] = column
              else:
                if shipCode in board2[i][j]:
                  column = board2[i][j]
                  column = column[:-1] + "sd"
                  board2[i][j] = column

      if len(destroyedShips2) > 0:
        for i in range(10):
          for j in range(10):
            for ship in destroyedShips2:
              shipCode = ship + "p"
              if player == "player1":
                if shipCode in board2[i][j]:
                  column = board2[i][j]
                  column = column[:-1] + "sd"
                  board2[i][j] = column
              else:
                if shipCode in board[i][j]:
                  column = board[i][j]
                  column = column[:-1] + "sd"
                  board[i][j] = column
      if player == "player1":
        youDestroyedShips = destroyedShips
        enemyDestroyedShips = destroyedShips2
      else:
        youDestroyedShips = destroyedShips2
        enemyDestroyedShips = destroyedShips
      
      yourDestroyedShips = []
      opponentDestroyedShips = []
    
      for i in youDestroyedShips:
        if "cr" in i:
          s = "  Cruiser - 3"
        elif "b" in i:
          s = "  Battleship - 4"
        elif "c" in i:
          s = "  Carrier - 3"
        elif "s" in i:
          s = "  Submarine - 3"
        elif "d" in i:
          s = "  Destroyer - 2"

        yourDestroyedShips.append(s)
      
      for i in enemyDestroyedShips:
        if "cr" in i:
          s = "  Cruiser - 3"
        elif "b" in i:
          s = "  Battleship - 4"
        elif "c" in i:
          s = "  Carrier - 3"
        elif "s" in i:
          s = "  Submarine - 3"
        elif "d" in i:
          s = "  Destroyer - 2"

        opponentDestroyedShips.append(s)

      if len(yourDestroyedShips) > 0:
        sentence = "Your destroyed ships: "
        sentenceList.append(sentence)

        for ship in yourDestroyedShips:
          sentenceList.append(ship)
        
        sentenceList.append(" ")

      if len(opponentDestroyedShips) > 0:
        sentence = "Opponent's destroyed ships: "
        sentenceList.append(sentence)

        for ship in opponentDestroyedShips:
          sentenceList.append(ship)
        
        sentenceList.append(" ")
      
      if len(destroyedShips) == 5:
        win = True
        winner = "Player 2"
      elif len(destroyedShips2) == 5: 
        win = True
        winner = "Player 1"

      if win==True and winner=="Player 1":
        sentenceList = []
        sentenceWon = player1+"(Player 1) won the tournament"
        sentenceList.insert(0, sentenceWon)
        sentenceList.insert(1,"")
        sentenceID = "The Game ID is " + id
        sentenceList.append(sentenceID)
      elif win==True and winner=="Player 2":
        sentenceList = []
        sentenceWon = player2+"(Player 2) won the tournament"
        sentenceList.insert(0, sentenceWon)
        sentenceList.insert(1,"")
        sentenceID = "The Game ID is " + id
        sentenceList.append(sentenceID)
      
      if win == True:
        notList = [" ", " ", " ", " "]
        start = "n"
        return render_template("menu.html", sentences=sentenceList, start=start, game="bs", board=board, board2=board2, notList=notList)

    if len(notList) == 4:
      return render_template("menu.html", sentences=sentenceList, start=start, game="bs", board=board, board2=board2, notList=notList)
     
    elif len(notList) != 4:
      return render_template("play.html", sentences=sentenceList, start=start, game="bs", board=board, board2=board2, notList=notList)

  
@app.route("/viewtodaytourns")
def viewtodaytourns():
  tz_NY = pytz.timezone('America/New_York')
  now=datetime.now(tz_NY)
  OTime= now.strftime("%d/%m/%y")

  db = SQL("sqlite:///games.db")
  results = db.execute("SELECT * FROM games WHERE date = :date", date=OTime)

  return render_template("results.html", results=results)

@app.route("/results2")
def results2():
  id=request.args.get("data")

  db = SQL("sqlite:///games.db")
  results = db.execute("SELECT * FROM games WHERE id = :id", id=id)

  game = results[0]["game"]

  if game == "rps":
    db = SQL("sqlite:///games.db")
    results = db.execute("SELECT * FROM games WHERE id = :id", id=id)

    player1=results[0]["player1"]
    player2=results[0]["player2"]
    pickStr = results[0]["pickStr"]
    games=pickStr.split()
    sentenceList=[]
    score1=0
    score2=0

    gameNum = len(games)+1
    games=games[::-1]
    for i in games:
      play1=i[0]
      if len(i) == 1:
        play2="Not Yet"
      else:
        play2=i[1]
      if play1 == "r":
        if play2 == 'r':
          gameNum-=1
          sentenceList.append("")
          sentenceList.append("Game: " + str(gameNum))
          sentenceList.append(player1+": Rock(Draw)")
          sentenceList.append(player2+": Rock(Draw)")
        elif play2 == 'p':
          gameNum-=1
          sentenceList.append("")
          sentenceList.append("Game: " + str(gameNum))
          sentenceList.append(player1+": Rock(Loser)")
          sentenceList.append(player2+": Paper(Winner)")
          score2+=1
        else:
          gameNum-=1
          sentenceList.append("")
          sentenceList.append("Game: " + str(gameNum))
          sentenceList.append(player1+": Rock(Winner)") 
          sentenceList.append(player2+": Scissors(Loser)")
          score1+=1
      elif play1 == "p":
        if play2 == 'p':
          gameNum-=1
          sentenceList.append("")
          sentenceList.append("Game: " + str(gameNum))
          sentenceList.append(player1+": Paper(Draw)")
          sentenceList.append(player2+": Paper(Draw)")
        elif play2 == 's':
          gameNum-=1
          sentenceList.append("")
          sentenceList.append("Game: " + str(gameNum))
          sentenceList.append(player1+": Paper(Loser)")
          sentenceList.append(player2+": Scissors(Winner)")
          score2+=1
        else:
          gameNum-=1
          sentenceList.append("")
          sentenceList.append("Game: " + str(gameNum))
          sentenceList.append(player1+": Paper(Winner)")
          sentenceList.append(player2+": Rock(Loser)")
          score1+=1
      elif play1 == "s":
        if play2 == 's':
          gameNum-=1
          sentenceList.append("")
          sentenceList.append("Game: " + str(gameNum))
          sentenceList.append(player1+": Scissors(Draw)")
          sentenceList.append(player2+": Scissors(Draw)")
        elif play2 == 'r':
          gameNum-=1
          sentenceList.append("")
          sentenceList.append("Game: " + str(gameNum))
          sentenceList.append(player1+": Scissors(Loser)")
          sentenceList.append(player2+": Rock(Winner)")
          score2+=1
        else:
          gameNum-=1
          sentenceList.append("")
          sentenceList.append("Game: " + str(gameNum))
          sentenceList.append(player1+": Scissors(Winner)")
          sentenceList.append(player2+": Paper(Loser)")
          score1+=1
    sentenceScore = player1+": " + str(score1) + " || "+player2+": " + str(score2)
    sentenceList.insert(0, sentenceScore)
    
    start="nspecial"
    db = SQL("sqlite:///games.db")
    results = db.execute("SELECT * FROM games WHERE id = :id", id=id)
    pickStr = results[0]["pickStr"]

    if score1 == 3:
      sentenceWon = player1+"(Player 1) won the tournament"
      sentenceList.insert(0, sentenceWon)
      sentenceList.insert(1,"")
      start="nspecial"
    elif score2 == 3:
      sentenceWon = player2+"(Player 2) won the tournament"
      sentenceList.insert(0, sentenceWon)
      sentenceList.insert(1,"")
      start="nspecial"
    
    sentenceID = "The Game ID is " + id
    sentenceList.append(sentenceID)

    return render_template("menu.html", sentences=sentenceList, start=start)
  elif game == "ttt":
    sentenceList=[]

    player1=results[0]["player1"]
    player2=results[0]["player2"]
    
    db = SQL("sqlite:///games.db")
    results = db.execute("SELECT * FROM games WHERE id = :id", id=id)
    pickStr = results[0]["pickStr"]
    whoseTurn = results[0]["turn"]

    info = session.get("cookie")
    list1=info.split()
    id=list1[0]
    player=list1[1]
    name=list1[2]


    mdList = []
    listOfLists = pickStr.split(":")

    for i in listOfLists:
      tempList=[]
      for j in i:
        if j !=",":
          tempList.append(j)
      mdList.append(tempList)

    win, winner, board = checkboard(mdList)



    db = SQL("sqlite:///games.db")
    moves = db.execute("SELECT moves FROM games WHERE id = :id", id=id)

    if win==True and winner=="Player 1":
      sentenceWon = player1+"(Player 1) won the tournament"
      sentenceList.insert(0, sentenceWon)
      sentenceList.insert(1,"")
      start="n"
    elif win==True and winner=="Player 2":
      sentenceWon = player2+"(Player 2) won the tournament"
      sentenceList.insert(0, sentenceWon)
      sentenceList.insert(1,"")
      start="n"
    elif moves == 9:
      sentenceWon = player2+"No One Won the tournament"
      sentenceList.insert(0, sentenceWon)
      sentenceList.insert(1,"")
      start="n"

    if pickStr!=None:
      if win == False:
        if player=="player1":
          if whoseTurn == player:
            start="y"
          else:
            sentenceList.insert(2, "")
            sentence="Please wait for Player 2..." 
            sentenceList.insert(3, sentence)
            start="n"
        else:
          if whoseTurn == player:
            start="y"
          else:
            sentenceList.insert(2, "")
            sentence="Please wait for Player 1..." 
            sentenceList.insert(3, sentence)
            start="n"
    sentenceID = "The Game ID is " + id
    sentenceList.append(sentenceID)

    return render_template("menu.html", sentences=sentenceList, start=start, game="ttt", board=board)
  elif game == "bs":
    sentenceList=[]

    pickStrE = results[0]["pickStr"]
    pickStr22 = results[0]["pickStr2"]

    print(pickStrE, pickStr22)

    board = getBoard(pickStrE)
    board2 = getBoard(pickStr22)

    sentenceID = "The Game ID is " + id
    sentenceList.append(sentenceID)

    start="n"

    return render_template("menu.html", sentences=sentenceList, start=start, game="bs", board=board, board2=board2, showResults="true")
  

@app.route("/rock")
def rock():
  info = session.get("cookie")
  list1=info.split()
  id=list1[0]
  player=list1[1]
  name=list1[2]

  db = SQL("sqlite:///games.db")
  results = db.execute("SELECT * FROM games WHERE id = :id", id=id)
  pickStr = results[0]["pickStr"]
  if pickStr!=None:
    if player=="player1":
      if pickStr[-1] == " ":
        pickStr+="r"
    else:
      if pickStr[-1] != " ":
        pickStr+="r "
  else:
    pickStr=""
    pickStr+="r"

  db = SQL("sqlite:///games.db")
  db.execute("UPDATE games SET pickStr = :pickStr WHERE id = :id", pickStr=pickStr, id=id)

  return redirect("/results")


@app.route("/paper")
def paper():
  info = session.get("cookie")
  list1=info.split()
  id=list1[0]
  player=list1[1]
  name=list1[2]

  db = SQL("sqlite:///games.db")
  results = db.execute("SELECT * FROM games WHERE id = :id", id=id)
  pickStr = results[0]["pickStr"]
  if pickStr!=None:
    if player=="player1":
      if pickStr[-1] == " ":
        pickStr+="p"
    else:
      if pickStr[-1] != " ":
        pickStr+="p "
  else:
    pickStr=""
    pickStr+="p"

  db = SQL("sqlite:///games.db")
  db.execute("UPDATE games SET pickStr = :pickStr WHERE id = :id", pickStr=pickStr, id=id)

  return redirect("/results")


@app.route("/scissors")
def scissors():
  info = session.get("cookie")
  list1=info.split()
  id=list1[0]
  player=list1[1]
  name=list1[2]

  db = SQL("sqlite:///games.db")
  results = db.execute("SELECT * FROM games WHERE id = :id", id=id)
  pickStr = results[0]["pickStr"]
  if pickStr!=None:
    if player=="player1":
      if pickStr[-1] == " ":
        pickStr+="s"
    else:
      if pickStr[-1] != " ":
        pickStr+="s "
  else:
    pickStr=""
    pickStr+="s"
  
  db = SQL("sqlite:///games.db")
  db.execute("UPDATE games SET pickStr = :pickStr WHERE id = :id", pickStr=pickStr, id=id)

  return redirect("/results")

@app.route("/convertdata")
def convertdata():
  db = SQL("sqlite:///games.db")
  games = db.execute("SELECT id, pickStr, pickStr2, game FROM games")

  file = open("gameData.txt", "a")

  for game in games:
    print(game)
    if game["game"] == "rps" and game["pickStr"] != None:
      sentence = "Game " + str(game["id"]) + " - Rock-Paper-Scissors: \n"
      file.write(sentence)
      rounds = game["pickStr"].split(" ")
      for round in rounds:
        if len(round) >= 2:
          player1=""
          player2=""
          play1 = round[0]
          play2 = round[1]
          if round[0] == "r":
            player1="Rock"
          elif round[0] == "p":
            player1="Paper"
          elif round[0] == "s":
            player1="Scissors"
          if round[1] == "r":
            player2="Rock"
          elif round[1] == "p":
            player2="Paper"
          elif round[1] == "s":
            player2="Scissors"

          if play1 == "r":
            if play2 == 'r':
              winner="Draw"
            elif play2 == 'p':
              winner="Player 2"
            else:
              winner="Player 1"
          elif play1 == "p":
            if play2 == 'p':
              winner="Draw"
            elif play2 == 's':
              winner="Player 2"
            else:
              winner = "Player 1"
          elif play1 == "s":
            if play2 == 's':
              winner="Draw"
            elif play2 == 'r':
              winner="Player 2"
            else:
              winner="Player 1"

          roundStr = "  Player 1: " + player1 + " - " + "Player 2: " + player2 + " : Winner: " + winner + "\n\n"
        else:
          roundStr = "  Not enough plays yet"
        file.write(roundStr + "\n\n")
    elif game["game"] == "ttt" and game["pickStr"] != None:
      numbersStill=0
      sentence = "Game " + str(game["id"]) + " - Tic-Tac-Toe: \n"
      file.write(sentence)
      pickStr = game["pickStr"]
      rows = pickStr.split(":")
      winner = "Draw"
      for row in rows:
        if "Xw" in row:
          winner = "Player 1"
        elif "Ow" in row:
          winner = "Player 2"
        rowStr = "  " + row + "\n"
        file.write(rowStr)
        for column in row:
          if column.isnumeric():
            numbersStill += 1
      
      if numbersStill > 1:
        winner = "Game is still going..."
      sentence = "  Winner: " + winner + "\n\n"
      file.write(sentence)
    elif game["game"] == "bs" and game["pickStr"] != None:
      sentence = "Game " + str(game["id"]) + " - Battleship: \n"
      file.write(sentence)
      sentence = "  Player 1's Ships: \n"
      file.write(sentence)
      pickStr = game["pickStr"]
      rows = pickStr.split(":")
      for row in rows:
        rowStr = "    " + row + "\n"
        file.write(rowStr)
      sentence = "\n  Player 2's Ships: \n"
      file.write(sentence)
      pickStr2 = game["pickStr2"]
      rows2 = pickStr2.split(":")

      for row in rows2:
        rowStr = "    " + row + "\n"
        file.write(rowStr)
      
      board = getBoard(pickStr)
      board2 = getBoard(pickStr2)

      destroyedShips = BSshipCheck(board)
      destroyedShips2 = BSshipCheck(board2)

      board1Str=" "
      board2Str=" "

      if len(destroyedShips) < 5 and len(destroyedShips2) < 5:
        winner = "Game is still going..."
      elif len(destroyedShips) == 5:
        winner = "Player 2"
      elif len(destroyedShips2) == 5:
        winner = "Player 1"
      for i in destroyedShips:
        if "cr" in i:
          s = "Cruiser,"
        elif "b" in i:
          s = "Battleship,"
        elif "c" in i:
          s = "Carrier,"
        elif "s" in i:
          s = "Submarine,"
        elif "d" in i:
          s = "Destroyer,"

        board1Str += s
      
      for i in destroyedShips2:
        if "cr" in i:
          s = "Cruiser,"
        elif "b" in i:
          s = "Battleship,"
        elif "c" in i:
          s = "Carrier,"
        elif "s" in i:
          s = "Submarine,"
        elif "d" in i:
          s = "Destroyer,"

        board2Str += s
      
      board1Str = board1Str[:-1]
      board2Str = board2Str[:-1]

      if board1Str == "":
        board1Str = " No ships have been destroyed yet"
      if board2Str == "":
        board2Str = " No ships have been destroyed yet"

      sentence = "\n  Player 1's Destroyed Ships:" + board1Str + "\n"
      file.write(sentence)

      sentence = "\n  Player 2's Destroyed Ships:" + board2Str + "\n"
      file.write(sentence)
      
      sentence = "\n  Winner: " + winner + "\n\n"
      file.write(sentence)
  
  file.close()

  return str(results)
