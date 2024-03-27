import { useState, useEffect, useContext } from "react";
import {
  ScheduleForm,
  Container,
  Input,
  Title,
  Textarea,
  Main,
  Button,
  TeacherDiary,
} from "../../components";
import api from "../../api";
import styles from "./styles.module.css";
import { useParams, useHistory } from "react-router-dom";
import MetaTags from "react-meta-tags";
import { AuthContext, UserContext } from "../../contexts";

const Diary = ({ isStaff }) => {
  const authContext = useContext(AuthContext);
  const userContext = useContext(UserContext);
  //const [ user, setUser ] = useState(null)
  const [students, setStudents] = useState([]);
  const [lessons, setLessons] = useState([]);
  const [groups, setGroups] = useState([]);
  const [group_id, setGroup_id] = useState(null);
  const [selected, setSelected] = useState(false);
  const [id, setId] = useState(null);
  const [isSending, setIsSending] = useState(false);
  const [value, setValue] = useState(null);
  const [teacher, setTeacher] = useState("");
  const [student, setStudent] = useState(null);

  const getGroups = () => {
    api.getGroups().then((res) => {
      setGroups(res);
    });
  };

  const handleChangeGrade = (e) => {
    e.preventDefault();
    setId(e.target.name);
    setValue(e.target.value);
  };

  const sendGrades = (e) => {
    e.preventDefault();
    setIsSending(true);
    if (id === null || value === null) {
      return;
    }
    if (Number(value) >= 0) {
      api
        .updateAttending({ id: id, points: Number(value), is_present: true })
        .then((res) => {
          setIsSending(false);
          setId(null);
        });
    } else {
      if (value === "Н") {
        api
          .updateAttending({ id: id, points: null, is_present: false })
          .then((res) => {
            setIsSending(false);
            setId(null);
          });
      } else {
        setIsSending(false);
        return alert("Введено неверное значение");
      }
    }
  };

  useEffect((_) => {
    if (isStaff) {
      return;
    }
    api.getUserData().then((res) => {
      setStudent(res);
    });
  }, []);

  const getLessons = ({ group_id, isStaff }) => {
    if (isStaff) {
      api.getAttendings({ id: group_id }).then((res) => {
        if (res.students) {
          setStudents(res.students);
        } else {
          setStudents([]);
        }
        if (res.lessons) {
          setLessons(res.lessons);
        } else {
          setLessons([]);
        }
      });
    } else {
      api.getAttendings({ id: group_id }).then((res) => {
        setTeacher(res.teacher);
        if (res.lessons) {
          setLessons(res.lessons);
        } else {
          setLessons([]);
        }
      });
    }
  };

  const handleChange = (e) => {
    const val = e.target.value;
    if (val === "" || val === "Выберите группу") {
      setSelected(false);
      return;
    }
    setGroup_id(e.target.value);
    setSelected(true);
  };

  useEffect((_) => {
    getGroups();
  }, []);

  useEffect(
    (_) => {
      if (!selected) {
        return;
      }
      getLessons({ group_id: group_id, isStaff: isStaff });
    },
    [group_id, isStaff]
  );

  return (
    <Main>
      <Container>
        <MetaTags>
          <title>Курсы</title>
          <meta name="description" content="Кружки - Журнал" />
          <meta property="og:title" content="Кружки" />
        </MetaTags>
        <div className={styles.title}>
          <Title title="Журнал" />
        </div>
        <div>
          <label>Группа: </label>
          <select name="group" onChange={handleChange}>
            <option defaultValue={""}>Выберите группу</option>
            {groups.map((group) => (
              <option key={group.id} value={group.id}>
                {group.title}
              </option>
            ))}
          </select>
        </div>
        {authContext && isStaff && selected && (
          <TeacherDiary
            lessons={lessons}
            students={students}
            handleChangeGrade={handleChangeGrade}
            handleOnBlur={sendGrades}
          />
        )}
        {authContext && !isStaff && selected && (
          <div>
            <label>Куратор группы: {teacher}</label>
            <h3>Оценки:</h3>
            {lessons.map((lesson) => {
              const Attending = lesson.attending.find(
                (element) => element.student === student.id
              );
              return (
                <p>
                  Дата: {lesson.ldate}. Оценка: {Attending.points}
                </p>
              );
            })}
          </div>
        )}
      </Container>
    </Main>
  );
};
export default Diary;
