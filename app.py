from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)


# 학생 리스트를 파일에서 읽어오는 함수
def read_students_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            # 줄바꿈을 제거하고 공백 라인은 무시
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []


# 학생들을 조별로 나누는 함수
def assign_groups(students, group_size):
    # 학생 리스트를 랜덤하게 섞음
    random.shuffle(students)

    num_groups = len(students) // group_size  # 5명씩 배정한 그룹 수
    remainder = len(students) % group_size  # 남는 학생 수

    groups = [students[i * group_size:(i + 1) * group_size] for i in range(num_groups)]

    # 남는 학생이 있으면 마지막 조에 추가
    if remainder > 0:
        for i in range(remainder):
            groups[i].append(students[num_groups * group_size + i])

    return groups


@app.route('/')
def index():
    return render_template('group_assignment.html')


@app.route('/assign', methods=['POST'])
def assign():
    data = request.get_json()
    group_size = data.get('groupSize', 1)

    # students.txt.txt 파일에서 학생 리스트 읽어오기
    students = read_students_from_file('students.txt')

    if not students:
        return jsonify({'error': '학생 목록을 찾을 수 없습니다.'})

    # 조 배정
    groups = assign_groups(students, group_size)

    return jsonify({'groups': groups})


if __name__ == '__main__':
    app.run(debug=True)