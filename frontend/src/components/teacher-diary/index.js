import styles from "./styles.module.css";

const TeacherDiary = ({
  lessons,
  students,
  handleChangeGrade,
  handleOnBlur,
}) => {
  return (
    <form onSubmit={handleOnBlur}>
      <div className={styles.teacherdiary}>
        <table className={styles.tablediary}>
          <thead className={styles.tablehead}>
            <tr>
              <th key="number">№</th>
              <th key="name">Фамилия и имя</th>
              {lessons.map((lesson) => (
                <th key={lesson.id}>{lesson.ldate}</th>
              ))}
            </tr>
          </thead>
          <tbody className={styles.tablebody}>
            {students.map((student, index) => (
              <tr>
                <th key={index + 1}>{index + 1}</th>
                <th key={student.id}>
                  {student.last_name} {student.first_name}
                </th>
                {lessons.map((lesson) => {
                  var Attending = lesson.attending.find(
                    (element) => element.student === student.id
                  );
                  if (!(Attending===undefined)){
                  return (
                    <td key={Attending.id}>
                      <input
                        type="text"
                        name={Attending.id}
                        defaultValue={
                          Attending.points || (!Attending.is_present ? "Н" : "")
                        }
                        onChange={handleChangeGrade}
                        onBlur={handleOnBlur}
                      />
                    </td>
                  );}
                  else {
                    return (<td key={`${lesson.id}.${student.id}`}>-</td>)
                  }
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </form>
  );
};
export default TeacherDiary;
