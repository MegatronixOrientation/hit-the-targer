import cv2
import numpy as np
import pickle

# Initialize players and scores
players = ["Player 1", "Player 2"]
current_player = 0
player_scores = [0, 0]

polygons = []  # all the polygons and their points
path = []  # current single polygon

img = cv2.imread('imgBoard.png')

def mousePoints(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        path.append([x, y])

while True:
    for point in path:
        cv2.circle(img, point, 7, (0, 0, 255), cv2.FILLED)

    pts = np.array(path, np.int32).reshape((-1, 1, 2))
    img = cv2.polylines(img, [pts], True, (0, 255, 0), 2)

    cv2.putText(img, f"{players[current_player]}'s Turn", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mousePoints)
    key = cv2.waitKey(1)

    if key == ord('q'):
        score = int(input("Enter Score: "))
        polygons.append([path, score])
        print(f"{players[current_player]}: Total Polygons - {len(polygons)}")
        path = []
    if key == ord("p"):
        player_scores[current_player] = sum(score for _, score in polygons)
        print(f"{players[current_player]}: Total Score - {player_scores[current_player]}")
        current_player = (current_player + 1) % 2  # Switch player's turn
        polygons = []
        path = []

    if key == ord("s"):
        with open('polygons.pkl', 'wb') as f:
            pickle.dump(player_scores, f)
        print("Scores saved to polygons.pkl")
    
    if key == ord("q"):
        break

cv2.destroyAllWindows()
