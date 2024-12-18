import spacy
from textblob import TextBlob, Word
from difflib import get_close_matches

# Tải mô hình spaCy
nlp = spacy.load("en_core_web_sm")

# Khởi tạo từ điển tùy chỉnh
custom_words = {"hello", "world", "python", "programming", "custom", "dictionary", "example"}

def add_custom_word(word):
    """Thêm từ mới vào từ điển tùy chỉnh."""
    custom_words.add(word.lower())
    print(f"Added custom word: {word}")

def is_custom_word(word):
    """Kiểm tra xem từ có thuộc từ điển tùy chỉnh không."""
    return word.lower() in custom_words

def suggest_word(word, suggestions=3):
    """Gợi ý từ gần đúng từ từ điển tùy chỉnh."""
    print(f"Custom words: {custom_words}")  # Debug: Kiểm tra từ điển
    if not custom_words:
        print("Custom dictionary is empty.")
        return None
    suggestions = get_close_matches(word.lower(), custom_words, n=suggestions)
    if suggestions:
        print(f"Suggestions for '{word}': {suggestions}")  # Debug: Hiển thị gợi ý
        return suggestions
    print(f"No suggestions for '{word}'.")  # Debug: Không có gợi ý
    return None

def correct_spelling_with_custom_dict(text):
    """Sửa lỗi chính tả, bao gồm từ điển tùy chỉnh."""
    words = text.split()
    corrected_words = []
    for word in words:
        # Nếu là từ trong từ điển tùy chỉnh, không sửa
        if is_custom_word(word):
            corrected_words.append(word)
        else:
            # Kiểm tra gợi ý từ
            suggestions = suggest_word(word)
            if suggestions:
                print(f"Using suggestion '{suggestions[0]}' for '{word}'")  # Debug
                corrected_words.append(suggestions[0])  # Chọn gợi ý đầu tiên
            else:
                print(f"No suggestion found for '{word}', using TextBlob correction.")  # Debug
                corrected_words.append(str(Word(word).correct()))
    return " ".join(corrected_words)

def fix_sentence_case_and_punctuation(text):
    """Sửa lỗi viết hoa đầu câu và đảm bảo kết thúc câu bằng dấu chấm, dấu chấm than hoặc dấu hỏi."""
    sentences = text.split(". ")
    fixed_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        # Viết hoa chữ cái đầu câu
        if sentence[0].islower():
            sentence = sentence[0].upper() + sentence[1:]
        # Kiểm tra kết thúc câu
        if not sentence.endswith(('.', '!', '?')):
            sentence += '.'
        fixed_sentences.append(sentence)
    return " ".join(fixed_sentences)

def spell_check_and_analyze(text):
    print("Original Text:", text)
    
    # Sửa lỗi chính tả
    corrected_text = correct_spelling_with_custom_dict(text)
    print("Corrected Spelling:", corrected_text)
    
    # Sửa lỗi viết hoa và dấu câu
    fixed_text = fix_sentence_case_and_punctuation(corrected_text)
    print("Fixed Sentence Case and Punctuation:", fixed_text)
    
    # Phân tích văn bản với spaCy
    doc = nlp(fixed_text)
    
    print("\nNLP Analysis:")
    for token in doc:
        print(f"Token: {token.text}, Lemma: {token.lemma_}, POS: {token.pos_}, Dependency: {token.dep_}")

# Giao diện người dùng
def main():
    while True:
        print("\nOptions:")
        print("1. Analyze text")
        print("2. Add custom word")
        print("3. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            text = input("Enter a sentence: ")
            spell_check_and_analyze(text)
        elif choice == "2":
            word = input("Enter a word to add to custom dictionary: ")
            add_custom_word(word)
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
