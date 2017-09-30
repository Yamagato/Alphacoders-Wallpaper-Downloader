import urllib.request, re
from urllib.error import HTTPError

finalStringImagePageUrl = "https://wall.alphacoders.com/big.php?i={}"
bitArrayGalleryPagesHTML = []
intArrayImageId = []
validGalleryURL = ""


def getIntInput(stringMessage, stringErrorMessage, intUpperBound, intLowerBound=1):
    while True:
        try:
            choice = int(getInput(stringMessage))
            if intLowerBound <= choice <= intUpperBound:
                return choice
            else:
                print(stringErrorMessage)
        except ValueError:
            print(stringErrorMessage)


def getInput(stringMessage):
    return input(stringMessage)


def imageExists(intImageId):
    try:
        with open("{}.jpg".format(intImageId), "rb") as f:
            log("\nImage {}.jpg exists. Skipping".format(intImageId))
            print("Image {}.jpg exists. Skipping".format(intImageId))
        return True
    except FileNotFoundError:
        pass
    try:
        with open("{}.png".format(intImageId), "rb") as f:
            log("\nImage {}.png exists. Skipping".format(intImageId))
            print("Image {}.png exists. Skipping".format(intImageId))
        return True
    except FileNotFoundError:
        pass
    try:
        with open("{}.jpeg".format(intImageId), "rb") as f:
            log("\nImage {}.jpeg exists. Skipping".format(intImageId))
            print("Image {}.jpeg exists. Skipping".format(intImageId))
        return True
    except FileNotFoundError:
        pass
    try:
        with open("{}.gif".format(intImageId), "rb") as f:
            log("\nImage {}.gif exists. Skipping".format(intImageId))
            print("Image {}.gif exists. Skipping".format(intImageId))
        return True
    except FileNotFoundError:
        pass
    return False


def findImageIDFromGalleryPage(bitGalleryPageHTML):
    queryImageId = re.compile("HD Wallpaper \| Background ID:[0-9]+")
    stringArrayImageId = queryImageId.findall(str(bitGalleryPageHTML))
    for stringImageId in stringArrayImageId:
        intArrayImageId.append(int(stringImageId.split(":")[1]))
    print("Discovered image ids: {}".format(str(intArrayImageId)))


def getImagePageHTML(intImageId):
    global finalStringImagePageUrl
    with urllib.request.urlopen(finalStringImagePageUrl.format(intImageId)) as f:
        return f.read()


def downloadImages():
    global intArrayImageId
    for intImageId in intArrayImageId:
        if not imageExists(intImageId):
            try:
                print("Fetching {} HTML page".format(intImageId))
                bitImagePageHTML = getImagePageHTML(intImageId)
                queryImageUrl = re.compile(
                    "(https://images[1-9]?\.alphacoders\.com/[0-9]{3}/[0-9]+\.(jpg|png|gif|jpeg))")
                print("Finding {} Url".format(intImageId))
                stringArrayImageUrl = queryImageUrl.findall(str(bitImagePageHTML))
                for stringTupleImageUrl in stringArrayImageUrl:
                    stringImageUrl = stringTupleImageUrl[0]
                    if str(intImageId) in stringImageUrl:
                        print("Image found at {}".format(stringImageUrl))
                        with urllib.request.urlopen(stringImageUrl) as f1:
                            with open("{}.{}".format(intImageId, stringImageUrl.split(".")[-1]), "wb") as f2:
                                f2.write(f1.read())
                                print("Image {}.{} downloaded".format(intImageId, stringImageUrl.split(".")[-1]))
                                log("\nImage {}.{} downloaded".format(intImageId, stringImageUrl.split(".")[-1]))
                        break
            except HTTPError:
                log("\nImage ID:{} not found".format(intImageId))
    intArrayImageId = []


def getGalleryPagesHTMLIndividual():
    allGalleryPagesScanned = False
    intGalleryPageIndex = 1
    while allGalleryPagesScanned == False:
        try:
            print("Downloading Gallery page {}".format(intGalleryPageIndex))
            with urllib.request.urlopen(stringGalleryUrl + "&page={}".format(intGalleryPageIndex)) as f:
                bitGalleryPageHTML = f.read()
                stringCheckCorrectGalleryPage = "Backgrounds - Wallpaper Abyss - Page {}".format(
                    intGalleryPageIndex)
                if (bytearray(stringCheckCorrectGalleryPage, "utf-8") in bitGalleryPageHTML) or (
                            intGalleryPageIndex == 1):
                    findImageIDFromGalleryPage(bitGalleryPageHTML)
                    downloadImages()
                else:
                    print("{} gallery pages found".format(intGalleryPageIndex - 1))
                    log("\n{} gallery pages found".format(intGalleryPageIndex - 1))
                    allGalleryPagesScanned = True
        except HTTPError:
            print("{} gallery pages found".format(intGalleryPageIndex - 1))
            log("\n{} gallery pages found".format(intGalleryPageIndex - 1))
        intGalleryPageIndex += 1


def log(stringLog):
    with open("log_latest.txt", "a") as f:
        f.write(stringLog)


def resetLog():
    import os
    try:
        os.remove("log_previous.txt")
    except FileNotFoundError:
        pass
    try:
        os.rename("log_latest.txt", "log_previous.txt")
    except FileNotFoundError:
        pass


if __name__ == "__main__":
    resetLog()
    choice = getIntInput("Select Mode:\n1).Download Gallery (One or more)\n2).Exit\n", "Please enter 1 or 2", 2)
    if choice == 1:
        stringArrayGalleryUrl = []
        while True:
            choice = getInput("Enter gallery url or type 'Break' to start downloading:\n")
            if choice == "Break":
                break
            else:
                validGalleryURL = re.compile("(https://wall\.alphacoders\.com/by_collection\.php\?id=[0-9]+)|"
                                             "(https://wall\.alphacoders\.com/by_sub_category\.php\?id=[0-9]+)|"
                                             "(https://wall\.alphacoders\.com/tags\.php\?tid=[0-9]+)|"
                                             "(https://wall\.alphacoders\.com/search\.php\?search=[^&]+)")
                try:
                    processedUrl = validGalleryURL.findall(choice)[0]
                    gottenUrl = processedUrl[0]
                    if gottenUrl is "":
                        gottenUrl = processedUrl[1]
                        if gottenUrl is "":
                            gottenUrl = processedUrl[2]
                            if gottenUrl is "":
                                gottenUrl = processedUrl[3]
                    if gottenUrl is not None and gottenUrl is not "":
                        stringArrayGalleryUrl.append(gottenUrl)
                        log("Queued Gallery: {}".format(gottenUrl))
                except IndexError:
                    print("Please enter a valid gallery url\n")
        for galleryUrl in stringArrayGalleryUrl:
            stringGalleryUrl = galleryUrl
            log("Downloading Gallery: {}".format(stringGalleryUrl))
            getGalleryPagesHTMLIndividual()
    elif choice == 2:
        exit(0)
