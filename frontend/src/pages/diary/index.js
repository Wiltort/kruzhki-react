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
import { AuthContext, UserContext } from '../../contexts'


const Diary = ({ isStaff }) => {
  const authContext = useContext(AuthContext);
  const userContext = useContext(UserContext);
  //const [ user, setUser ] = useState(null)
  const [students, setStudents] = useState([]);
  const [lessons, setLessons] = useState([]);
  const [groups, setGroups] = useState([]);
  const [group_id, setGroup_id] = useState(null);
  const [selected, setSelected] = useState(false);

  const getGroups = () => {
    api.getGroups().then((res) => {
      setGroups(res);
    });
  };

  const getLessons = ({ group_id, isStaff }) => {
    if (isStaff) {
      api.getAttendings({ id: group_id }).then((res) => {
        setStudents(res.students);
        setLessons(res.lessons);
      });
    }
  };

  useEffect((_) => {
    getGroups();
  }, []);

  useEffect((_) => {
    if (!selected) {
      return;
    }
    getLessons({ group_id: group_id, isStaff: isStaff });
  }, []);

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
          <select
            name="group"
            onChange={(e) => {
              setGroup_id(e.target.value);
              setSelected(true);
            }}
          >
            <option defaultValue={""}>Выберите группу</option>
            {groups.map((group) => (
              <option key={group.id} value={group.id}>
                {group.title}
              </option>
            ))}
          </select>
        </div>
        {authContext && isStaff && (
          <TeacherDiary lessons={lessons} students={students} />
        )}
      </Container>
    </Main>
  );
};
export default Diary;
