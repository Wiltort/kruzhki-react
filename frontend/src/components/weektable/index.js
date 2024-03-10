import { useState, useContext, table } from "react";
import { AuthContext } from "../../contexts";

const WeekTable = ({ items, onSelect, Ring, days }) => {
  return (
    <table>
      <thead>
        <tr>
          <th key="MONDAY">Понедельник</th>
          <th key="TUESDAY">Вторник</th>
          <th key="WEDNESDAY">Среда</th>
          <th key="THURSDAY">Четверг</th>
          <th key="FRIDAY">Пятница</th>
          <th key="SATURDAY">Суббота</th>
          <th key="SUNDAY">Воскресение</th>
        </tr>
      </thead>
      <tbody>
        {Ring.map((v, i) => (
          <tr>
            {days.map((val, ind) => (
              <td 
              key={val.name}
              onClick={() => this.onSelect(val.ind,v.number)}
              >
                {v.number}. {v.begin_at} - {v.end_at}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default WeekTable;
