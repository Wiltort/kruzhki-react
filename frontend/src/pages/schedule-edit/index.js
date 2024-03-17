import { useState, useEffect } from "react";
import {
  ScheduleForm,
  Container,
  Input,
  Title,
  Textarea,
  Main,
  Button,
} from "../../components";
import api from "../../api";
import styles from "./styles.module.css";
import { useParams, useHistory } from "react-router-dom";
import MetaTags from "react-meta-tags";

const ScheduleEdit = () => {
  const [Items, setItems] = useState([]);
  const days = [
    {
      ind: 0,
      name: "Понедельник",
    },
    {
      ind: 1,
      name: "Вторник",
    },
    {
      ind: 2,
      name: "Среда",
    },
    {
      ind: 3,
      name: "Четверг",
    },
    {
      ind: 4,
      name: "Пятница",
    },
    {
      ind: 5,
      name: "Суббота",
    },
    {
      ind: 6,
      name: "Воскресенье",
    },
  ];
  const [Rings, setRings] = useState([]);
  const history = useHistory();
  const [loading, setLoading] = useState(true);
  const [addItem, setAddItem] = useState(false);
  const [pole1, setPole1] = useState();
  const [pole2, setPole2] = useState();

  useEffect((_) => {
    api.getRings().then((res) => {
      setRings(res);
    });
  }, []);

  const handleAddItem = (e) => {
    e.preventDefault();
    setAddItem(!addItem);
  };

  const handleChangeForm = ({ item, index, e }) => {
    const { name, value } = e.target;

    if (name === "day") {
      item[index].day_of_week = value;
    } else if (name === "time") {
      item[index].time = value;
    }

    setItems([...Items]);
  };

  
  const { id } = useParams();
  const getSchedule = (id) => {
    api
    .getSchedule({
      group_id: id,
    })
    .then((res) => {
      setItems(res);
      setLoading(false);
    });
  }

  useEffect((_) => {
    if (!loading) {
      return;
    }
    api
      .getSchedule({
        group_id: id,
      })
      .then((res) => {
        setItems(res);
        setLoading(false);
      });
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();

    await api.createSchedule({
      day_of_week: pole1,
      btime: pole2,
      group_id: id,
    });
    setLoading(true);
    getSchedule(id)

  }
  async function handleDelete(e) {
    e.preventDefault();
    await api.deleteSchedule({
      group_id: id,
    });
    setLoading(true);
    getSchedule(id)
  }

  return (
    <Main>
      <Container>
        <MetaTags>
          <title>Редактирование расписания группы</title>
          <meta
            name="description"
            content="Кружки - Редактирование расписания"
          />
          <meta property="og:title" content="Редактирование расписания" />
        </MetaTags>
        <Title title="Редактирование расписания" />

        <ScheduleForm className={styles.form} onSubmit={handleSubmit}>
          <h3>Занятия:</h3>
          {Items.map((item, i) => (
            <div key={i} style={{ marginTop: "10px" }}>
              <div>
                {item.day_of_week}, {item.btime}
              </div>
            </div>
          ))}
              <h3>Добавить урок</h3>

          {
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                marginTop: "20px",
              }}
            >
              <label>День недели:</label>
              <select name="day" onChange={(e) => setPole1(e.target.value)}>
                <option defaultValue={""}>Выберите день недели</option>
                {days.map((day) => (
                  <option key={day.ind} value={day.ind}>
                    {day.name}
                  </option>
                ))}
              </select>

              <label>Урок:</label>
              <select name="time" onChange={(e) => setPole2(e.target.value)}>
                <option defaultValue={""}>Выберите номер урока</option>

                {Rings.map((Ring) => (
                  <option key={Ring.id} value={Ring.id}>
                    {Ring.number}. {Ring.begin_at} - {Ring.end_at}
                  </option>
                ))}
              </select>
            </div>
          }
          <div className={styles.actions}>


            <Button
              modifier="style_dark-blue"
              //disabled={checkIfDisabled()}
              className={styles.button}
            >
              Сохранить
            </Button>
            <div
              className={styles.deleteRecipe}
              onClick={handleDelete}
            >
              Удалить
            </div>
          </div>
        </ScheduleForm>
      </Container>
    </Main>
  );
};

export default ScheduleEdit;
