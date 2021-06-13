import datetime

def mouseClicked(event):
    if event.button == 37: # left
        print("Next.")
        loop()
    elif event.button == 39: # right
        stamp = datetime.datetime.now().replace(microsecond=0).isoformat()
        stamp = stamp.replace(":","-")
        fn = "versions/" + stamp + ".png"
        save(fn)
        print("Saved.")
