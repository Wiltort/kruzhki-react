import styles from './styles.module.css'

const Ingredients = ({ ingredients }) => {
  if (!ingredients) { return null }
  return <div className={styles.ingredients}>
    <h3 className={styles['ingredients__title']}>Студенты:</h3>
    <div className={styles['ingredients__list']}>
      {ingredients.map(({
        first_name,
        last_name,
      }) => <p
        key={`${first_name}${last_name}`}
        className={styles['ingredients__list-item']}
      >
        {first_name} {last_name}
      </p>)}
    </div>
  </div>
}

export default Ingredients

