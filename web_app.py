"""Web application cho hệ thống chấm trắc nghiệm."""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from src.storage.file_storage import FileStorageManager
from src.business.exam_manager import ExamManager
from src.business.grading_engine import GradingEngine
from src.models.submission import Submission
import uuid

app = Flask(__name__)

# Khởi tạo storage và managers
storage = FileStorageManager(base_path="data")
exam_manager = ExamManager(storage)
grading_engine = GradingEngine(storage)


@app.route('/')
def index():
    """Trang chủ."""
    return render_template('index.html')


@app.route('/teacher')
def teacher():
    """Trang giáo viên - tạo đề thi."""
    return render_template('teacher.html')


@app.route('/student')
def student():
    """Trang học sinh - làm bài thi."""
    # Lấy danh sách đề thi
    success, msg, exams = exam_manager.list_all_exams()
    return render_template('student.html', exams=exams)


@app.route('/api/create-exam', methods=['POST'])
def create_exam():
    """API tạo đề thi."""
    data = request.json
    
    # Tạo đề thi
    success, msg, exam_id = exam_manager.create_exam(
        title=data['title'],
        teacher_id=data['teacher_id']
    )
    
    if not success:
        return jsonify({'success': False, 'message': msg})
    
    # Thêm câu hỏi
    for q in data['questions']:
        success, msg, q_id = exam_manager.add_question(
            exam_id=exam_id,
            content=q['content'],
            choices=q['choices'],
            correct_answer=q['correct_answer']
        )
        
        if not success:
            return jsonify({'success': False, 'message': msg})
    
    return jsonify({
        'success': True,
        'message': 'Tạo đề thi thành công',
        'exam_id': exam_id
    })


@app.route('/api/get-exam/<exam_id>')
def get_exam(exam_id):
    """API lấy thông tin đề thi."""
    success, msg, exam_dict = exam_manager.get_exam(exam_id)
    
    if not success:
        return jsonify({'success': False, 'message': msg})
    
    return jsonify({
        'success': True,
        'exam': exam_dict
    })


@app.route('/api/submit-exam', methods=['POST'])
def submit_exam():
    """API nộp bài thi."""
    data = request.json
    
    # Tạo submission
    submission_id = f"S{uuid.uuid4().hex[:8].upper()}"
    
    submission = Submission(
        submission_id=submission_id,
        exam_id=data['exam_id'],
        student_id=data['student_id'],
        answers=data['answers']
    )
    
    # Lưu submission
    storage.save_submission(submission.to_dict())
    
    # Chấm bài
    success, msg, result = grading_engine.grade_submission(submission_id)
    
    if not success:
        return jsonify({'success': False, 'message': msg})
    
    return jsonify({
        'success': True,
        'message': 'Chấm bài thành công',
        'result': result
    })


@app.route('/api/list-exams')
def list_exams():
    """API liệt kê đề thi."""
    success, msg, exams = exam_manager.list_all_exams()
    return jsonify({
        'success': True,
        'exams': exams
    })


@app.route('/statistics')
def statistics():
    """Trang thống kê."""
    return render_template('statistics.html')


@app.route('/api/all-results')
def all_results():
    """API lấy tất cả kết quả."""
    results = storage.list_results()
    return jsonify({
        'success': True,
        'results': results
    })


@app.route('/api/delete-exam/<exam_id>', methods=['DELETE'])
def delete_exam(exam_id):
    """API xóa đề thi."""
    success, msg = exam_manager.delete_exam(exam_id)
    return jsonify({
        'success': success,
        'message': msg
    })


@app.route('/api/export-results/<exam_id>')
def export_results(exam_id):
    """API xuất kết quả ra CSV."""
    import csv
    from flask import Response
    from io import StringIO
    
    # Lấy đề thi
    success, msg, exam_dict = exam_manager.get_exam(exam_id)
    if not success:
        return jsonify({'success': False, 'message': msg})
    
    # Lấy kết quả
    results = storage.list_results(exam_id=exam_id)
    
    # Tạo CSV
    output = StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Mã HS', 'Điểm', 'Số câu đúng', 'Số câu sai', 'Tổng câu', 'Thời gian nộp'])
    
    # Data
    for result in results:
        writer.writerow([
            result['student_id'],
            result['score'],
            result['correct_answers'],
            result['wrong_answers'],
            result['total_questions'],
            result['graded_at']
        ])
    
    # Return CSV
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename=ket_qua_{exam_id}.csv'}
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
