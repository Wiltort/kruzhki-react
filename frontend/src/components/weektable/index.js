import React from 'react';
{/*Для решения этой задачи вам нужно будет создать компонент Table, который будет отображать расписание
 занятий.
 В каждой ячейке таблицы будет компонент Select, который позволит пользователю выбирать время занятия.
Также вам нужно будет добавить возможность выбора нескольких занятий. Для этого вы можете использовать
 компоненты Checkbox или Radio.*/}


const WeekTable = ({ items, onSelect, Ring }) => {
    return (
      <table>
        <thead>
          <tr>
            <th>День недели</th>
            <th>Время</th>
          </tr>
        </thead>
        <tbody>
          {items.map(({ day_of_week, btime}, index) => (
            <tr key={day_of_week}>
              <td>{day_of_week}</td>
              <td>
                <select
                  value={btime}
                  onChange={(e) => onSelect(e, index)}
                >
                  {Ring.time_slots.map((time_slot) => (
                    <option key={time_slot} value={time_slot}>
                      {time_slot}
                    </option>
                  ))}
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

export default WeekTable;
