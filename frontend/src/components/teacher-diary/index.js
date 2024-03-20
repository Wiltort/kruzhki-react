import styles from "./style.module.css";

const TeacherDiary = ({ lessons, students }) => {

  return (
    <div className={styles.TeacherDiary}>
      <table>
        <thead>
          <tr>
            <th key="number">№</th>
            <th key="name">Фамилия и имя</th>
            {lessons.map((lesson) => (
              <th key={lesson.id}>{lesson.topic}. lesson.ldate</th>
            ))}
          </tr>
        </thead>
        {students.map((student, index) => (
          <tr>
            <td key={index + 1}>{index + 1}</td>
            <td key={student.id}>
              {student.last_name} {student.first_name}
            </td>
            {lessons.map((lesson) => {
              const Attending = lesson.attending.find(
                (element) => element.student == student.id
              );
              <td key={Attending.id}>
                {Attending.points}
                {!Attending.is_present ? "Н" : ""}
              </td>;
            })}
          </tr>
        ))}
      </table>
    </div>
  );
};
export default TeacherDiary;
