class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question    # 문제
        self.choices = choices      # 선택지 4개 리스트
        self.answer = answer        # 정답 번호 1~4

    def show(self):
        print(self.question)
        for i, choice in enumerate(self.choices, start=1):
            print(f"  {i}. {choice}")

    def is_correct(self, user_choice):
        return user_choice == self.answer

def ask_int(prompt, low, high):
    """low~high 사이의 정수를 안전하게 입력받는다."""
    while True:
        raw = input(prompt).strip()
        if raw == "":
            print("⚠️ 입력이 비어 있습니다. 다시 입력하세요.")
            continue
        try:
            number = int(raw)
        except ValueError:
            print("⚠️ 숫자를 입력하세요.")
            continue
        if low <= number <= high:
            return number
        print(f"⚠️ {low}~{high} 사이의 숫자를 입력하세요.")

def show_menu():
    print("=" * 40)
    print("        🎯 나만의 퀴즈 게임 🎯")
    print("=" * 40)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("=" * 40)


def main():
    while True:
        show_menu()
        choice = ask_int("선택: ", 1, 5)
        if choice == 5:
            print("게임을 종료합니다. 안녕히 가세요!")
            break
        else:
            print(f"[{choice}번 기능은 곧 만듭니다]")


if __name__ == "__main__":
    main()

    