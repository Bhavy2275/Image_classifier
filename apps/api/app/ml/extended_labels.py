"""
Extended label set for CLIP zero-shot classification.

Covers thousands of real-world objects, brands and categories beyond ImageNet's 1000.
"""

# fmt: off
EXTENDED_LABELS = [
    # Gaming consoles & accessories
    "PlayStation 5", "PlayStation 4", "PlayStation 3", "Xbox Series X", "Xbox Series S",
    "Xbox One", "Xbox 360", "Nintendo Switch", "Nintendo Switch Lite", "Nintendo 3DS",
    "Nintendo DS", "Game Boy", "Wii", "Wii U", "Sega Genesis", "Atari", "Steam Deck",
    "gaming controller", "DualSense controller", "Xbox controller", "gaming headset",
    "gaming keyboard", "gaming mouse", "gaming chair", "VR headset", "Oculus Quest",
    "PlayStation VR",

    # Computers & phones
    "laptop computer", "MacBook", "MacBook Pro", "MacBook Air", "iMac",
    "desktop computer", "computer tower", "PC gaming setup", "monitor",
    "keyboard", "computer mouse", "USB hub", "webcam", "microphone",
    "iPhone", "Android phone", "smartphone", "tablet", "iPad",
    "Samsung Galaxy", "Google Pixel", "smartwatch", "Apple Watch",
    "earbuds", "AirPods", "headphones", "Bluetooth speaker",
    "charger", "power bank", "USB cable", "HDMI cable",

    # TVs & entertainment
    "television", "flat screen TV", "smart TV", "remote control", "streaming device",
    "Roku", "Apple TV", "Amazon Fire Stick", "projector", "soundbar",
    "DVD player", "Blu-ray player",

    # Kitchen & food
    "pizza", "burger", "hamburger", "sandwich", "hot dog", "taco", "burrito",
    "sushi", "ramen", "pasta", "salad", "steak", "chicken", "fish",
    "french fries", "chips", "popcorn", "ice cream", "cake", "cupcake",
    "donut", "cookie", "chocolate", "candy", "bread", "toast",
    "coffee", "latte", "cappuccino", "tea", "smoothie", "juice", "beer",
    "wine", "cocktail", "water bottle", "soda can",
    "microwave", "toaster", "blender", "coffee maker", "air fryer",
    "refrigerator", "dishwasher", "oven", "stovetop", "kitchen sink",
    "pot", "pan", "bowl", "plate", "cup", "mug", "glass",

    # Furniture & home
    "sofa", "couch", "armchair", "bed", "mattress", "pillow", "blanket",
    "dining table", "desk", "bookshelf", "bookcase", "wardrobe", "dresser",
    "lamp", "ceiling fan", "curtains", "rug", "carpet", "mirror",
    "bathtub", "shower", "toilet", "sink", "faucet",
    "door", "window", "staircase", "fireplace", "air conditioner",

    # Vehicles
    "car", "sedan", "SUV", "truck", "pickup truck", "van", "minivan",
    "sports car", "convertible", "electric car", "Tesla",
    "motorcycle", "bicycle", "scooter", "skateboard", "longboard",
    "bus", "school bus", "ambulance", "police car", "fire truck",
    "train", "subway", "tram", "airplane", "jet", "helicopter",
    "boat", "sailboat", "yacht", "kayak", "canoe",
    "forklift", "tractor", "excavator", "crane",

    # Clothing & fashion
    "t-shirt", "shirt", "dress", "skirt", "pants", "jeans", "shorts",
    "jacket", "coat", "hoodie", "sweater", "suit", "tie",
    "shoes", "sneakers", "boots", "heels", "sandals", "flip flops",
    "hat", "cap", "beanie", "sunglasses", "glasses", "watch", "ring",
    "necklace", "bracelet", "earrings", "handbag", "backpack", "wallet",

    # Sports & outdoors
    "football", "soccer ball", "basketball", "baseball", "tennis ball",
    "golf ball", "volleyball", "rugby ball", "cricket bat",
    "tennis racket", "badminton racket", "golf club", "baseball bat",
    "hockey stick", "ski", "snowboard", "surfboard", "skateboard",
    "bicycle helmet", "football helmet", "boxing gloves",
    "swimming pool", "gym equipment", "dumbbell", "barbell",
    "treadmill", "yoga mat", "jump rope",
    "tent", "sleeping bag", "hiking boots", "backpack", "compass",

    # Tools & hardware
    "hammer", "screwdriver", "wrench", "pliers", "saw", "drill",
    "tape measure", "level", "toolbox", "ladder", "shovel", "rake",
    "lawn mower", "chainsaw", "power drill",

    # Office & school
    "pen", "pencil", "marker", "highlighter", "notebook", "book",
    "textbook", "folder", "binder", "stapler", "scissors",
    "calculator", "printer", "scanner", "projector", "whiteboard",
    "desk chair", "filing cabinet",

    # Musical instruments
    "guitar", "acoustic guitar", "electric guitar", "bass guitar",
    "piano", "keyboard instrument", "violin", "cello", "trumpet",
    "saxophone", "drums", "drum kit", "flute", "harmonica",
    "microphone stand", "amplifier", "DJ equipment", "turntable",

    # Art & photography
    "camera", "DSLR camera", "mirrorless camera", "lens", "tripod",
    "painting", "canvas", "brush", "palette", "sculpture",
    "drawing", "sketch", "watercolor",

    # Medical
    "stethoscope", "syringe", "pill", "medicine", "first aid kit",
    "wheelchair", "crutches", "hospital bed", "mask", "gloves",
    "thermometer", "blood pressure monitor",

    # Plants & nature
    "flower", "rose", "sunflower", "tulip", "daisy", "orchid",
    "tree", "palm tree", "cactus", "succulent", "bonsai",
    "grass", "forest", "mountain", "beach", "ocean", "river",
    "waterfall", "desert", "snow", "rainbow", "sunset", "sunrise",
    "cloud", "storm", "lightning",

    # Buildings & places
    "house", "apartment building", "skyscraper", "office building",
    "church", "mosque", "temple", "castle", "bridge", "tunnel",
    "stadium", "airport", "train station", "shopping mall", "hotel",
    "restaurant", "cafe", "bar", "gym", "hospital", "school",
    "library", "museum", "park", "playground",

    # Tabletop games, toys & gambling
    "dice", "pair of dice", "white dice", "gaming dice", "craps dice", "six-sided dice",
    "dominoes", "domino tile", "rubik's cube", "puzzle cube", "playing cards", "poker cards",
    "poker chip", "casino chip", "chess piece", "chessboard", "chess set", "checkers",
    "mahjong tile", "mahjong set", "dartboard", "darts", "roulette wheel", "slot machine",
    "billiard ball", "pool ball", "pool table", "8-ball", "foosball table", "air hockey table",
    "arcade machine", "pinball machine", "board game", "puzzle", "jigsaw puzzle", "Lego bricks",
    "action figure", "toy car", "doll", "teddy bear", "yo-yo", "fidget spinner", "kite",

    # Everyday objects & containers
    "bottle", "plastic bottle", "glass bottle", "jar", "tin can", "aluminum can",
    "cardboard box", "wooden box", "bag", "plastic bag", "paper bag", "envelope", "package",
    "clock", "alarm clock", "wall clock", "digital clock", "hourglass", "compass",
    "flashlight", "candle", "candle holder", "lighter", "matchbox", "matches",
    "umbrella", "suitcase", "luggage", "briefcase", "padlock", "lock", "key", "keychain",
    "coin", "coins", "banknote", "paper money", "credit card", "passport", "ID card",
    "newspaper", "magazine", "book", "hardcover book", "map", "globe",
    "balloon", "gift box", "ribbon", "trophy", "medal", "badge",
    "soap", "liquid soap", "shampoo", "toothbrush", "electric toothbrush", "toothpaste", "razor",
    "sunscreen", "perfume bottle", "cologne", "makeup brush", "lipstick", "nail polish",

    # Food (more specific)
    "apple", "banana", "orange", "strawberry", "blueberry", "grape",
    "watermelon", "mango", "pineapple", "avocado", "lemon", "lime",
    "carrot", "broccoli", "tomato", "potato", "onion", "garlic",
    "mushroom", "corn", "pepper", "cucumber",
    "egg", "bacon", "sausage", "cheese", "butter", "yogurt", "milk",
    "cereal", "granola", "oatmeal", "pancake", "waffle",

    # Pets & Wildlife (beyond standard ImageNet)
    "bat", "fruit bat", "flying bat", "vampire bat",
    "octopus", "giant octopus", "squid", "cuttlefish", "jellyfish", "starfish", "sea turtle",
    "horseshoe crab", "hermit crab", "crab", "lobster", "shrimp",
    "bald eagle", "African fish eagle", "sea eagle", "eagle", "golden eagle", "hawk", "falcon", "owl",
    "fennec fox", "fennec", "desert fox", "kit fox", "arctic fox", "red fox", "fox",
    "armadillo", "pangolin", "anteater", "sloth",
    "ferret", "black-footed ferret", "weasel", "otter", "badger", "meerkat",
    "clownfish", "anemone fish", "angelfish", "seahorse", "ray", "stingray", "manta ray", "shark",
    "goldfish", "parrot", "turtle", "tortoise", "hamster", "guinea pig", "rabbit",
    "lizard", "gecko", "chameleon", "snake", "iguana", "chinchilla", "hedgehog",
    "koala", "kangaroo", "panda", "red panda", "raccoon", "lemur", "monkey", "chimpanzee",
    "lion", "tiger", "leopard", "cheetah", "jaguar", "cougar", "wolf", "bear", "polar bear",
    "elephant", "giraffe", "zebra", "hippopotamus", "rhinoceros", "camel", "deer", "moose",
]
# fmt: on

# Deduplicate while preserving order
_seen = set()
EXTENDED_LABELS = [x for x in EXTENDED_LABELS if not (x.lower() in _seen or _seen.add(x.lower()))]
