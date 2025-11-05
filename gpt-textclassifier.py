import time
import os
from openai import OpenAI
from dotenv import load_dotenv


def classify(text:str, model_name):
    response = client.responses.create(
        model=model_name,
        instructions="""
        You are a text classifier assistant. Your primary function is to classify the given text based on the domains provided below: 

        DOMAINS:
        1. Science
        2. Programming/Technology
        3. English Literature
        4. Mathematics

        CLASSIFICATION RULES:
        1. STRICTLY carefully scan through the given text and take note of the important terminologies that would classify their domain.
        2. If such variety of terminologies exists within the text for different domains, note them and create a mean percentage of how likely it is the domain of the given text.
        3. Don't add information that is not found within the text given, only look for the text given to you.

        OUTPUT FORMAT:
        - Provide only the name of the domain with the highest percentage based on the mean percentage you calculated, without any additional comments or meta-commentary.
        - Provide the number of the domain instead of its full categorical name.
        """,
        input=f"{text}",
    )

    return response.output_text

load_dotenv()
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# text = input("Text:")

# start = time.perf_counter()
# output = classify(text)
# print(type(output), output)

# end = time.perf_counter()
# print(f"Time: {end - start:.2f}")


# Text Classifier models evaluation
import random

classification_dataset = [
    # Science (25 examples)
    ("The mitochondria is often called the powerhouse of the cell because it generates most of the cell's supply of ATP.", "science"),
    ("Photosynthesis is the process by which plants convert light energy into chemical energy stored in glucose.", "science"),
    ("The periodic table organizes elements by their atomic number and recurring chemical properties.", "science"),
    ("DNA replication occurs during the S phase of the cell cycle, creating two identical copies of genetic material.", "science"),
    ("Newton's third law states that for every action, there is an equal and opposite reaction.", "science"),
    ("The theory of plate tectonics explains the movement of Earth's lithospheric plates over the asthenosphere.", "science"),
    ("Enzymes are biological catalysts that speed up chemical reactions without being consumed in the process.", "science"),
    ("The greenhouse effect occurs when atmospheric gases trap heat radiation from Earth's surface.", "science"),
    ("Gravitational waves were first directly detected by LIGO in 2015, confirming Einstein's prediction.", "science"),
    ("Neurons transmit electrical signals through synapses using neurotransmitters as chemical messengers.", "science"),
    ("The Krebs cycle is a series of chemical reactions that generate energy through the oxidation of acetyl-CoA.", "science"),
    ("Evolution by natural selection favors traits that increase an organism's reproductive success.", "science"),
    ("The water cycle involves evaporation, condensation, precipitation, and collection processes.", "science"),
    ("Antibiotics work by targeting specific bacterial structures or metabolic pathways without harming human cells.", "science"),
    ("The speed of light in a vacuum is approximately 299,792 kilometers per second.", "science"),
    ("Meiosis produces four haploid cells from one diploid cell through two rounds of division.", "science"),
    ("The electromagnetic spectrum ranges from radio waves to gamma rays, with visible light in between.", "science"),
    ("Entropy is a measure of disorder or randomness in a thermodynamic system.", "science"),
    ("Covalent bonds form when atoms share electrons to achieve stable electron configurations.", "science"),
    ("The Big Bang theory proposes that the universe began as an extremely hot, dense point approximately 13.8 billion years ago.", "science"),
    ("Homeostasis refers to an organism's ability to maintain stable internal conditions despite external changes.", "science"),
    ("Quantum mechanics describes the behavior of matter and energy at the atomic and subatomic scale.", "science"),
    ("The carbon cycle involves the movement of carbon through the atmosphere, biosphere, hydrosphere, and geosphere.", "science"),
    ("Ribosomes are cellular structures responsible for protein synthesis by reading mRNA sequences.", "science"),
    ("The Doppler effect causes the frequency of waves to change based on the relative motion between source and observer.", "science"),
    
    # Programming/Technology (25 examples)
    ("A binary search tree maintains sorted order, allowing O(log n) lookup time in balanced cases.", "programming/technology"),
    ("Docker containers provide lightweight virtualization by sharing the host OS kernel while isolating applications.", "programming/technology"),
    ("The REST API uses HTTP methods like GET, POST, PUT, and DELETE to perform CRUD operations.", "programming/technology"),
    ("Machine learning algorithms learn patterns from data without being explicitly programmed for specific tasks.", "programming/technology"),
    ("Git version control tracks changes to code, enabling collaborative development and easy rollback.", "programming/technology"),
    ("SQL injection attacks exploit vulnerabilities by inserting malicious SQL code into input fields.", "programming/technology"),
    ("Big O notation describes the time complexity of algorithms as input size approaches infinity.", "programming/technology"),
    ("Cloud computing delivers on-demand computing resources over the internet on a pay-per-use basis.", "programming/technology"),
    ("Blockchain technology creates immutable ledgers through cryptographic hashing and distributed consensus.", "programming/technology"),
    ("The TCP/IP protocol suite enables reliable data transmission across networks through packet switching.", "programming/technology"),
    ("Agile methodology emphasizes iterative development, continuous feedback, and adaptive planning.", "programming/technology"),
    ("Neural networks consist of interconnected layers of nodes that process information similarly to biological brains.", "programming/technology"),
    ("Recursion is a programming technique where a function calls itself to solve smaller instances of a problem.", "programming/technology"),
    ("HTTPS encrypts data transmission between browsers and servers using SSL/TLS protocols.", "programming/technology"),
    ("Object-oriented programming organizes code into reusable classes with encapsulation, inheritance, and polymorphism.", "programming/technology"),
    ("A hash table uses a hash function to map keys to array indices for O(1) average-case lookup.", "programming/technology"),
    ("DevOps practices combine software development and IT operations to shorten development cycles.", "programming/technology"),
    ("Microservices architecture breaks applications into small, independently deployable services.", "programming/technology"),
    ("The CPU executes instructions by fetching, decoding, and executing them in a cycle.", "programming/technology"),
    ("Kubernetes orchestrates containerized applications across clusters of machines with automatic scaling.", "programming/technology"),
    ("Database normalization eliminates redundancy by organizing data into related tables.", "programming/technology"),
    ("Artificial intelligence systems can now generate human-like text using large language models.", "programming/technology"),
    ("RAM provides fast, temporary storage that the CPU can quickly access during program execution.", "programming/technology"),
    ("Encryption algorithms like AES secure data by transforming it into unreadable ciphertext.", "programming/technology"),
    ("The Model-View-Controller pattern separates application logic, user interface, and data handling.", "programming/technology"),
    
    # English Literature (25 examples)
    ("In Shakespeare's Hamlet, the protagonist's indecision reflects the Renaissance questioning of medieval certainties.", "english literature"),
    ("Jane Austen's Pride and Prejudice satirizes the marriage market of Regency-era England through wit and irony.", "english literature"),
    ("The stream of consciousness technique in Virginia Woolf's Mrs. Dalloway captures the fluidity of human thought.", "english literature"),
    ("George Orwell's 1984 presents a dystopian vision of totalitarianism where language itself becomes a tool of oppression.", "english literature"),
    ("The green light in The Great Gatsby symbolizes Gatsby's unreachable dreams and the American Dream's corruption.", "english literature"),
    ("Emily Dickinson's poetry often explores themes of death, immortality, and nature through unconventional syntax.", "english literature"),
    ("Chinua Achebe's Things Fall Apart depicts the collision between Igbo culture and British colonialism in Nigeria.", "english literature"),
    ("The unreliable narrator in The Catcher in the Rye reveals Holden Caulfield's psychological turmoil and alienation.", "english literature"),
    ("Mary Shelley's Frankenstein raises questions about scientific responsibility and the nature of humanity.", "english literature"),
    ("Toni Morrison's Beloved explores the psychological trauma of slavery through magical realism and fragmented narrative.", "english literature"),
    ("The Canterbury Tales uses a frame narrative to present diverse voices from medieval English society.", "english literature"),
    ("James Joyce's Ulysses parallels Homer's Odyssey while capturing a single day in Dublin with modernist techniques.", "english literature"),
    ("In To Kill a Mockingbird, Scout Finch's coming-of-age story intersects with themes of racial injustice in the Deep South.", "english literature"),
    ("The metaphysical poets like John Donne combined intellectual wit with passionate emotion in their verse.", "english literature"),
    ("Charlotte Brontë's Jane Eyre challenges Victorian gender norms through its fiercely independent heroine.", "english literature"),
    ("The Romantic poets emphasized emotion, nature, and individual experience over Enlightenment rationalism.", "english literature"),
    ("Gabriel García Márquez's One Hundred Years of Solitude exemplifies magical realism with its blend of fantasy and reality.", "english literature"),
    ("The tragic flaw of hubris leads to Oedipus's downfall in Sophocles' classical Greek drama.", "english literature"),
    ("Walt Whitman's free verse in Leaves of Grass celebrated democracy and the common person.", "english literature"),
    ("Symbolism in Lord of the Flies represents the thin veneer of civilization over human savagery.", "english literature"),
    ("The Harlem Renaissance produced writers like Langston Hughes who expressed African American cultural identity.", "english literature"),
    ("Charles Dickens' novels criticized Victorian social conditions while entertaining mass audiences with memorable characters.", "english literature"),
    ("Postcolonial literature examines the cultural and psychological impacts of imperialism on colonized peoples.", "english literature"),
    ("The iambic pentameter of Shakespeare's sonnets creates a rhythmic pattern that enhances their emotional impact.", "english literature"),
    ("Modernist literature broke from traditional forms, reflecting the fragmentation and disillusionment after World War I.", "english literature"),
    
    # Mathematics (25 examples)
    ("The Pythagorean theorem states that in a right triangle, a² + b² = c² where c is the hypotenuse.", "mathematics"),
    ("Integration is the inverse operation of differentiation and calculates the area under a curve.", "mathematics"),
    ("Prime numbers are natural numbers greater than 1 that have no positive divisors other than 1 and themselves.", "mathematics"),
    ("The quadratic formula x = (-b ± √(b²-4ac)) / 2a solves any quadratic equation ax² + bx + c = 0.", "mathematics"),
    ("Matrix multiplication is not commutative, meaning AB does not necessarily equal BA.", "mathematics"),
    ("The fundamental theorem of calculus links differentiation and integration as inverse operations.", "mathematics"),
    ("Euler's identity e^(iπ) + 1 = 0 elegantly connects five fundamental mathematical constants.", "mathematics"),
    ("A function is continuous at a point if the limit equals the function value at that point.", "mathematics"),
    ("The binomial theorem expands (a + b)^n using combinations and powers of a and b.", "mathematics"),
    ("Linear algebra studies vector spaces, linear transformations, and systems of linear equations.", "mathematics"),
    ("The derivative represents the instantaneous rate of change of a function at a given point.", "mathematics"),
    ("Probability theory quantifies uncertainty using values between 0 and 1, where 1 represents certainty.", "mathematics"),
    ("The Riemann hypothesis concerns the distribution of prime numbers and remains one of the unsolved Millennium Prize Problems.", "mathematics"),
    ("Logarithms are the inverse of exponential functions, with log_b(x) asking 'b to what power equals x?'", "mathematics"),
    ("The chain rule allows us to differentiate composite functions by multiplying derivatives.", "mathematics"),
    ("Set theory forms the foundation of modern mathematics, dealing with collections of distinct objects.", "mathematics"),
    ("The normal distribution is a bell-shaped probability distribution characterized by its mean and standard deviation.", "mathematics"),
    ("Taylor series represent functions as infinite sums of polynomial terms centered at a point.", "mathematics"),
    ("The pigeonhole principle states that if n items are placed in m containers with n > m, at least one container has multiple items.", "mathematics"),
    ("Complex numbers extend the real numbers by including the imaginary unit i where i² = -1.", "mathematics"),
    ("The mean value theorem guarantees a point where the instantaneous rate equals the average rate over an interval.", "mathematics"),
    ("Vectors have both magnitude and direction, distinguishing them from scalar quantities.", "mathematics"),
    ("The limit of a function describes its behavior as the input approaches a particular value.", "mathematics"),
    ("Group theory studies algebraic structures with a single binary operation satisfying closure, associativity, identity, and invertibility.", "mathematics"),
    ("The fundamental theorem of algebra states that every non-constant polynomial has at least one complex root.", "mathematics"),
]

