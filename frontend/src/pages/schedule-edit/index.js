import { useState, useEffect } from "react";
import { Form, Container, Input, Title, WeekTable, Textarea, Main, Button } from "../../components";
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
  const [ loading, setLoading ] = useState(true)

  useEffect((_) => {
    api
    .getRings()
    .then((res) => {
      setRings(res);
    });
  }, []);

  const handleChange = ({ e, index }) => {
    setItems(
      items.map((value, i) =>
        i !== index ? value : { ...value, begin_at: e.target.value }
      )
    );
  };
  const { id } = useParams()
  useEffect(_ => {
    if (value.length === 0 || !loading) { return }
    api.getRecipe({
      
    })
  })
  return (
    <div>
      <WeekTable
        items={items}
        onSelect={handleChange}
        Ring={Rings}
        days={days}
      />
    </div>
  );
};

export default ScheduleEdit;
