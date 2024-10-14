function addExam() {
    const examList = document.getElementById('exam-list');
    const newExam = prompt("Enter new exam name and date (e.g., English Test - 1st Nov 2024):");
    if (newExam) {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.textContent = newExam;
        examList.appendChild(li);
    }
}

function addStudent() {
    const studentList = document.getElementById('student-list');
    const newStudent = prompt("Enter new student name:");
    if (newStudent) {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.textContent = newStudent;
        studentList.appendChild(li);
    }
}
