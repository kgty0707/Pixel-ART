import re

INPUT_FILE = "requirements.txt"
OUTPUT_FILE = "requirements-clean.txt"

def contains_local_path(line: str) -> bool:
    # 1) file:///C:/... 같은 로컬 경로
    if re.search(r"file://", line, re.IGNORECASE):
        return True

    # 2) conda 빌드 경로
    if re.search(r"conda-bld", line, re.IGNORECASE):
        return True

    # 3) 줄 시작이 C:\... 또는 C:/... 인 경우만 제거
    if re.match(r"^[A-Za-z]:[\\/]", line):
        return True

    return False


def clean_requirements():
    cleaned_lines = []

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            striped = line.strip()

            if not striped:
                cleaned_lines.append("")
                continue

            if contains_local_path(striped):
                print(f"[삭제됨] {striped}")
                continue

            cleaned_lines.append(striped)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("\n".join(cleaned_lines))

    print(f"\n[정리 완료] {OUTPUT_FILE} 파일이 안전하게 덮어쓰기 되었습니다.")


if __name__ == "__main__":
    clean_requirements()
