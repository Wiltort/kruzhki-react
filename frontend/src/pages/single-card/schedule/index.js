import styles from './styles.module.css'

const Schedule = ({ items }) => {
  let isEmpty = true
  for (let key in items){
    isEmpty = false
  }
  if (isEmpty) { return null }
 {return <div className={styles.ingredients}>
    <h3 className={styles['ingredients__title']}>Расписание:</h3>
    <div className={styles['ingredients__list']}>
      {items[0].items.map(({
        day_of_week,
        btime,
        etime,
      }) => <p
        key={`${day_of_week}${btime}${etime}`}
        className={styles['ingredients__list-item']}
      >
        {day_of_week}: {btime} - {etime}
      </p>)}
    </div>
  </div>}
}

export default Schedule

