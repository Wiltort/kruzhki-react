import { useState, useEffect } from "react";
import {
  ScheduleForm,
  Container,
  Title,
  Textarea,
  Main,
} from "../../components";
import api from "../../api";
import styles from "./styles.module.css";
import { useParams, useHistory } from "react-router-dom";
import MetaTags from "react-meta-tags";

const MySchedule = () => {
  const [Lessons, setLessons] = useState([]);
  const history = useHistory();
  const getLessons = () => {
    api
    .getLessons()
    .then((res) => {
      setLessons(res);
    });
  }

  useEffect((_) => {
    getLessons()
  }, []);

  return (
    <Main>
      <Container>
        <MetaTags>
          <title>Моё расписание</title>
          <meta
            name="description"
            content="Кружки - Мое расписание"
          />
          <meta property="og:title" content="Мое расписание" />
        </MetaTags>
        <Title title="Мое расписание" />

        <div>
          <h3>Занятия:</h3>
          {Lessons.map((item, i) => (
            <div key={i} style={{ marginTop: "10px" }}>
              <div>
                {item.ldate}. Группа "{item.stud_group}". Тема: "{item.topic}".
              </div>
            </div>
          ))}
              
          </div>
      </Container>
    </Main>
  );
};

export default MySchedule;
