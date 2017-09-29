import urllib.request, re
finalStringGalleryUrl = "https://wall.alphacoders.com/by_collection.php?id=34"
finalStringImagePageUrl = "https://wall.alphacoders.com/big.php?i={}"
finalStringArrayImageTypes = ["jpg", "png", "gif"]
bitArrayGalleryPagesHTML = []
intArrayImageId = []
stringLog = ""

def getGalleryPagesHTML():
	global stringLog
	allGalleryPagesScanned = False
	intGalleryPageIndex = 1
	while(allGalleryPagesScanned == False):
		try:
			print("Downloading Gallery page {}".format(intGalleryPageIndex))
			with urllib.request.urlopen(finalStringGalleryUrl.format(intGalleryPageIndex)) as f:
				bitGalleryPageHTML = f.read()
				stringCheckCorrectGalleryPage = "The Elder Scrolls HD Wallpapers | Backgrounds - Wallpaper Abyss - Page {}".format(intGalleryPageIndex)
				if (bytearray(stringCheckCorrectGalleryPage, "utf-8") in bitGalleryPageHTML) or (intGalleryPageIndex == 1):
					bitArrayGalleryPagesHTML.append(bitGalleryPageHTML)
				else:
					print("{} gallery pages found".format(intGalleryPageIndex - 1))
					stringLog += "\n{} gallery pages found".format(intGalleryPageIndex - 1)
					allGalleryPagesScanned = True
		except urllib.error.HTTPError:
			print("{} gallery pages found".format(intGalleryPageIndex - 1))
			stringLog += "\n{} gallery pages found".format(intGalleryPageIndex - 1)
		intGalleryPageIndex += 1
	
def findImageIDFromAllGalleryPages():
	queryImageId = re.compile("HD Wallpaper \| Background ID:[0-9]+")
	for bitGalleryPageHTML in bitArrayGalleryPagesHTML:
		stringArrayImageId = queryImageId.findall(str(bitGalleryPageHTML))
		print(stringArrayImageId)
		for stringImageId in stringArrayImageId:
			intArrayImageId.append(int(stringImageId.split(":")[1]))
		
def downloadImages():
	global stringLog
	for intImageId in intArrayImageId:
		if not imageExists(intImageId):
			try:
				downloadJPG(intImageId)
			except urllib.error.HTTPError:
				try:
					downloadPNG(intImageId)
				except urllib.error.HTTPError:
					try:
						downloadGIF(intImageId)
					except urllib.error.HTTPError:
						stringLog += "\nImage ID:{} not found".format(intImageId)

def downloadJPG(intImageId):
	with urllib.request.urlopen(finalStringImageUrlJPG.format(str(intImageId)[:3], intImageId)) as f1:
		with open("{}.jpg", "wb") as f2:
			f2.write(f1.read())
			stringLog += "\n{}.jpg downloaded".format(intImageId)
						
def downloadPNG(intImageId):						
	with urllib.request.urlopen(finalStringImageUrlPNG.format(str(intImageId)[:3], intImageId)) as f1:
		with open("{}.png", "wb") as f2:
			f2.write(f1.read())
			stringLog += "\n{}.png downloaded".format(intImageId)

def downloadGIF(intImageId):
	with urllib.request.urlopen(finalStringImageUrlGIF.format(str(intImageId)[:3], intImageId)) as f1:
		with open("{}.gif", "wb") as f2:
			f2.write(f1.read())
			stringLog += "\n{}.gif downloaded".format(intImageId)

def redownloadImages():
	pass

def imageExists(intImageId):
	global stringLog
	try:
		with open("{}.jpg".format(intImageId), "rb") as f:
			stringLog += "\nImage {}.jpg exists. Skipping".format(intImageId)
			print("Image {}.jpg exists. Skipping".format(intImageId))
		return True
	except FileNotFoundError:
		pass
	try:
		with open("{}.png".format(intImageId), "rb") as f:
			stringLog += "\nImage {}.png exists. Skipping".format(intImageId)
			print("Image {}.png exists. Skipping".format(intImageId))
		return True
	except FileNotFoundError:
		pass
	try:
		with open("{}.jpeg".format(intImageId), "rb") as f:
			stringLog += "\nImage {}.jpeg exists. Skipping".format(intImageId)
			print("Image {}.jpeg exists. Skipping".format(intImageId))
		return True
	except FileNotFoundError:
		pass
	try:
		with open("{}.gif".format(intImageId), "rb") as f:
			stringLog += "\nImage {}.gif exists. Skipping".format(intImageId)
			print("Image {}.gif exists. Skipping".format(intImageId))
		return True
	except FileNotFoundError:
		pass
	return False

class getGalleryPagesHTMLIndividual():
	def findImageIDFromGalleryPage(self, bitGalleryPageHTML):
		queryImageId = re.compile("HD Wallpaper \| Background ID:[0-9]+")
		stringArrayImageId = queryImageId.findall(str(bitGalleryPageHTML))
		for stringImageId in stringArrayImageId:
			print("Found {}".format(stringImageId))
			intArrayImageId.append(int(stringImageId.split(":")[1]))
		print("Discovered image ids: {}".format(str(intArrayImageId)))
		
	def getImagePageHTML(self, intImageId):
		global finalStringImagePageUrl
		with urllib.request.urlopen(finalStringImagePageUrl.format(intImageId)) as f:
			return f.read()
		
	def downloadImages(self):
		global stringLog, intArrayImageId
		for intImageId in intArrayImageId:
			if not imageExists(intImageId):
				try:
					print("Fetching {} HTML page".format(intImageId))
					bitImagePageHTML = self.getImagePageHTML(intImageId)
					queryImageUrl = re.compile("(https:\/\/images[1-9]?\.alphacoders\.com\/[0-9]{3}\/[0-9]+\.(jpg|png|gif|jpeg))")
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
									stringLog += "\nImage {}.{} downloaded".format(intImageId, stringImageUrl.split(".")[-1])
							break
				except urllib.error.HTTPError:
					stringLog += "\nImage ID:{} not found".format(intImageId)
		intArrayImageId = []
		
	def __init__(self):
		global stringLog
		allGalleryPagesScanned = False
		intGalleryPageIndex = 1
		while(allGalleryPagesScanned == False):
			try:
				print("Downloading Gallery page {}".format(intGalleryPageIndex))
				with urllib.request.urlopen(finalStringGalleryUrl + "&page={}".format(intGalleryPageIndex)) as f:
					bitGalleryPageHTML = f.read()
					stringCheckCorrectGalleryPage = "Backgrounds - Wallpaper Abyss - Page {}".format(intGalleryPageIndex)
					if (bytearray(stringCheckCorrectGalleryPage, "utf-8") in bitGalleryPageHTML) or (intGalleryPageIndex == 1):
						self.findImageIDFromGalleryPage(bitGalleryPageHTML)
						self.downloadImages()
					else:
						print("{} gallery pages found".format(intGalleryPageIndex - 1))
						stringLog += "\n{} gallery pages found".format(intGalleryPageIndex - 1)
						allGalleryPagesScanned = True
			except urllib.error.HTTPError:
				print("{} gallery pages found".format(intGalleryPageIndex - 1))
				stringLog += "\n{} gallery pages found".format(intGalleryPageIndex - 1)
			intGalleryPageIndex += 1
	
if __name__ == "__main__":
	finalStringGalleryUrl = input("Enter gallery url:\n")
	getGalleryPagesHTMLIndividual()
	with open("log.txt", "w") as f:
		f.write(stringLog)
