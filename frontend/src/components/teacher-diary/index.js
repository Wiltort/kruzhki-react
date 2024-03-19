import React, { Component } from 'react';


{/*В этом примере мы используем компоненты для отображения группы 
студентов, студентов и оценок, а также компонент таблицы для отображения оценок. 
Вы можете добавить больше функционала,
например, полосу прокрутки в таблицу, если количество уроков большое.*/}

class GroupStudent extends Component {
    render() {
      const { students, group } = this.props;
      return (
        <div>
          <h3>{group.name}</h3>
          {students.map(student => (
            <Student
              key={student.id}
              student={student}
              group={group}
              lesson={this.props.lesson}
            />
          ))}
        </div>
      );
    }
  }
  
  class Student extends Component {
    constructor(props) {
      super(props);
      this.state = {
        score: '',
    };
}

handleChange = (event) => {
this.setState({ score: event.target.value });
};

submitScore = (e) => {
e.preventDefault();
const { student, group, lesson, score } = this.state;
// Здесь отправляем оценку на сервер
alert(`Оценка ${student.name} за урок ${lesson.title} успешно добавлена`);
};

render() {
return (
<form onSubmit={this.submitScore}>
<div>
<label>Оценка:</label>
<input
type="text"
value={this.state.score}
onChange={this.handleChange}
/>
</div>
</form>
);
}
}

function Table(props) {
const { lessons, groups, students } = props;
return (
<table>
<thead>
<tr>
{lessons.map((lesson, index) => (
<th key={index}>{lesson.title}</th>
))}
</tr>
</thead>
{groups.map((group, index) => (
<GroupStudent
key={index}
lesson={lessons}
group={group}
students={students}
/>
))}
</table>
);
}