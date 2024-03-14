import { useState, useEffect } from "react";
import { Form, Container, Input, Title, Textarea, Main, Button } from "../../components";
import api from "../../api";
import styles from "./styles.module.css";
import { useParams, useHistory } from "react-router-dom";

const ScheduleEdit = () => {
  const [items, setItems] = useState([]);
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
  const [Rings, setRings] = useState([])
  const history = useHistory()
  const [loading, setLoading] = useState(true)
  const [addItem, setAddItem] = useState(false);

  useEffect((_) => {
    api
      .getRings()
      .then((res) => {
        setRings(res);
      });
  }, []);

  const handleAddItem = (e) => {
    e.preventDefault();
    setAddItem(!addItem);
  }

  const handleChangeForm = ({ item, index, e }) => {
    const { name, value } = e.target;

    if (name === 'day') {
      item[index].day = value;
    } else if (name === 'time') {
      item[index].time = value;
    }

    setItems([...Items]);
  };

  const { id } = useParams()
  useEffect(_ => {
    if (value.length === 0 || !loading) { return }
    api.getSchedule({
      group_id: id
    }).then(res => {
      setItems(res)
      setLoading(false)
    })
  }, [])

  async function handleSubmit(e) {
    e.preventDefault();

    await api.updateSchedule(Items);

    setItems([]);
    setAddItem(false);

  }

  return (
    <Main>
      <MetaTags>
        <title>Редактирование расписания группы</title>
        <meta name="description" content="Кружки - Редактирование расписания" />
        <meta property="og:title" content="Редактирование расписания" />
      </MetaTags>
      <Title title='Редактирование группы' />

      <form onSubmit={handleSubmit}>
        {Items.map((item, i) => (
          <div key={i} style={{ marginTop: '10px' }}>
            <div>Day: {item.day}</div>
            <div>Time: {item.time}</div>
          </div>
        ))
        }

        {
          addItem && (
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '20px' }}>
              <label>Day</label>
              <select name="day" onChange={(e) => handleChange(Items, Items.length, e)}>
                <option value="1">1</option>
                ...
              </select>

              <label>Time</label>
              <select name="time" onChange={(e) => handleChange(Items, Items.length, e)}>
                <option value="0">0</option>
              </select>

              <button type="button" onClick={() => setAddItem(false)}>Remove Item</button>
            </div>
          )
        }

        <button type="submit">Submit</button>
      </form >
    </Main>

  );
};

export default ScheduleEdit;
