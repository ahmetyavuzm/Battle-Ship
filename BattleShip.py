import sys
alphabet ="ABCDEFGHIJ"
allAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
outputFile = open("Battleship.out","w")
def outputFunc(text):
    outputFile.write(text)
    print(text, end="")

try:
	if len(sys.argv[1:]) < 4:
		#outputFunc("There is missing file(s).")
		outputFunc(" kaBOOM: run for your life!\n")
		exit()
	else:

		player1ShipsFile = open(sys.argv[1])
		player2ShipsFile = open(sys.argv[2])
		player1ShotsFile = open(sys.argv[3])
		player2ShotsFile = open(sys.argv[4])

		def createPlayerGrid(playerShipFile):
			"""Creates a player grid and a dictionary of ships for a given 	player."""

			global alphabet
			playerGrid , playerShipsPositions = dict(), dict()
			playerShipsPositions["C"], playerShipsPositions["B"], playerShipsPositions["D"], playerShipsPositions["S"], playerShipsPositions["P"]  = list(), list(), list(), list(), list()

			def seperateShipsFunc(playerShipPositions):
				"""Separates a player's ships into individual dictionaries."""
				global alphabet
				nonlocal playerGrid
				allShips = dict()
				for shipType in playerShipPositions:
					positions = playerShipPositions[shipType]

					shipLength = {
						"C":5,
						"B":4,
						"D":3,
						"S":3,
						"P":2,
					}
					shipAmount = {
						"C":1,
						"B":2,
						"D":1,
						"S":1,
						"P":4,
					}

					ships = dict()
					shipNum = 1
					lastPosition = None
					constantPosition = None
					firstPositions = None
					while len(ships) != shipAmount[shipType]:
						for positionCounter in positions:
							if lastPosition == None:
								currentShip = dict()
								if constantPosition == None:
									constantPosition = positionCounter
								lastPosition = positionCounter
								currentShip[positionCounter] = {"hitStatus": False}
								playerGrid[lastPosition]["ship"] = f"{shipType}{shipNum}"
							elif len(currentShip) < shipLength[shipType]:
								lastRow, lastColumn = int(lastPosition[:-1]), lastPosition[-1]
								currentRow, currentColumn = int(positionCounter[:-1]), positionCounter[-1]
								if currentRow == lastRow and (alphabet.index(currentColumn)-1) == alphabet.index(lastColumn) or currentColumn == lastColumn and (currentRow -1) == lastRow:
									currentShip[positionCounter] = {"hitStatus": False}
									playerGrid[positionCounter]["ship"] = f"{shipType}{shipNum}"
									lastPosition = positionCounter
							else:
								break
						if len(currentShip) == shipLength[shipType]:
							
							def removeElements(ships,positions):
								firstPositions = positions.copy()
								for shipCounter in ships:
									currentShip = ships[shipCounter]
									for counter in currentShip:
										try:
											positions.remove(counter)
										except ValueError:
											pass
								return positions, firstPositions

							ships[shipNum] = currentShip
							[positions, firstPositions] = removeElements(ships,positions)
							shipNum += 1
							lastPosition = None
						else:
							try:
								if lastPosition == positions[-1]:
									raise AssertionError()
								else:
									ships.clear()
									currentShip.clear()
									shipNum = 1
									if firstPositions != None:
										positions = firstPositions
									lastPosition = positions[positions.index(constantPosition) + 1]
									constantPosition = lastPosition
									currentShip[lastPosition] = {"hitStatus": False}
							except AssertionError as msg:
								outputFunc(" kaBOOM: run for your life!\n")
								exit()

					allShips[shipType] = ships

				return allShips

			def gridFunc():
				"""Creates a player's grid with default values."""
				nonlocal playerShipsPositions
				shipC,shipB,shipD,shipS,shipP = 0,0,0,0,0
				def shipError(shipType):
					nonlocal shipB,shipC, shipD, shipP, shipS
					if shipType == "C": shipC += 1
					elif shipType == "B": shipB += 1
					elif shipType == "D": shipD += 1
					elif shipType == "S": shipS += 1
					elif shipType == "P": shipP += 1
					else: pass      
				for rowCounter in range(1,11):
					line = playerShipFile.readline()
					line = line.rstrip("\n").split(";")
					for columnCounter in range(0,10):
						try:
							if line[columnCounter] in ("C","B","D","S","P",""):
								if line[columnCounter] == "" : positionStatus = {"positionStatus" : "-", "hitStatus": False, "ship" : None, "displaySymbol" : "-"}
								else: 
									shipError(line[columnCounter])
									positionStatus = {"positionStatus" : line[columnCounter] , "hitStatus": False, "ship" : None, "displaySymbol" : "-"}
									playerShipsPositions[line[columnCounter]].append(f"{rowCounter}{alphabet[columnCounter]}")
								playerGrid[f"{rowCounter}{alphabet[columnCounter]}"] = positionStatus
							else:
								raise AssertionError
						except Exception as msg:
							outputFunc(" kaBOOM: run for your life!\n")
							exit()
				try:
					assert shipC == 5 and shipB == 8 and shipD == 3 and shipS == 3 and shipP == 8
				except AssertionError:
					outputFunc(" kaBOOM: run for your life!\n")
					exit()

				return playerGrid

			playerGrid = gridFunc()
			playerShips  = seperateShipsFunc(playerShipsPositions)
			return {"grid": playerGrid , "ships": playerShips}

		def shipsSituations(playerShips):
			"""Checks the sink status of a player's ships."""
			playerShipsSinkStatus = dict()
			gameOver = True
			for shipType in playerShips:
				sinkedShipNum = 0    
				for shipNum in playerShips[shipType]:
					for position in playerShips[shipType][shipNum]:
						hitStatus = playerShips[shipType][shipNum][position]["hitStatus"]
						if hitStatus == False:
							gameOver = False
							sinkStatus = False
							break
						else:
							sinkStatus = True
					if sinkStatus == True:
						sinkedShipNum += 1
					shipAmount = int(shipNum)
				playerShipsSinkStatus[shipType] = " ".join("X"*sinkedShipNum + "-"*(shipAmount-sinkedShipNum))
			return playerShipsSinkStatus, gameOver

		def winnerFunc(player1GameOver, player2GameOver):
			"""Determines the winner of the game."""
			global player1Datas, player2Datas
			if player1GameOver == True and player2GameOver == True:
				winner = "Draw"
			elif player1GameOver == True:
				winner = "Player2 Wins!"
			elif player2GameOver == True:
				winner = "Player1 Wins!"
			else:
				winner = None

			return winner

		def display(player1Datas, player2Datas, playerMove = None, roundNum = None, attackPosition = None, winner = None, justMove = False):
			"""Displays the current state of the game on the screen."""
			global alphabet, p1sss, p2sss
			player1grid, player2grid = player1Datas["grid"], player2Datas["grid"]

			def displayNormalHeader():
				outputFunc(playerMove+"\n\n")
				outputFunc("Round : "+str(roundNum)+"\t\t\t\t\tGrid Size: 10x10\n\n")
				outputFunc("Player1's Hidden Board\t\tPlayer2's Hidden Board\n")
			def displayFinalHeader():
				outputFunc(winner+"\n\n")
				outputFunc("Final Information\n\n")
				outputFunc("Player1's Board\t\t\t\tPlayer2's Board\n")
			def displayBattleGrid():
				
				outputFunc("  A B C D E F G H I J\t\t  A B C D E F G H I J\n")
				for rowCounter in range(1,11):
					def displayOneRow(playerGrid,rowCounter, winner):
						if rowCounter == 10: space = ""
						else: space = " "
						outputFunc(str(rowCounter)+space)
						rowList = []
						for columnCounter in alphabet:
							if winner != None and playerGrid[f"{rowCounter}{columnCounter}"]["hitStatus"] == False:
								rowList.append(playerGrid[f"{rowCounter}{columnCounter}"]["positionStatus"])
							else:
								rowList.append(playerGrid[f"{rowCounter}{columnCounter}"]["displaySymbol"])
						outputFunc(" ".join(rowList))
					displayOneRow(player1grid,rowCounter,winner)
					outputFunc("\t\t")
					displayOneRow(player2grid,rowCounter,winner)
					outputFunc("\n") 
				outputFunc("\n")

			def displayShipSituations():
				outputFunc(f"Carrier\t\t{p1sss['C']}\t\t\t\tCarrier\t\t{p2sss['C']}\n")
				outputFunc(f"Battleship\t{p1sss['B']}\t\t\t\tBattleship\t{p2sss['B']}\n")
				outputFunc(f"Destroyer\t{p1sss['D']}\t\t\t\tDestroyer\t{p2sss['D']}\n")
				outputFunc(f"Submarine\t{p1sss['S']}\t\t\t\tSubmarine\t{p2sss['S']}\n")
				outputFunc(f"Patrol Boat\t{p1sss['P']}\t\t\tPatrol Boat\t{p2sss['P']}\n\n")
			
			def displayMove():
				outputFunc("Enter your move: "+attackPosition+"\n")
			if justMove == True:
				displayMove()
			elif winner != None:
				displayFinalHeader()
				displayBattleGrid()
				displayShipSituations()
			else:
				displayNormalHeader()
				displayBattleGrid()
				displayShipSituations()
				#displayMove()

		def attack(playerDatas,position, errorExist = False):
			"""Simulates an attack on a player's grid."""
			position = position.replace(",","")
			if errorExist == False:   
				playerGrid = playerDatas["grid"]
				playerShips = playerDatas["ships"]
				if playerGrid[position]["hitStatus"] == False:
					attackSuccess = True
					playerGrid[position]["hitStatus"] = True
					if playerGrid[position]["positionStatus"] == "-":
						playerGrid[position]["displaySymbol"] = "O"  
					else:
						ShotedShip = playerGrid[position]["ship"]
						playerGrid[position]["displaySymbol"] = "X"
						playerShips[ShotedShip[0]][int(ShotedShip[1])][position]["hitStatus"] = True
				else:
					attackSuccess = False
					outputFunc(" kaBOOM: run for your life!\n")
					exit()
				playerDatas = {"grid": playerGrid , "ships": playerShips}
			
			else:
				attackSuccess = None

			return playerDatas, attackSuccess
					
		def allShotsFunc(player1ShotsFile, player2ShotsFile):

			def playerShotsFunc(playerShotsFile):
				"""Gets a list of positions for a player's shots."""
				playerShots = "".join(playerShotsFile.readlines())
				playerShots = playerShots.split(";")[:-1]
				return playerShots

			def positionError(position): # position variable has a comma (5,E)
				"""Checks for errors in the format of a shot position."""
				try:
					firstComma = position.index(",")
					positionRow, positionColumn = position[:firstComma],position[firstComma+1:]
					def indexErrors():
						nonlocal positionRow, positionColumn
						if len(positionRow) != 0 and len(positionColumn) != 0 and "," in position:
							valueErrors()
						else:
							if "," in position:
								positionRow, positionColumn = position.split(",")
								if positionRow == "" and positionColumn == "":
									errorMessage = f"IndexError: '{position}' row and column information are missing."
								elif positionRow != "" and positionColumn == "":
									errorMessage = f"IndexError: '{position}' column information is missing."
								else:
									errorMessage = f"IndexError: '{position}' row information is missing."
							else:
								if len(position) == 2:
									errorMessage = f"IndexError: '{position}' comma is missing."
								elif len(position) == 1:
									if position[0] in alphabet:
										errorMessage = f"IndexError: '{position}' row information and comma is missing."
									else:
										errorMessage = f"IndexError: '{position}' column information and comma is missing."
								else:
									errorMessage = f"IndexError: '{position}' empty position."
							raise IndexError(errorMessage)
						
					def valueErrors():
						nonlocal positionRow, positionColumn
						if 3<= len(position) <= 4:
							multipleError = 0
							try: 
								errorMessage = f"ValueError: '{position}' row information must be an integer."
								positionRow =int(positionRow)
							except ValueError:
								multipleError += 1 
							try:
								if positionColumn not in allAlphabet:
									errorMessage = f"ValueError: '{position}' column information must be a letter"
									raise ValueError
							except ValueError:
								multipleError += 1
							finally:
								if multipleError == 0:
									assertionErrors()
								else:
									if multipleError == 2:
										errorMessage = f"ValueError: '{position}' row and column informations order is wrong it must be '{positionColumn},{positionRow}' "
									raise ValueError(errorMessage)
							
						else:
							raise ValueError(f"ValueError: '{position}' to many information in one position.")
					
					def assertionErrors():
						if int(positionRow) not in range(1,11):
							raise AssertionError(f"AssertionError: {position} row must be between 1 and 10. (1 and 10 included)")
						elif positionColumn in allAlphabet and positionColumn not in alphabet:
							raise AssertionError(f"AssertionError: {position} column must be between A and J. (A and J included)")
						else:
							return #There is no assertion error.

					indexErrors()
					return {"errorExist": False, "errorMessage" : None}
				except Exception as msg:
					return {"errorExist": True , "errorMessage" : msg}
			
			def zipShots(player1shots, player2shots, counter1 = 0, counter2 = 0, allShots = list()):
				"""Combines the shots taken by each player into pairs."""
				nonlocal positionError
				try:
					playerErrors= dict()
					boll1, boll2 = True, False
					while True:
						currentPlayer1shot = player1shots[counter1]
						currentPlayer2shot = player2shots[counter2]
						errorExistPlayer1, player1message = positionError(currentPlayer1shot)["errorExist"], positionError(currentPlayer1shot)["errorMessage"]
						errorExistPlayer2, player2message = positionError(currentPlayer2shot)["errorExist"], positionError(currentPlayer2shot)["errorMessage"]
						errorExist = errorExistPlayer1 or errorExistPlayer2
						if errorExistPlayer1 == True:
							boll1 = True
							allShots.append((currentPlayer1shot,None))
							playerErrors[currentPlayer1shot] = {"player" : "Player1", "msg": player1message}
							counter1 +=1
						elif errorExistPlayer2 == True:
							boll2 = True
							if boll1:
								allShots.append((currentPlayer1shot,None))
								counter1 +=1
								boll1 = False
							allShots.append((None, currentPlayer2shot))
							playerErrors[currentPlayer2shot] = {"player" : "Player2", "msg": player2message}
							counter2 += 1
						else:
							if boll2 == True:
								allShots.append((None,currentPlayer2shot))
								counter2 +=1
								currentPlayer2shot = currentPlayer2shot = player2shots[counter2]
								boll2 = False
							else:
								allShots.append((currentPlayer1shot,currentPlayer2shot))
								counter2 +=1
								counter1 +=1

				except IndexError:
					return allShots, playerErrors

			player1shots = playerShotsFunc(player1ShotsFile)
			player2shots = playerShotsFunc(player2ShotsFile)
			allShots, playerErrors = zipShots(player1shots,player2shots)
			return allShots, playerErrors
				
		def battle(player1Datas, player2Datas, allShots, playerErrors):
			""" It is the main function of this program. 
			It calls the other functions and simulates the all battle between two players."""
			global display, attack, p1sss, p2sss, winner
			player1ships, player2ships = player1Datas["ships"], player2Datas["ships"]
			roundNum = 1
			errorSolved = True
			player1moveExist, player2moveExist = False, False
			outputFunc("Battle of Ships Game\n\n")
			for positions in allShots:
				for shotCounter in range(2):
					attackPosition = positions[shotCounter]
					if attackPosition == None:
						pass
					else:
						if shotCounter == 0 :
							playerDatas = player2Datas
							playerMove = "Player1's Move"
						else:
							playerDatas = player1Datas
							playerMove = "Player2's Move" 
						if errorSolved == True:
							display(player1Datas, player2Datas, playerMove, roundNum, attackPosition)
						
						if attackPosition in playerErrors:
							errorSolved = False
							display(player1Datas, player2Datas, playerMove, roundNum, attackPosition, justMove = True)
							outputFunc(f"When {playerErrors[attackPosition]['player']} is attacking an error ocurred: {playerErrors[attackPosition]['msg']}\n")
						else:
							display(player1Datas, player2Datas, playerMove, roundNum, attackPosition, justMove = True)
							outputFunc("\n")
							errorSolved = True
							"""if errorSolved == False:
								display(player1Datas, player2Datas, playerMove, roundNum, attackPosition, justMove = True)
								errorSolved = True"""
							if shotCounter == 0 :
								player1moveExist = True
							else: 
								player2moveExist = True

							[playerDatas,attackSuccess]  = attack(playerDatas, attackPosition)
							[p1sss, player1GameOver] = shipsSituations(player1ships)
							[p2sss, player2GameOver] = shipsSituations(player2ships)
							winner = winnerFunc(player1GameOver, player2GameOver) 
							if winner != None and playerMove == "Player2's Move":
								display(player1Datas, player2Datas, playerMove, roundNum, attackPosition, winner)
							if player1moveExist and player2moveExist:
								roundNum += 1
								player1moveExist,player2moveExist = False, False


		player1Datas = createPlayerGrid(player1ShipsFile)
		player2Datas = createPlayerGrid(player2ShipsFile)
		allShots, playerErrors = allShotsFunc(player1ShotsFile, player2ShotsFile)
		player1ships, player2ships = player1Datas["ships"], player2Datas["ships"]
		[p1sss, player1GameOver] = shipsSituations(player1ships)
		[p2sss, player2GameOver] = shipsSituations(player2ships)
		winner = winnerFunc(player1GameOver, player2GameOver)
		battle(player1Datas, player2Datas, allShots,playerErrors)

except IOError:
	def getWrongFiles(files):
		try:
			file = open(files[0])
		except:
			if len(files) == 1:
				return [files[0]]
			else:
				return [files[0]] + getWrongFiles(files[1:])
		else:
			file.close()
			if len(files) == 1:
				return []
			else:
				return getWrongFiles(files[1:])
	
	wrongfiles = getWrongFiles(sys.argv[1:5])
	if len(wrongfiles) == 1 :
		outputFunc(f"IOError: input file {wrongfiles[0]} is not reachable.\n\n")
	else:
		outputFunc(f"IOError: input files {', '.join(wrongfiles)} are not reachable.\n\n")