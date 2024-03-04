{/*Для решения этой задачи вам нужно будет создать компонент Table, 
который будет отображать расписание занятий. В каждой ячейке таблицы 
будет компонент Select, который позволит пользователю выбирать время занятия.
Также вам нужно будет добавить возможность выбора нескольких занятий. 
Для этого вы можете использовать компоненты Checkbox или Radio.
Пример кода:*/}
import { useState } from "react"
import { WeekTable } from '../../components'

function App() {
  const [items, setItems] = useState([
    {
      day: "Monday",
      begin_at: "08:00",
    },
    {
      day: "Tuesday",
      begin_at: "10:00",
    }
  ]);

  function handleChange(e, index) {
    setItems(items.map((value, i) =>
      i !== index ? value : { ...value, begin_at: e.target.value }
    ));
  }

  return (
    <div>
      <WeekTable items={items} onSelect={handleChange} />
    </div>
  );
}