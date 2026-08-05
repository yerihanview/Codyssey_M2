import json
import os

STATE_FILE = "state.json"
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

    def to_dict(self):
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

    @classmethod
    def from_dict(cls, data):
        return cls(data["question"], data["choices"], data["answer"])

DEFAULT_QUIZZES = [
    Quiz("태양계에서 가장 큰 행성은?", ["수성", "목성", "화성", "지구"], 2),
    Quiz("대한민국의 수도는?", ["부산", "인천", "서울", "대구"], 3),
    Quiz("물의 화학식은?", ["CO₂", "H₂O", "O₂", "NaCl"], 2),
    Quiz("1년은 몇 개월인가?", ["10개월", "11개월", "12개월", "13개월"], 3),
    Quiz("무지개는 보통 몇 색으로 표현하나?", ["5색", "6색", "7색", "8색"], 3),
]

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

class QuizBank:
    """퀴즈 보관 + 최고점수 (데이터 담당). 저장 기능은 Step 10에서 추가."""

    def __init__(self):
        self.quizzes = list(DEFAULT_QUIZZES)
        self.best_score = 0

    def is_empty(self):
        return len(self.quizzes) == 0

    def add(self, quiz):
        self.quizzes.append(quiz)

    def update_best_score(self, score):
        """더 높으면 갱신하고 True, 아니면 False."""
        if score > self.best_score:
            self.best_score = score
            return True
        return False


class QuizGame:
    """메뉴·풀기·점수 진행 + 화면 (진행 담당)."""

    def __init__(self):
        self.bank = QuizBank()
        self.has_played = False

    def show_menu(self):
        print("=" * 40)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def play(self):
        if self.bank.is_empty():
            print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return
        quizzes = self.bank.quizzes
        print(f"\n📝 퀴즈를 시작합니다! (총 {len(quizzes)}문제)\n")
        score = 0
        for i, quiz in enumerate(quizzes, start=1):
            print("-" * 40)
            print(f"[문제 {i}]")
            quiz.show()
            user_choice = ask_int("정답 입력: ", 1, 4)
            if quiz.is_correct(user_choice):
                print("✅ 정답입니다!")
                score += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")
        print("=" * 40)
        print(f"🏆 결과: {len(quizzes)}문제 중 {score}문제 정답!")
        self.has_played = True
        if self.bank.update_best_score(score):
            print("🎉 새로운 최고 점수입니다!")
        print("=" * 40)

    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = input("문제를 입력하세요: ").strip()
        if question == "":
            print("⚠️ 문제가 비어 있어 취소합니다.")
            return
        choices = []
        for i in range(1, 5):
            choice = input(f"선택지 {i}: ").strip()
            if choice == "":
                print("⚠️ 선택지가 비어 있어 취소합니다.")
                return
            choices.append(choice)
        answer = ask_int("정답 번호 (1-4): ", 1, 4)
        self.bank.add(Quiz(question, choices, answer))
        print("✅ 퀴즈가 추가되었습니다!")

    def list_quizzes(self):
        if self.bank.is_empty():
            print("등록된 퀴즈가 없습니다.")
            return
        quizzes = self.bank.quizzes
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(quizzes)}개)")
        print("-" * 40)
        for i, quiz in enumerate(quizzes, start=1):
            print(f"[{i}] {quiz.question}")
        print("-" * 40)

    def show_score(self):
        if not self.has_played:
            print("아직 퀴즈를 풀지 않았습니다.")
            return
        print(f"\n🏆 최고 점수: {self.bank.best_score}문제 정답")

    def run(self):
        while True:
            self.show_menu()
            choice = ask_int("선택: ", 1, 5)
            if choice == 1:
                self.play()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                print("게임을 종료합니다. 안녕히 가세요!")
                break


if __name__ == "__main__":
    QuizGame().run()

    