gpt_models = [
    "gpt-5-mini",
    "gpt-5-nano",
    "gpt-4.1-nano",
    "gpt-4o-mini"
]

backup_texts = classification_dataset.copy()

for model in gpt_models:
    start = time.perf_counter()

    classification_dataset = backup_texts.copy()
    points = {
        "science": 0,
        "programming/technology": 0,
        "english literature": 0,
        "mathematics": 0
    }
    sample_count = 0

    for i in range(len(classification_dataset)):
        rand_num = random.randrange(0, len(classification_dataset))
        text = classification_dataset[rand_num][0]
        ref = classification_dataset[rand_num][1]
        pred = classify(text, model)

        # Convert the pred to it full name category
        match pred:
            case "1": pred = "science"
            case "2": pred = "programming/technology"
            case "3": pred = "english literature"
            case "4": pred = "mathematics"

        # Score based on prediction
        if ref == pred:
            points[ref] += 1
        
        if sample_count < 5:
            print(text)
            print(f"Reference: {ref}")
            print(f"Prediction: {pred}")
            print()
            sample_count += 1
        else:
            if i % 10 == 0:
                print(i)
        classification_dataset.pop(rand_num)

    end = time.perf_counter()
    print(f"Time: {end - start:.2f}")

    # Display model's scores
    print(f"{model} scores:")
    print(f"Science: {points['science'] / 25}")
    print(f"Programming/Technology: {points['programming/technology'] / 25}")
    print(f"English Literature: {points['english literature'] / 25}")
    print(f"Mathematics: {points['mathematics'] / 25}")
    print()
