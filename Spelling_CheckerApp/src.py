#Step 1 - importing the required library
from spellchecker import SpellChecker

#Step 2 - creating the app class
class SpellCheckerApp:
    def __init__(self):
        self.spell = SpellChecker()

    def correct_text(self, text):
        words = text.split()  # "hello world" will be stored like ["hello","world"]
        corrected_words = []
    
        for word in words:
            corrected_word = self.spell.correction(word)
            if corrected_word != word.lower():
                print(f'Correcting "{word}" to "{corrected_word}"')
            corrected_words.append(corrected_word)

        #step 4 - returning the correct text
        return ' '.join(corrected_words)
    
    #step 5 - running the app
    def run(self):
        print("\n---Spell Checker---")
        
        while True:
            text = input("Enter text to check (OR type 'exit' to quit): ")

            if text.lower() == 'exit':
                print("Closing the program...")
                break

            corrected_text = self.correct_text(text)
            print(f"Corrected Text: {corrected_text}")


#Step 6 - running the main program
if __name__ == "__main__":
    SpellCheckerApp().run()