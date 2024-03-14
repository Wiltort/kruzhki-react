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
      name: "MONDAY",
    },
    {
      ind: 1,
      name: "TUESDAY",
    },
    {
      ind: 2,
      name: "WEDNESDAY",
    },
    {
      ind: 3,
      name: "THURSDAY",
    },
    {
      ind: 4,
      name: "FRIDAY",
    },
    {
      ind: 5,
      name: "SATURDAY",
    },
    {
      ind: 6,
      name: "SUNDAY",
    },
  ];
  const [Rings, setRings] = useState([]);
  const history = useHistory();
  const [loading, setLoading] = useState(true);
  const [addItem, setAddItem] = useState(false);
  const [pole1,setPole1] = useState()
  const [pole2,setPole2] = useState()

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
    const { name, value } = e.target

    if (name === "day") {
      item[index].day_of_week = value;
    } else if (name === "time") {
      item[index].time = value;
    }

    setItems([...Items]);
  };

  const { id } = useParams();
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

    await api.createSchedule({day_of_week: pole1, btime: pole2, group_id: id});

    setItems([]);
    setAddItem(false);
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
          {Items.map((item, i) => (
            <div key={i} style={{ marginTop: "10px" }}>
              <div>{item.day_of_week}, {item.btime}</div>
            </div>
          ))}

          {(
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                marginTop: "20px",
              }}
            >
              
              <label>Day</label>
              <select
                name="day"
                onChange={e=> setPole1(e.target.value)}
                
              >
                        <option defaultValue={''}>Выберите Базис</option>
                {days.map((day) => (
                  <option key={day.ind} value={day.name}>
                    {day.name}
                  </option>
                ))}
              </select>

              <label>Time</label>
              <select
                name="time"
                onChange={e=> setPole2(e.target.value)}
              
              >
                {Rings.map((Ring) => (  
                  <option key={Ring.id} value={Ring.id}>
                    {Ring.begin_at}
                  </option>
                ))}
              </select>
              </div>
)}
              <button type="button" onClick={() => setAddItem(false)}>
                Remove Item
              </button>
            
          

          
          <Button
            modifier='style_dark-blue'
            //disabled={checkIfDisabled()}
            className={styles.button}
          >
            Сохранить
          </Button>
        </ScheduleForm>
      </Container>
    </Main>
  );
};

export default ScheduleEdit;
